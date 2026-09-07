from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm
from .models import User


def profile_selection(request):
    """Page de sélection du type de profil (Locataire ou Propriétaire)"""
    return render(request, 'accounts/profile_selection.html')


def register_tenant(request):
    """Inscription pour les locataires"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'tenant'
            user.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm(initial={'user_type': 'tenant'})
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'tenant',
        'title': 'Inscription Locataire'
    })


def register_owner(request):
    """Inscription pour les propriétaires"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'owner'
            user.save()
            messages.success(request, 'Inscription réussie ! Votre compte sera vérifié avant activation.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm(initial={'user_type': 'owner'})
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'owner',
        'title': 'Inscription Prestataire'
    })


def user_login(request):
    """Connexion utilisateur"""
    username = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            if user.is_platform_admin:
                return redirect('accounts:staff_dashboard')
            if user.is_owner:
                return redirect('properties:owner_dashboard')
            return redirect('properties:property_list')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'accounts/login.html', {'username': username})


def user_logout(request):
    """Déconnexion (accepte GET pour les liens du menu)"""
    logout(request)
    return redirect('properties:property_list')


@login_required
def profile(request):
    """Profil de l'utilisateur connecté"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
