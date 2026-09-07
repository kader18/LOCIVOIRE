"""
Pipeline Gaussian Splatting pour Locivoire.

- Extraction d'images depuis une vidéo (imageio-ffmpeg)
- Reconstruction réelle via commande externe (SPLAT_WORKER_CMD) si configurée
  Exemple (Linux/GPU) :
    SPLAT_WORKER_CMD="python -m gsplat.scripts.fit ..."

Sans worker GPU, le job reste en échec explicite après extraction —
l'upload manuel d'un .splat/.ply fonctionne toujours.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files import File

logger = logging.getLogger(__name__)


def extract_frames_from_video(video_path: str, out_dir: Path, max_frames: int = 80) -> int:
    """Extrait des frames JPEG depuis une vidéo. Retourne le nombre d'images."""
    try:
        import imageio.v3 as iio
    except ImportError as exc:
        raise RuntimeError(
            'Installez imageio et imageio-ffmpeg : pip install imageio imageio-ffmpeg'
        ) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        meta = iio.immeta(video_path, plugin='pyav')
    except Exception:
        meta = {}
    fps = float(meta.get('fps') or 24)
    # ~2 fps de captation pour une reconstruction stable
    step = max(int(round(fps / 2.0)), 1)

    count = 0
    try:
        for i, frame in enumerate(iio.imiter(video_path, plugin='pyav')):
            if i % step != 0:
                continue
            count += 1
            dest = out_dir / f'frame_{count:04d}.jpg'
            iio.imwrite(dest, frame)
            if count >= max_frames:
                break
    except Exception:
        # Fallback plugin
        count = 0
        for i, frame in enumerate(iio.imiter(video_path)):
            if i % step != 0:
                continue
            count += 1
            dest = out_dir / f'frame_{count:04d}.jpg'
            iio.imwrite(dest, frame)
            if count >= max_frames:
                break

    if count < 8:
        raise RuntimeError(
            f'Trop peu d’images extraites ({count}). Filmez 15–40 s en tournant lentement dans la pièce.'
        )
    return count


def run_external_splat_worker(frames_dir: Path, output_splat: Path) -> None:
    """
    Lance SPLAT_WORKER_CMD si défini.
    Variables d'environnement injectées :
      SPLAT_FRAMES_DIR, SPLAT_OUTPUT_FILE
    """
    cmd = getattr(settings, 'SPLAT_WORKER_CMD', None) or os.environ.get('SPLAT_WORKER_CMD')
    if not cmd:
        raise RuntimeError(
            'Aucun worker GPU configuré (SPLAT_WORKER_CMD). '
            'Uploadez un fichier .splat/.ply, ou configurez un worker gsplat sur GPU.'
        )

    env = os.environ.copy()
    env['SPLAT_FRAMES_DIR'] = str(frames_dir.resolve())
    env['SPLAT_OUTPUT_FILE'] = str(output_splat.resolve())

    logger.info('Lancement worker splat : %s', cmd)
    result = subprocess.run(
        cmd,
        shell=True,
        env=env,
        capture_output=True,
        text=True,
        timeout=getattr(settings, 'SPLAT_WORKER_TIMEOUT', 3600),
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or 'erreur worker').strip()
        raise RuntimeError(f'Worker splat en échec : {err[:800]}')

    if not output_splat.exists() or output_splat.stat().st_size < 1000:
        raise RuntimeError('Le worker n’a pas produit de fichier splat valide.')


def process_splat_job(splat) -> None:
    """Traite un PropertySplat (pending/processing) jusqu'à ready ou failed."""
    from properties.models import PropertySplat

    if not isinstance(splat, PropertySplat):
        raise TypeError('splat invalide')

    splat.status = 'processing'
    splat.error_message = ''
    splat.save(update_fields=['status', 'error_message', 'updated_at'])

    work = Path(tempfile.mkdtemp(prefix=f'lv_splat_{splat.pk}_'))
    try:
        # Cas 1 : fichier déjà uploadé
        if splat.splat_file and splat.splat_file.name:
            splat.status = 'ready'
            splat.save(update_fields=['status', 'updated_at'])
            return

        if not splat.source_video_id or not splat.source_video.video:
            raise RuntimeError('Aucune vidéo source ni fichier splat.')

        video_path = splat.source_video.video.path
        frames_dir = work / 'frames'
        out_splat = work / 'scene.splat'

        n = extract_frames_from_video(video_path, frames_dir)
        splat.frames_extracted = n
        splat.save(update_fields=['frames_extracted', 'updated_at'])

        run_external_splat_worker(frames_dir, out_splat)

        with out_splat.open('rb') as fh:
            splat.splat_file.save(f'property_{splat.property_id}_splat_{splat.pk}.splat', File(fh), save=False)
        splat.status = 'ready'
        splat.error_message = ''
        splat.save()
    except Exception as exc:
        logger.exception('Splat job %s failed', splat.pk)
        splat.status = 'failed'
        splat.error_message = str(exc)[:2000]
        splat.save(update_fields=['status', 'error_message', 'updated_at'])
    finally:
        shutil.rmtree(work, ignore_errors=True)
