from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bookings.models import Booking
from properties.models import Property

from .models import ContactMessage, User


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_platform_admin:
            messages.error(request, 'Accès réservé à l’équipe Locivoire.')
            return redirect('properties:property_list')
        return view_func(request, *args, **kwargs)
    return _wrapped


@staff_required
def staff_dashboard(request):
    pending_owners = (
        User.objects.filter(user_type='owner', is_verified=False, is_active=True)
        .order_by('-date_joined')
    )
    new_messages = ContactMessage.objects.filter(status='new')
    context = {
        'pending_owners': pending_owners[:8],
        'pending_owners_count': pending_owners.count(),
        'verified_owners_count': User.objects.filter(user_type='owner', is_verified=True).count(),
        'tenants_count': User.objects.filter(user_type='tenant').count(),
        'properties_count': Property.objects.count(),
        'bookings_pending': Booking.objects.filter(status='pending').count(),
        'messages_new_count': new_messages.count(),
        'recent_messages': ContactMessage.objects.all()[:6],
    }
    return render(request, 'accounts/staff_dashboard.html', context)


@staff_required
def staff_owners(request):
    tab = request.GET.get('tab', 'pending')
    qs = User.objects.filter(user_type='owner').order_by('-date_joined')
    if tab == 'pending':
        qs = qs.filter(is_verified=False, is_active=True)
    elif tab == 'verified':
        qs = qs.filter(is_verified=True)
    elif tab == 'rejected':
        qs = qs.filter(is_active=False)
    return render(request, 'accounts/staff_owners.html', {
        'owners': qs,
        'tab': tab,
        'pending_count': User.objects.filter(user_type='owner', is_verified=False, is_active=True).count(),
    })


@staff_required
def staff_owner_detail(request, user_id):
    owner = get_object_or_404(User, pk=user_id, user_type='owner')
    props = Property.objects.filter(owner=owner).order_by('-created_at')[:10]
    return render(request, 'accounts/staff_owner_detail.html', {
        'owner': owner,
        'properties': props,
    })


@staff_required
@require_POST
def staff_owner_approve(request, user_id):
    owner = get_object_or_404(User, pk=user_id, user_type='owner')
    owner.is_verified = True
    owner.is_active = True
    owner.verification_note = request.POST.get('note', '').strip() or 'Compte validé par l’admin Locivoire.'
    owner.save(update_fields=['is_verified', 'is_active', 'verification_note', 'updated_at'])
    messages.success(request, f'Prestataire « {owner.username} » validé.')
    return redirect('accounts:staff_owner_detail', user_id=owner.pk)


@staff_required
@require_POST
def staff_owner_reject(request, user_id):
    owner = get_object_or_404(User, pk=user_id, user_type='owner')
    note = request.POST.get('note', '').strip() or 'Compte refusé — pièces invalides ou incomplètes.'
    owner.is_verified = False
    owner.is_active = False
    owner.verification_note = note
    owner.save(update_fields=['is_verified', 'is_active', 'verification_note', 'updated_at'])
    messages.warning(request, f'Prestataire « {owner.username} » refusé / désactivé.')
    return redirect('accounts:staff_owners')


@staff_required
def staff_messages(request):
    tab = request.GET.get('tab', 'new')
    qs = ContactMessage.objects.all()
    if tab == 'new':
        qs = qs.filter(status='new')
    elif tab == 'open':
        qs = qs.filter(status__in=['new', 'read'])
    return render(request, 'accounts/staff_messages.html', {
        'items': qs,
        'tab': tab,
        'new_count': ContactMessage.objects.filter(status='new').count(),
    })


@staff_required
def staff_message_detail(request, pk):
    item = get_object_or_404(ContactMessage, pk=pk)
    if item.status == 'new':
        item.status = 'read'
        item.save(update_fields=['status', 'updated_at'])

    if request.method == 'POST':
        item.admin_note = request.POST.get('admin_note', '').strip()
        item.status = request.POST.get('status', item.status)
        item.save(update_fields=['admin_note', 'status', 'updated_at'])
        messages.success(request, 'Message mis à jour.')
        return redirect('accounts:staff_message_detail', pk=item.pk)

    return render(request, 'accounts/staff_message_detail.html', {'item': item})


def _safe_contact_next(raw_next):
    """Retourne une URL relative sûre vers le footer contact."""
    if not raw_next or not isinstance(raw_next, str):
        return '/#contact'
    next_url = raw_next.strip()
    if not next_url.startswith('/') or next_url.startswith('//'):
        return '/#contact'
    path = next_url.split('#')[0] or '/'
    return f'{path}#contact'


def contact(request):
    """Réception du formulaire contact (affiché dans le footer du site)."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        body = request.POST.get('message', '').strip()
        subject = (request.POST.get('subject', '') or 'Message depuis le site').strip()
        next_url = _safe_contact_next(request.POST.get('next'))

        if not (name and email and body):
            messages.error(request, 'Merci de remplir tous les champs obligatoires.')
        else:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=body,
                sender=request.user if request.user.is_authenticated else None,
            )
            messages.success(
                request,
                'Message envoyé. L’équipe Locivoire vous répondra rapidement.',
            )
        return redirect(next_url)

    return redirect('/#contact')
