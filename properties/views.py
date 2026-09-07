import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Property, PropertyImage, PropertyVideo, PropertySplat, ARTour, Room
from bookings.models import Booking, Favorite


DEFAULT_CITY_CHIPS = [
    'Abidjan', 'Bouaké', 'Yamoussoukro', 'San-Pédro',
    'Grand-Bassam', 'Korhogo', 'Daloa',
]

# Communes / quartiers d'Abidjan (filtre sur l'adresse)
ABIDJAN_QUARTIERS = {
    'cocody', 'yopougon', 'marcory', 'plateau', 'riviera', 'koumassi',
    'treichville', 'abobo', 'adjamé', 'adjame', 'port-bouët', 'port-bouet',
}


def property_list(request):
    """Liste des propriétés disponibles - Page d'accueil"""
    properties = Property.objects.filter(status='available').select_related('owner').prefetch_related('images')

    # Filtres de recherche
    search_query = request.GET.get('search', '')
    property_type = request.GET.get('property_type', '')
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    if property_type:
        properties = properties.filter(property_type=property_type)

    if city:
        city_key = city.strip().lower()
        if city_key in ABIDJAN_QUARTIERS:
            # Quartier abidjanais → filtre adresse / titre
            properties = properties.filter(
                Q(address__icontains=city) |
                Q(title__icontains=city) |
                Q(city__icontains=city)
            )
        else:
            properties = properties.filter(
                Q(city__icontains=city) | Q(address__icontains=city)
            )

    if min_price:
        try:
            properties = properties.filter(price_per_room__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            properties = properties.filter(price_per_room__lte=float(max_price))
        except ValueError:
            pass

    total_count = properties.count()

    city_stats = list(
        Property.objects.filter(status='available')
        .exclude(city='')
        .values('city')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    city_stats_tuples = [(row['city'], row['count']) for row in city_stats]

    db_cities = [c for c, _ in city_stats_tuples]
    city_chips = []
    for name in DEFAULT_CITY_CHIPS:
        if name not in city_chips:
            city_chips.append(name)
    for name in db_cities:
        if name not in city_chips:
            city_chips.append(name)
    city_chips = city_chips[:10]

    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Photos normales pour carrousel des cartes (hors panoramas 360)
    for prop in page_obj:
        normals = [img for img in prop.images.all() if img.image_type != 'panorama_360'][:8]
        if not normals:
            normals = list(prop.images.all()[:4])
        prop.card_images = normals

    # Markers pour la carte — URL visite 3D incluse
    map_qs = list(Property.objects.filter(status='available').select_related('owner')[:80])
    if city:
        city_key = city.strip().lower()
        if city_key in ABIDJAN_QUARTIERS:
            map_qs = [
                p for p in map_qs
                if city.lower() in (p.address or '').lower()
                or city.lower() in (p.title or '').lower()
                or city.lower() in (p.city or '').lower()
            ]
        else:
            map_qs = [
                p for p in map_qs
                if city.lower() in (p.city or '').lower()
                or city.lower() in (p.address or '').lower()
            ]
    map_markers = []
    for p in map_qs:
        map_markers.append({
            'id': p.pk,
            'title': p.title,
            'city': p.city,
            'address': p.address or '',
            'price': f'{p.price_per_room:,.0f}'.replace(',', ' '),
            'lat': float(p.latitude) if p.latitude is not None else None,
            'lng': float(p.longitude) if p.longitude is not None else None,
            'url': reverse('properties:property_detail', args=[p.pk]),
            'tour_url': reverse('bookings:ar_demo', args=[p.pk]),
            'rooms': p.number_of_rooms,
        })

    context = {
        'properties': page_obj,
        'search_query': search_query,
        'property_type': property_type,
        'city': city,
        'min_price': min_price,
        'max_price': max_price,
        'PROPERTY_TYPES': Property.PROPERTY_TYPE_CHOICES,
        'total_count': total_count,
        'city_stats': city_stats_tuples,
        'city_chips': city_chips,
        'map_markers_json': json.dumps(map_markers, ensure_ascii=False),
    }

    return render(request, 'properties/property_list_modern.html', context)


def property_detail(request, pk):
    """Détails d'une propriété"""
    property_obj = Property.objects.filter(pk=pk).first()
    if not property_obj:
        messages.warning(
            request,
            "Ce bien n'existe plus (la démo a été rechargée). Voici les annonces actuelles.",
        )
        return redirect('properties:property_list')
    images = property_obj.images.all()
    # Galerie : photos normales seulement (pas les panoramas 360)
    gallery_images = list(
        images.filter(image_type='normal').order_by('-is_primary', 'id')
    )
    if not gallery_images:
        gallery_images = list(images.exclude(image_type='panorama_360').order_by('-is_primary', 'id'))
    primary_image = gallery_images[0] if gallery_images else images.filter(is_primary=True).first()
    other_images = gallery_images[1:] if len(gallery_images) > 1 else []
    
    # Récupérer les chambres de la propriété
    rooms = property_obj.rooms.prefetch_related('images').all()
    
    # Vérifier si l'utilisateur a déjà cette propriété en favoris
    is_favorite = False
    if request.user.is_authenticated and request.user.is_tenant:
        is_favorite = Favorite.objects.filter(
            tenant=request.user,
            property_obj=property_obj
        ).exists()
    
    # Vérifier si une visite AR existe ou si des médias immersifs sont disponibles
    ar_tour = None
    try:
        ar_tour = property_obj.ar_tour
        if not ar_tour.is_active:
            ar_tour = None
    except ARTour.DoesNotExist:
        pass
    
    has_immersive_media = (
        property_obj.images.exists() or
        property_obj.videos.exists()
    )
    
    context = {
        'property': property_obj,
        'primary_image': primary_image,
        'other_images': other_images,
        'gallery_images': gallery_images,
        'is_favorite': is_favorite,
        'ar_tour': ar_tour,
        'rooms': rooms,
        'has_immersive_media': has_immersive_media,
    }
    
    return render(request, 'properties/property_detail.html', context)


def room_detail(request, property_id, room_id):
    """Détails d'une chambre avec visite AR"""
    property_obj = Property.objects.filter(pk=property_id).first()
    if not property_obj:
        messages.warning(
            request,
            "Ce bien n'existe plus (la démo a été rechargée). Voici les annonces actuelles.",
        )
        return redirect('properties:property_list')

    room = Room.objects.filter(pk=room_id, property=property_obj).first()
    if not room:
        messages.warning(request, "Cette pièce n'existe plus. Voici le bien.")
        return redirect('properties:property_detail', pk=property_obj.pk)
    
    # Récupérer les images de la chambre
    room_images = room.images.all()
    
    has_room_tour = room.images.exists() or room.videos.exists()
    
    context = {
        'property': property_obj,
        'room': room,
        'room_images': room_images,
        'has_room_tour': has_room_tour,
    }
    
    return render(request, 'properties/room_detail.html', context)


@login_required
def owner_dashboard(request):
    """Tableau de bord du propriétaire"""
    if not request.user.is_owner:
        messages.error(request, 'Accès réservé aux propriétaires.')
        return redirect('properties:property_list')
    
    properties = (
        Property.objects.filter(owner=request.user)
        .prefetch_related('images', 'rooms')
        .annotate(media_count=Count('images', distinct=True))
        .order_by('-created_at')
    )
    bookings = (
        Booking.objects.filter(property_obj__owner=request.user)
        .select_related('tenant', 'property_obj')
        .order_by('-created_at')[:10]
    )
    total_bookings = Booking.objects.filter(property_obj__owner=request.user).count()
    immersive_ready = properties.filter(media_count__gt=0).count()
    props_needing_media = max(properties.count() - immersive_ready, 0)

    context = {
        'properties': properties,
        'bookings': bookings,
        'total_properties': properties.count(),
        'available_properties': properties.filter(status='available').count(),
        'pending_bookings': Booking.objects.filter(
            property_obj__owner=request.user,
            status='pending'
        ).count(),
        'total_bookings': total_bookings,
        'immersive_ready': immersive_ready,
        'props_needing_media': props_needing_media,
    }

    return render(request, 'properties/owner_dashboard.html', context)


@login_required
def add_property(request):
    """Ajouter une nouvelle propriété"""
    if not request.user.is_owner:
        messages.error(request, 'Accès réservé aux propriétaires.')
        return redirect('properties:property_list')

    if not request.user.is_verified:
        messages.warning(
            request,
            'Votre compte prestataire doit d’abord être validé par l’admin Locivoire '
            'avant de publier un bien. Contactez l’équipe si besoin.',
        )
        return redirect('properties:owner_dashboard')
    
    if request.method == 'POST':
        # Créer la propriété
        property_obj = Property.objects.create(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            property_type=request.POST.get('property_type'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country', "Côte d'Ivoire"),
            latitude=request.POST.get('latitude') or None,
            longitude=request.POST.get('longitude') or None,
            price_per_room=request.POST.get('price_per_room'),
            number_of_rooms=request.POST.get('number_of_rooms'),
            number_of_bedrooms=request.POST.get('number_of_bedrooms'),
            number_of_bathrooms=request.POST.get('number_of_bathrooms', 1),
            area=request.POST.get('area') or None,
            status='available',
            is_featured=request.POST.get('is_featured') == 'on',
        )
        
        # Gérer les images normales
        images = request.FILES.getlist('images')
        for idx, image in enumerate(images):
            PropertyImage.objects.create(
                property=property_obj,
                image=image,
                image_type='normal',
                is_primary=(idx == 0)
            )
        
        # Gérer les photos panoramiques 360°
        images_360 = request.FILES.getlist('images_360')
        for image in images_360:
            PropertyImage.objects.create(
                property=property_obj,
                image=image,
                image_type='panorama_360',
                is_primary=False
            )
        
        # Gérer la vidéo
        video_file = request.FILES.get('video')
        if video_file:
            PropertyVideo.objects.create(
                property=property_obj,
                video=video_file,
                video_type='walkthrough',
                title='Visite guidée'
            )
        
        messages.success(request, 'Propriété ajoutée avec succès !')
        return redirect('properties:property_detail', pk=property_obj.pk)
    
    return render(request, 'properties/add_property.html', {
        'PROPERTY_TYPES': Property.PROPERTY_TYPE_CHOICES,
    })


@login_required
def manage_property_media(request, property_id):
    """Gestion des médias (photos, photos 360, vidéos) par pièce"""
    property_obj = get_object_or_404(Property, pk=property_id, owner=request.user)
    rooms = property_obj.rooms.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'upload_image':
            image_file = request.FILES.get('image')
            image_type = request.POST.get('image_type', 'normal')
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, pk=room_id, property=property_obj) if room_id else None
            if image_file:
                PropertyImage.objects.create(
                    property=property_obj,
                    room=room,
                    image=image_file,
                    image_type=image_type,
                    is_primary=False
                )
                messages.success(request, 'Photo ajoutée.')
        
        elif action == 'upload_video':
            video_file = request.FILES.get('video')
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, pk=room_id, property=property_obj) if room_id else None
            if video_file:
                PropertyVideo.objects.create(
                    property=property_obj,
                    room=room,
                    video=video_file,
                    video_type='walkthrough',
                    title=request.POST.get('title', 'Visite')
                )
                messages.success(request, 'Vidéo ajoutée.')

        elif action == 'upload_splat':
            splat_file = request.FILES.get('splat_file')
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, pk=room_id, property=property_obj) if room_id else None
            if splat_file:
                name = (splat_file.name or '').lower()
                if not name.endswith(('.splat', '.ply', '.ksplat')):
                    messages.error(request, 'Formats acceptés : .splat, .ply, .ksplat')
                else:
                    PropertySplat.objects.create(
                        property=property_obj,
                        room=room,
                        title=request.POST.get('title', '') or 'Scène 3D',
                        splat_file=splat_file,
                        status='ready',
                    )
                    messages.success(request, 'Scène 3D splat ajoutée — visible dans la visite.')

        elif action == 'queue_splat_from_video':
            video_id = request.POST.get('video_id')
            video = get_object_or_404(PropertyVideo, pk=video_id, property=property_obj)
            job = PropertySplat.objects.create(
                property=property_obj,
                room=video.room,
                source_video=video,
                title=video.title or 'Reconstruction 3D',
                status='pending',
            )
            # Tentative immédiate (sinon : python manage.py process_splat_jobs)
            try:
                from properties.splat_pipeline import process_splat_job
                process_splat_job(job)
                job.refresh_from_db()
                if job.status == 'ready':
                    messages.success(request, 'Reconstruction 3D terminée.')
                else:
                    messages.warning(
                        request,
                        'Job mis en file. Lancez : python manage.py process_splat_jobs '
                        f'(#{job.pk}). Sans worker GPU, uploadez un .splat/.ply.',
                    )
            except Exception as exc:
                messages.warning(request, f'Reconstruction différée : {exc}')

        elif action == 'delete_splat':
            splat_id = request.POST.get('splat_id')
            PropertySplat.objects.filter(pk=splat_id, property=property_obj).delete()
            messages.success(request, 'Scène 3D supprimée.')

        elif action == 'delete_image':
            img_id = request.POST.get('image_id')
            PropertyImage.objects.filter(pk=img_id, property=property_obj).delete()
            messages.success(request, 'Photo supprimée.')
        
        elif action == 'delete_video':
            vid_id = request.POST.get('video_id')
            PropertyVideo.objects.filter(pk=vid_id, property=property_obj).delete()
            messages.success(request, 'Vidéo supprimée.')
        
        elif action == 'set_room':
            img_id = request.POST.get('image_id')
            room_id = request.POST.get('room') or None
            room = get_object_or_404(Room, pk=room_id, property=property_obj) if room_id else None
            PropertyImage.objects.filter(pk=img_id, property=property_obj).update(room=room)
            messages.success(request, 'Pièce mise à jour.')
        
        return redirect('properties:manage_property_media', property_id=property_id)
    
    images = property_obj.images.all().select_related('room')
    videos = property_obj.videos.all().select_related('room')
    splats = property_obj.splats.all().select_related('room', 'source_video')

    context = {
        'property': property_obj,
        'rooms': rooms,
        'images': images,
        'videos': videos,
        'splats': splats,
    }
    return render(request, 'properties/manage_media.html', context)


@login_required
def tenant_dashboard(request):
    """Tableau de bord du locataire"""
    if not request.user.is_tenant:
        messages.error(request, 'Accès réservé aux locataires.')
        return redirect('properties:property_list')
    
    bookings = Booking.objects.filter(tenant=request.user).order_by('-created_at')
    favorites = Favorite.objects.filter(tenant=request.user).select_related('property_obj')
    
    context = {
        'bookings': bookings,
        'favorites': favorites,
    }
    
    return render(request, 'properties/tenant_dashboard.html', context)


def ar_demo_page(request):
    """Page de démonstration des visites immersives"""
    from django.db.models import Q

    properties_with_media = Property.objects.filter(
        status='available'
    ).filter(
        Q(images__isnull=False) | Q(videos__isnull=False)
    ).distinct()[:6]

    if properties_with_media.count() < 3:
        other = Property.objects.filter(status='available').exclude(
            pk__in=properties_with_media.values_list('pk', flat=True)
        )[:3 - properties_with_media.count()]
        properties = list(properties_with_media) + list(other)
    else:
        properties = properties_with_media

    return render(request, 'properties/ar_demo_page.html', {
        'properties': properties
    })
