from django.urls import path
from . import views
from . import staff_views

app_name = 'accounts'

urlpatterns = [
    path('select-profile/', views.profile_selection, name='profile_selection'),
    path('register/tenant/', views.register_tenant, name='register_tenant'),
    path('register/owner/', views.register_owner, name='register_owner'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('contact/', staff_views.contact, name='contact'),

    # Espace admin Locivoire
    path('staff/', staff_views.staff_dashboard, name='staff_dashboard'),
    path('staff/owners/', staff_views.staff_owners, name='staff_owners'),
    path('staff/owners/<int:user_id>/', staff_views.staff_owner_detail, name='staff_owner_detail'),
    path('staff/owners/<int:user_id>/approve/', staff_views.staff_owner_approve, name='staff_owner_approve'),
    path('staff/owners/<int:user_id>/reject/', staff_views.staff_owner_reject, name='staff_owner_reject'),
    path('staff/messages/', staff_views.staff_messages, name='staff_messages'),
    path('staff/messages/<int:pk>/', staff_views.staff_message_detail, name='staff_message_detail'),
]
