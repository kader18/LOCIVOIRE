from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ContactMessage


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User personnalisé"""

    list_display = ['username', 'email', 'user_type', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations personnelles', {
            'fields': (
                'user_type', 'phone', 'date_of_birth', 'place_of_birth',
                'profile_picture', 'id_card_front', 'id_card_back',
                'is_verified', 'verification_note',
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations personnelles', {
            'fields': ('user_type', 'email', 'phone', 'date_of_birth', 'place_of_birth')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
