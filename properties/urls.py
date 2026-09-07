from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('ar-demo/', views.ar_demo_page, name='ar_demo_page'),  # Doit être avant <int:pk>/
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/add/', views.add_property, name='add_property'),
    path('owner/<int:property_id>/media/', views.manage_property_media, name='manage_property_media'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('<int:property_id>/rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('<int:pk>/', views.property_detail, name='property_detail'),  # En dernier pour éviter les conflits
]

