from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:property_id>/', views.create_booking, name='create_booking'),
    path('list/', views.booking_list, name='booking_list'),
    path('favorite/<int:property_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('ar-tour/<int:property_id>/', views.ar_tour_view, name='ar_tour'),
    path('ar-demo/<int:property_id>/', views.ar_tour_view_public, name='ar_demo'),  # Doit être avant <int:pk>/
    path('room-ar/<int:property_id>/<int:room_id>/', views.room_ar_tour, name='room_ar_tour'),
    path('<int:pk>/approve/', views.approve_booking, name='approve_booking'),
    path('<int:pk>/reject/', views.reject_booking, name='reject_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),  # En dernier pour éviter les conflits
]

