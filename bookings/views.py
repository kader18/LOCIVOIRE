from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from properties.models import Property, ARTour, Room
from .models import Booking, Favorite
from .tour_utils import build_immersive_tour_data


def _get_property_or_redirect(request, property_id):
    """Évite le 404 brut quand la démo a été rechargée (IDs changés)."""
    property_obj = Property.objects.filter(pk=property_id).first()
    if property_obj:
        return property_obj
    messages.warning(
        request,
        "Ce bien n'existe plus (la démo a été rechargée). Voici les annonces actuelles.",
    )
    return None


@login_required
def create_booking(request, property_id):
    """Créer une réservation"""
    if not request.user.is_tenant:
        messages.error(request, 'Seuls les locataires peuvent effectuer des réservations.')
        return redirect('properties:property_list')
    
    property_obj = _get_property_or_redirect(request, property_id)
    if not property_obj:
        return redirect('properties:property_list')
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        number_of_rooms = int(request.POST.get('number_of_rooms', 1))
        message = request.POST.get('message', '')
        
        # Validation
        if not start_date or not end_date:
            messages.error(request, 'Veuillez remplir toutes les dates.')
            return redirect('properties:property_detail', pk=property_id)
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start >= end:
            messages.error(request, 'La date de fin doit être postérieure à la date de début.')
            return redirect('properties:property_detail', pk=property_id)
        
        if start < timezone.now().date():
            messages.error(request, 'La date de début ne peut pas être dans le passé.')
            return redirect('properties:property_detail', pk=property_id)
        
        if number_of_rooms > property_obj.number_of_rooms and not property_obj.is_entire_rental:
            messages.error(request, f'Le nombre de chambres demandé dépasse le nombre disponible ({property_obj.number_of_rooms}).')
            return redirect('properties:property_detail', pk=property_id)

        if property_obj.is_entire_rental:
            number_of_rooms = 1

        total_price = property_obj.compute_booking_price(start, end, number_of_rooms)

        # Créer la réservation
        booking = Booking.objects.create(
            tenant=request.user,
            property_obj=property_obj,
            start_date=start,
            end_date=end,
            number_of_rooms=number_of_rooms,
            total_price=total_price,
            message=message,
            status='pending'
        )

        if property_obj.is_monthly:
            messages.success(
                request,
                'Demande de location envoyée ! En attente de confirmation du propriétaire.',
            )
        else:
            messages.success(request, 'Réservation créée avec succès ! En attente de confirmation du propriétaire.')
        return redirect('bookings:booking_detail', pk=booking.pk)
    
    return redirect('properties:property_detail', pk=property_id)


@login_required
def booking_detail(request, pk):
    """Détails d'une réservation"""
    booking = get_object_or_404(
        Booking.objects.select_related('property_obj', 'tenant', 'property_obj__owner')
        .prefetch_related('property_obj__images'),
        pk=pk,
    )

    # Vérifier que l'utilisateur a le droit de voir cette réservation
    if not (request.user == booking.tenant or
            (request.user.is_owner and request.user == booking.property_obj.owner)):
        messages.error(request, 'Vous n\'avez pas accès à cette réservation.')
        return redirect('properties:property_list')

    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


@login_required
def booking_list(request):
    """Liste des réservations de l'utilisateur"""
    if request.user.is_owner:
        bookings = Booking.objects.filter(property_obj__owner=request.user)
    else:
        bookings = Booking.objects.filter(tenant=request.user)

    bookings = (
        bookings.select_related('property_obj', 'tenant')
        .prefetch_related('property_obj__images')
        .order_by('-created_at')
    )

    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings
    })


@login_required
def approve_booking(request, pk):
    """Approuver une réservation (propriétaire uniquement)"""
    if not request.user.is_owner:
        messages.error(request, 'Accès réservé aux propriétaires.')
        return redirect('properties:property_list')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.property_obj.owner != request.user:
        messages.error(request, 'Vous n\'avez pas le droit d\'approuver cette réservation.')
        return redirect('properties:property_list')
    
    if booking.status != 'pending':
        messages.error(request, 'Cette réservation ne peut plus être modifiée.')
        return redirect('bookings:booking_detail', pk=pk)
    
    booking.status = 'approved'
    booking.property_obj.status = 'pending'
    booking.property_obj.save()
    booking.save()
    
    messages.success(request, 'Réservation approuvée !')
    return redirect('bookings:booking_detail', pk=pk)


@login_required
def reject_booking(request, pk):
    """Rejeter une réservation (propriétaire uniquement)"""
    if not request.user.is_owner:
        messages.error(request, 'Accès réservé aux propriétaires.')
        return redirect('properties:property_list')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.property_obj.owner != request.user:
        messages.error(request, 'Vous n\'avez pas le droit de rejeter cette réservation.')
        return redirect('properties:property_list')
    
    if request.method == 'POST':
        owner_response = request.POST.get('owner_response', '')
        booking.status = 'rejected'
        booking.owner_response = owner_response
        booking.save()
        
        messages.info(request, 'Réservation rejetée.')
        return redirect('bookings:booking_detail', pk=pk)
    
    return redirect('bookings:booking_detail', pk=pk)


@login_required
def toggle_favorite(request, property_id):
    """Ajouter/Retirer une propriété des favoris"""
    if not request.user.is_tenant:
        messages.error(request, 'Seuls les locataires peuvent ajouter des favoris.')
        return redirect('properties:property_detail', pk=property_id)
    
    property_obj = _get_property_or_redirect(request, property_id)
    if not property_obj:
        return redirect('properties:property_list')
    favorite, created = Favorite.objects.get_or_create(
        tenant=request.user,
        property_obj=property_obj
    )
    
    if not created:
        favorite.delete()
        messages.info(request, 'Propriété retirée des favoris.')
    else:
        messages.success(request, 'Propriété ajoutée aux favoris !')
    
    return redirect('properties:property_detail', pk=property_id)


def _render_immersive_tour(request, property_obj, start_room_id=None):
    """Affiche la visite immersive basée sur les médias uploadés (sans casque VR)."""
    tour = build_immersive_tour_data(request, property_obj)
    if not tour['has_immersive_tour']:
        return None
    return render(request, 'bookings/immersive_tour.html', {
        'property': property_obj,
        'tour': tour,
        'start_room_id': start_room_id,
    })


def ar_tour_view(request, property_id):
    """Visite virtuelle immersive — photos/vidéos uploadées, sans casque VR."""
    property_obj = _get_property_or_redirect(request, property_id)
    if not property_obj:
        return redirect('properties:property_list')
    response = _render_immersive_tour(request, property_obj)
    if response:
        return response
    messages.info(request, 'Aucune visite immersive disponible. Le propriétaire doit ajouter des photos ou vidéos par pièce.')
    return redirect('properties:property_detail', pk=property_obj.pk)


def ar_tour_view_public(request, property_id):
    """Visite immersive publique (démo)."""
    property_obj = _get_property_or_redirect(request, property_id)
    if not property_obj:
        return redirect('properties:property_list')
    response = _render_immersive_tour(request, property_obj)
    if response:
        return response
    messages.info(request, 'Aucune visite immersive disponible pour cette propriété.')
    return redirect('properties:property_detail', pk=property_obj.pk)


def room_ar_tour(request, property_id, room_id):
    """Visite immersive d'une pièce spécifique."""
    property_obj = _get_property_or_redirect(request, property_id)
    if not property_obj:
        return redirect('properties:property_list')
    room = Room.objects.filter(pk=room_id, property=property_obj).first()
    if not room:
        messages.warning(request, "Cette pièce n'existe plus. Voici le bien.")
        return redirect('properties:property_detail', pk=property_obj.pk)
    tour = build_immersive_tour_data(request, property_obj)
    room_has_media = any(s['room_id'] == room.pk for s in tour['scenes'])
    if not room_has_media:
        messages.info(request, 'Aucun média immersif pour cette pièce. Ajoutez des photos 360° ou des photos.')
        return redirect('properties:room_detail', property_id=property_obj.pk, room_id=room.pk)
    return _render_immersive_tour(request, property_obj, start_room_id=room.pk)
