from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from accounts.models import User


class Property(models.Model):
    """Modèle pour les propriétés à louer"""
    
    PROPERTY_TYPE_CHOICES = [
        ('house', 'Maison'),
        ('apartment', 'Appartement'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('land', 'Terrain'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('rented', 'Louée'),
        ('pending', 'En attente'),
        ('unavailable', 'Indisponible'),
    ]
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties',
        limit_choices_to={'user_type': 'owner'},
        verbose_name="Propriétaire"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    description = models.TextField(
        verbose_name="Description"
    )
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name="Type de propriété"
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Ville"
    )
    country = models.CharField(
        max_length=100,
        default="Côte d'Ivoire",
        verbose_name="Pays"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude (GPS)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude (GPS)"
    )
    price_per_room = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix par chambre (FCFA)"
    )
    number_of_rooms = models.PositiveIntegerField(
        verbose_name="Nombre de pièces"
    )
    number_of_bedrooms = models.PositiveIntegerField(
        verbose_name="Nombre de chambres"
    )
    number_of_bathrooms = models.PositiveIntegerField(
        default=1,
        verbose_name="Nombre de salles de bain"
    )
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Superficie (m²)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="Statut"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mise en avant"
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
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.city}"
    
    @property
    def is_available(self):
        return self.status == 'available'


class Room(models.Model):
    """Modèle pour les chambres individuelles d'une propriété"""
    
    ROOM_TYPE_CHOICES = [
        ('bedroom', 'Chambre'),
        ('living_room', 'Salon'),
        ('kitchen', 'Cuisine'),
        ('bathroom', 'Salle de bain'),
        ('dining_room', 'Salle à manger'),
        ('office', 'Bureau'),
        ('balcony', 'Balcon'),
        ('other', 'Autre'),
    ]
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Propriété"
    )
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES,
        default='bedroom',
        verbose_name="Type de pièce"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la chambre"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Superficie (m²)"
    )
    floor_number = models.IntegerField(
        default=1,
        verbose_name="Étage"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Chambre"
        verbose_name_plural = "Chambres"
        ordering = ['order', 'floor_number', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.property.title}"


class PropertyImage(models.Model):
    """Modèle pour les images des propriétés"""
    
    IMAGE_TYPE_CHOICES = [
        ('normal', 'Photo normale'),
        ('panorama_360', 'Photo panoramique 360°'),
    ]
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Propriété"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        verbose_name="Chambre (optionnel)"
    )
    image = models.ImageField(
        upload_to='property_images/',
        verbose_name="Image"
    )
    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE_CHOICES,
        default='normal',
        verbose_name="Type d'image"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Image principale"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    
    class Meta:
        verbose_name = "Image de propriété"
        verbose_name_plural = "Images de propriétés"
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image de {self.property.title}"


class PropertyVideo(models.Model):
    """Modèle pour les vidéos des propriétés (walkthrough, visite)"""
    
    VIDEO_TYPE_CHOICES = [
        ('walkthrough', 'Visite guidée'),
        ('360_video', 'Vidéo 360°'),
    ]
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name="Propriété"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos',
        verbose_name="Chambre (optionnel)"
    )
    video = models.FileField(
        upload_to='property_videos/',
        verbose_name="Vidéo",
        help_text="Formats supportés: mp4, webm"
    )
    video_type = models.CharField(
        max_length=20,
        choices=VIDEO_TYPE_CHOICES,
        default='walkthrough',
        verbose_name="Type de vidéo"
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Titre"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    
    class Meta:
        verbose_name = "Vidéo de propriété"
        verbose_name_plural = "Vidéos de propriétés"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Vidéo de {self.property.title}"


class PropertySplat(models.Model):
    """
    Scène 3D Gaussian Splatting (immersion haute fidélité).
    Générée depuis une vidéo walkthrough, ou uploadée (.splat / .ply / .ksplat).
    """

    STATUS_CHOICES = [
        ('pending', 'En file'),
        ('processing', 'Reconstruction…'),
        ('ready', 'Prête'),
        ('failed', 'Échec'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='splats',
        verbose_name='Propriété',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='splats',
        verbose_name='Pièce',
    )
    source_video = models.ForeignKey(
        PropertyVideo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='splat_jobs',
        verbose_name='Vidéo source',
    )
    title = models.CharField(max_length=200, blank=True, verbose_name='Titre')
    splat_file = models.FileField(
        upload_to='property_splats/',
        blank=True,
        verbose_name='Fichier splat',
        help_text='Formats : .splat, .ply, .ksplat',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Statut',
    )
    error_message = models.TextField(blank=True, verbose_name='Erreur')
    frames_extracted = models.PositiveIntegerField(default=0, verbose_name='Images extraites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Scène 3D splat'
        verbose_name_plural = 'Scènes 3D splat'
        ordering = ['-created_at']

    def __str__(self):
        label = self.title or (self.room.name if self.room_id else 'Vue générale')
        return f"Splat — {self.property.title} — {label} ({self.status})"

    def ready_for_tour(self):
        return self.status == 'ready' and bool(self.splat_file)


class ARTour(models.Model):
    """Modèle pour les visites virtuelles en réalité augmentée"""
    
    property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name='ar_tour',
        null=True,
        blank=True,
        verbose_name="Propriété"
    )
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        related_name='ar_tour',
        null=True,
        blank=True,
        verbose_name="Chambre"
    )
    # URL ou fichier pour le modèle 3D ou la scène AR
    ar_scene_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL de la scène AR"
    )
    ar_model_file = models.FileField(
        upload_to='ar_models/',
        null=True,
        blank=True,
        verbose_name="Fichier modèle AR"
    )
    # QR Code pour l'accès rapide à la visite AR
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        null=True,
        blank=True,
        verbose_name="QR Code"
    )
    # Instructions pour la visite AR
    instructions = models.TextField(
        blank=True,
        verbose_name="Instructions de visite"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
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
        verbose_name = "Visite AR"
        verbose_name_plural = "Visites AR"
    
    def __str__(self):
        if self.room:
            return f"Visite AR - {self.room.name}"
        return f"Visite AR - {self.property.title}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.property and not self.room:
            raise ValidationError("Une visite AR doit être associée soit à une propriété, soit à une chambre.")
        if self.property and self.room:
            raise ValidationError("Une visite AR ne peut pas être associée à la fois à une propriété et à une chambre.")
