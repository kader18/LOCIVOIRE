from django.core.management.base import BaseCommand

from properties.models import PropertySplat
from properties.splat_pipeline import process_splat_job


class Command(BaseCommand):
    help = (
        'Traite les jobs Gaussian Splatting en file (pending). '
        'Nécessite SPLAT_WORKER_CMD pour la reconstruction GPU, '
        'sinon seuls les fichiers déjà uploadés passent en ready.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=5, help='Nombre max de jobs')
        parser.add_argument('--id', type=int, default=None, help='Traiter un job précis')
        parser.add_argument('--retry-failed', action='store_true', help='Réessayer les échecs')

    def handle(self, *args, **options):
        qs = PropertySplat.objects.select_related('source_video', 'property')
        if options['id']:
            qs = qs.filter(pk=options['id'])
        elif options['retry_failed']:
            qs = qs.filter(status='failed')
        else:
            qs = qs.filter(status='pending')

        jobs = list(qs.order_by('created_at')[: options['limit']])
        if not jobs:
            self.stdout.write(self.style.WARNING('Aucun job à traiter.'))
            return

        for job in jobs:
            self.stdout.write(f'→ Job #{job.pk} ({job.property.title})…')
            process_splat_job(job)
            job.refresh_from_db()
            if job.status == 'ready':
                self.stdout.write(self.style.SUCCESS(f'  OK ready — {job.splat_file.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'  ÉCHEC — {job.error_message[:200]}'))
