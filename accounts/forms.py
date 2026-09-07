from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription pour les utilisateurs"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    phone = forms.CharField(
        max_length=17,
        required=False,
        label="Téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+225 XX XX XX XX XX'})
    )
    date_of_birth = forms.DateField(
        required=False,
        label="Date de naissance",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    place_of_birth = forms.CharField(
        max_length=100,
        required=False,
        label="Lieu de naissance",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville de naissance'})
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        required=True,
        label="Type de compte",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        label="Photo de profil",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    id_card_front = forms.ImageField(
        required=False,
        label="Pièce d'identité (recto)",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    id_card_back = forms.ImageField(
        required=False,
        label="Pièce d'identité (verso)",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 
                 'date_of_birth', 'place_of_birth', 'user_type', 'password1', 
                 'password2', 'profile_picture', 'id_card_front', 'id_card_back')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre les pièces d'identité obligatoires pour les propriétaires
        if self.data:
            user_type = self.data.get('user_type') or (self.initial.get('user_type') if hasattr(self, 'initial') else None)
            if user_type == 'owner':
                self.fields['id_card_front'].required = True
                self.fields['id_card_back'].required = True
    
    def clean_phone(self):
        """Nettoie le téléphone : supprime espaces et tirets pour validation"""
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return ''
        return ''.join(c for c in phone if c.isdigit() or c == '+')

