from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from accounts.models import User
from properties.models import Property


class Booking(models.Model):
    """Modèle pour les réservations de propriétés"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
    ]
    
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'user_type': 'tenant'},
        verbose_name="Locataire"
    )
    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Propriété"
    )
    start_date = models.DateField(
        verbose_name="Date de début"
    )
    end_date = models.DateField(
        verbose_name="Date de fin"
    )
    number_of_rooms = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Nombre de chambres"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix total (FCFA)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    message = models.TextField(
        blank=True,
        verbose_name="Message au propriétaire"
    )
    owner_response = models.TextField(
        blank=True,
        verbose_name="Réponse du propriétaire"
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
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Réservation {self.property_obj.title} par {self.tenant.username}"
    
    def save(self, *args, **kwargs):
        # Calculer le prix total si non fourni
        if not self.total_price and self.property_obj and self.number_of_rooms:
            days = (self.end_date - self.start_date).days
            if days > 0:
                self.total_price = self.property_obj.price_per_room * self.number_of_rooms * days
        super().save(*args, **kwargs)
    
    @property
    def duration_days(self):
        """Retourne la durée de la réservation en jours"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'


class Favorite(models.Model):
    """Modèle pour les propriétés favorites des locataires"""
    
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        limit_choices_to={'user_type': 'tenant'},
        verbose_name="Locataire"
    )
    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name="Propriété"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )
    
    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        unique_together = ['tenant', 'property_obj']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tenant.username} aime {self.property_obj.title}"
