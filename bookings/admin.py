from django.contrib import admin
from .models import Booking, Favorite


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les réservations"""
    
    list_display = ['property_obj', 'tenant', 'start_date', 'end_date', 
                   'number_of_rooms', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'end_date', 'created_at']
    search_fields = ['property_obj__title', 'tenant__username', 'tenant__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de réservation', {
            'fields': ('tenant', 'property_obj', 'start_date', 'end_date', 'number_of_rooms', 'total_price')
        }),
        ('Statut', {
            'fields': ('status', 'message', 'owner_response')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property_obj', 'created_at']
    list_filter = ['created_at']
    search_fields = ['tenant__username', 'property_obj__title']
