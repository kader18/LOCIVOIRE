# Locivoire — Scènes 3D Gaussian Splatting

## Usage immédiat (recommandé)

1. Reconstruisez une pièce hors plateforme (Polycam, SuperSplat, Luma, pipeline gsplat…).
2. Dans **Médias immersifs**, onglet **Splat 3D**, uploadez un fichier `.splat` / `.ply` / `.ksplat`.
3. Ouvrez la **visite immersive** → bouton **Splat 3D**.

## Depuis une vidéo Locivoire

1. Uploadez une vidéo walkthrough (20–40 s, mouvement lent).
2. Cliquez **→ Splat 3D** sur la carte vidéo.
3. Traitez les jobs :

```bash
python manage.py process_splat_jobs
```

Sans worker GPU, le job échoue après extraction des images — uploadez alors un fichier splat généré ailleurs.

## Worker GPU (optionnel)

Définissez une commande qui lit `SPLAT_FRAMES_DIR` et écrit `SPLAT_OUTPUT_FILE` :

```bash
# PowerShell
$env:SPLAT_WORKER_CMD = "python path\to\votre_script_gsplat.py"
python manage.py process_splat_jobs
```

Ou dans `settings.py` :

```python
SPLAT_WORKER_CMD = r'python C:\path\to\votre_script_gsplat.py'
SPLAT_WORKER_TIMEOUT = 3600
```

Votre machine dispose d’un GPU NVIDIA (8 Go) — idéal pour un worker local gsplat / video-3d-reconstruction-gsplat.

## Dépendances

```bash
pip install imageio imageio-ffmpeg
```
