from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec profils Locivoire"""

    USER_TYPE_CHOICES = [
        ('owner', 'Prestataire'),
        ('tenant', 'Locataire'),
        ('admin', 'Administrateur'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        verbose_name="Type d'utilisateur"
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name="Téléphone"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de naissance"
    )
    place_of_birth = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Lieu de naissance"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )
    id_card_front = models.ImageField(
        upload_to='id_cards/',
        null=True,
        blank=True,
        verbose_name="Pièce d'identité (recto)"
    )
    id_card_back = models.ImageField(
        upload_to='id_cards/',
        null=True,
        blank=True,
        verbose_name="Pièce d'identité (verso)"
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Vérifié"
    )
    verification_note = models.TextField(
        blank=True,
        verbose_name="Note de vérification"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_owner(self):
        return self.user_type == 'owner'

    @property
    def is_tenant(self):
        return self.user_type == 'tenant'

    @property
    def is_platform_admin(self):
        return self.is_staff or self.user_type == 'admin'


class ContactMessage(models.Model):
    """Messages envoyés à l'équipe Locivoire (admin)."""

    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('closed', 'Clos'),
    ]

    name = models.CharField(max_length=120, verbose_name='Nom')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Téléphone')
    subject = models.CharField(max_length=180, verbose_name='Sujet')
    message = models.TextField(verbose_name='Message')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Statut'
    )
    sender = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='contact_messages',
        verbose_name='Utilisateur lié'
    )
    admin_note = models.TextField(blank=True, verbose_name='Note admin')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Reçu le')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} — {self.name}"
