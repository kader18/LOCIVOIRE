from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo, PropertySplat, ARTour, Room


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('name', 'room_type', 'description', 'area', 'floor_number', 'order')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'owner', 'property_type', 'rental_mode', 'price_period',
        'city', 'price_per_room', 'number_of_rooms', 'status', 'is_featured', 'created_at',
    ]
    list_filter = ['property_type', 'rental_mode', 'price_period', 'status', 'is_featured', 'city', 'created_at']
    search_fields = ['title', 'description', 'address', 'city', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PropertyImageInline, RoomInline]

    fieldsets = (
        ('Informations générales', {
            'fields': ('owner', 'title', 'description', 'property_type', 'status', 'is_featured'),
        }),
        ('Location', {
            'fields': ('rental_mode', 'price_period', 'price_per_room'),
        }),
        ('Localisation', {
            'fields': ('address', 'city', 'country', 'latitude', 'longitude'),
        }),
        ('Caractéristiques', {
            'fields': (
                'number_of_rooms', 'number_of_bedrooms', 'number_of_bathrooms',
                'area',
            ),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'property', 'room_type', 'floor_number', 'area', 'order']
    list_filter = ['room_type', 'floor_number', 'property']
    search_fields = ['name', 'description', 'property__title']
    ordering = ['property', 'order', 'floor_number', 'name']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'room', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at', 'room']


@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ['property', 'room', 'title', 'video_type', 'uploaded_at']
    list_filter = ['video_type', 'uploaded_at']


@admin.register(PropertySplat)
class PropertySplatAdmin(admin.ModelAdmin):
    list_display = ['property', 'room', 'status', 'frames_extracted', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['property__title', 'title', 'error_message']
    readonly_fields = ['created_at', 'updated_at', 'frames_extracted']


@admin.register(ARTour)
class ARTourAdmin(admin.ModelAdmin):
    list_display = ['property', 'room', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('property', 'room')
