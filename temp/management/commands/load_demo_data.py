"""
Charge un jeu de démonstration complet pour Locivoire.
Usage:
  python manage.py load_demo_data
  python manage.py load_demo_data --fresh
"""

from __future__ import annotations

import io
import math
import urllib.request
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from bookings.models import Booking, Favorite
from properties.models import Property, PropertyImage, Room

User = get_user_model()

# Photos façades / maisons
HOUSE_PHOTO_URLS = [
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&h=800&q=80",
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&h=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&h=800&q=80",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&h=800&q=80",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&h=800&q=80",
    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdbc?auto=format&fit=crop&w=1200&h=800&q=80",
]

# Vues d'ensemble d'intérieur (pièce entière visible, pas de gros plans)
INTERIOR_PHOTO_URLS = {
    "living_room": [
        "https://images.unsplash.com/photo-1600566752355-35792bedcfea?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "bedroom": [
        "https://images.unsplash.com/photo-1616594039961-1bdcc297e4e0?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1631679706909-184e58cdbb21?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "kitchen": [
        "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "bathroom": [
        "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "balcony": [
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdbc?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "dining_room": [
        "https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "garden": [
        "https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "corridor": [
        "https://images.unsplash.com/photo-1600607687644-c7171b42498f?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
    "general": [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&h=1000&q=80",
        "https://images.unsplash.com/photo-1600047509358-9dc75507daeb?auto=format&fit=crop&w=1600&h=1000&q=80",
    ],
}

# Villes CI (villes réelles) + quartiers d'Abidjan pour GPS
CITIES = {
    "Abidjan": (5.3600, -4.0083),
    "Bouaké": (7.6906, -5.0303),
    "Yamoussoukro": (6.8276, -5.2893),
    "San-Pédro": (4.7485, -6.6363),
    "Grand-Bassam": (5.2118, -3.7388),
    "Korhogo": (9.4580, -5.6296),
    "Daloa": (6.8774, -6.4502),
}

# Quartiers / communes d'Abidjan (pas des villes séparées)
ABIDJAN_AREAS = {
    "Cocody": (5.3600, -3.9880),
    "Yopougon": (5.3364, -4.0880),
    "Marcory": (5.2970, -3.9950),
    "Plateau": (5.3230, -4.0210),
    "Riviera": (5.3400, -3.9600),
    "Koumassi": (5.2880, -3.9550),
    "Treichville": (5.3020, -4.0060),
    "Abobo": (5.4200, -4.0200),
    "Adjamé": (5.3530, -4.0230),
    "Port-Bouët": (5.2560, -3.9240),
}


ROOMS_VILLA = [
    ("Salon principal", "living_room"),
    ("Salle à manger", "dining_room"),
    ("Cuisine équipée", "kitchen"),
    ("Couloir", "other"),
    ("Chambre parentale", "bedroom"),
    ("Chambre 2", "bedroom"),
    ("Salle de bain", "bathroom"),
    ("Balcon", "balcony"),
    ("Jardin", "other"),
]
ROOMS_HOUSE = [
    ("Salon", "living_room"),
    ("Cuisine", "kitchen"),
    ("Couloir", "other"),
    ("Chambre 1", "bedroom"),
    ("Chambre 2", "bedroom"),
    ("Salle de bain", "bathroom"),
    ("Cour / jardin", "other"),
]
ROOMS_APT = [
    ("Séjour", "living_room"),
    ("Cuisine", "kitchen"),
    ("Couloir", "other"),
    ("Chambre", "bedroom"),
    ("Salle de bain", "bathroom"),
    ("Balcon", "balcony"),
]
ROOMS_STUDIO = [
    ("Pièce principale", "living_room"),
    ("Coin cuisine", "kitchen"),
    ("Salle d'eau", "bathroom"),
    ("Balcon", "balcony"),
]


def make_cover(width, height, color, title, subtitle=""):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)
    try:
        font_lg = ImageFont.truetype("arial.ttf", 36)
        font_sm = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font_lg = ImageFont.load_default()
        font_sm = font_lg

    # Bandeau décoratif
    draw.rectangle([0, height - 70, width, height], fill=(27, 42, 74))
    draw.rectangle([0, 0, width, 8], fill=(217, 164, 65))

    tw = draw.textlength(title, font=font_lg) if hasattr(draw, "textlength") else len(title) * 18
    draw.text(((width - tw) / 2, height / 2 - 40), title, fill=(255, 255, 255), font=font_lg)
    if subtitle:
        sw = draw.textlength(subtitle, font=font_sm) if hasattr(draw, "textlength") else len(subtitle) * 10
        draw.text(((width - sw) / 2, height / 2 + 10), subtitle, fill=(217, 164, 65), font=font_sm)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    buf.seek(0)
    return buf


def make_panorama_fallback(label="Salon", theme="living"):
    """Génère un panorama intérieur 2:1 (pièce) — pas d'extérieur / montagnes."""
    from PIL import Image, ImageDraw, ImageFont

    themes = {
        "living": {"ceil": (245, 240, 232), "wall": (232, 220, 200), "floor": (139, 105, 20), "accent": (217, 164, 65)},
        "bedroom": {"ceil": (240, 245, 250), "wall": (210, 225, 235), "floor": (160, 130, 90), "accent": (100, 140, 180)},
        "kitchen": {"ceil": (250, 250, 248), "wall": (235, 235, 230), "floor": (180, 180, 175), "accent": (47, 111, 107)},
        "bathroom": {"ceil": (245, 250, 252), "wall": (220, 235, 240), "floor": (200, 210, 215), "accent": (70, 130, 140)},
        "balcony": {"ceil": (180, 210, 235), "wall": (200, 185, 160), "floor": (170, 150, 120), "accent": (217, 164, 65)},
        "general": {"ceil": (245, 240, 232), "wall": (225, 215, 195), "floor": (120, 90, 50), "accent": (217, 164, 65)},
    }
    c = themes.get(theme, themes["living"])

    w, h = 2048, 1024
    img = Image.new("RGB", (w, h))
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            t = y / h
            # Variation mur (fenêtres stylisées)
            window = abs((x % 512) - 256) < 80 and 0.32 < t < 0.55
            if t < 0.28:
                shade = int(8 * math.sin(x / 100.0))
                pixels[x, y] = (max(0, c["ceil"][0] + shade), max(0, c["ceil"][1] + shade), max(0, c["ceil"][2] + shade))
            elif t < 0.68:
                if window:
                    pixels[x, y] = (160, 195, 220)
                else:
                    shade = int(12 * math.sin(x / 70.0))
                    pixels[x, y] = (
                        min(255, max(0, c["wall"][0] + shade)),
                        min(255, max(0, c["wall"][1] + shade)),
                        min(255, max(0, c["wall"][2] + shade)),
                    )
        else:
                shade = int(10 * math.sin(x / 40.0))
                pixels[x, y] = (
                    min(255, max(0, c["floor"][0] + shade)),
                    min(255, max(0, c["floor"][1] + shade)),
                    min(255, max(0, c["floor"][2] + shade)),
                )

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 52)
        font_sm = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
        font_sm = font

    title = label
    subtitle = "Visite 360 — glissez la souris"
    tw = draw.textlength(title, font=font) if hasattr(draw, "textlength") else len(title) * 22
    draw.rounded_rectangle(
        [w / 2 - tw / 2 - 28, h / 2 - 50, w / 2 + tw / 2 + 28, h / 2 + 55],
        radius=12,
        fill=(27, 42, 74),
    )
    draw.text(((w - tw) / 2, h / 2 - 36), title, fill=c["accent"], font=font)
    sw = draw.textlength(subtitle, font=font_sm) if hasattr(draw, "textlength") else len(subtitle) * 12
    draw.text(((w - sw) / 2, h / 2 + 18), subtitle, fill=(230, 230, 230), font=font_sm)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    buf.seek(0)
    return buf


def make_sphere_from_photo(photo_bytes, label=""):
    """Compat : une seule photo → panorama multi-angles."""
    return make_sphere_from_photos([photo_bytes], label=label)


def make_sphere_from_photos(photos_bytes_list, label=""):
    """
    Construit un panorama 360° (2:1) avec plusieurs VRAIES photos autour.
    En tournant la souris, on voit d'autres angles nets — pas un flou.
    """
    from PIL import Image, ImageDraw, ImageFont, ImageOps

    w, h = 2048, 1024
    photos = []
    for raw in photos_bytes_list or []:
        try:
            photos.append(Image.open(io.BytesIO(raw)).convert("RGB"))
        except Exception:
            pass

    if not photos:
        return make_panorama_fallback(label or "Pièce", "general")

    # Au moins 4 secteurs pour un tour d'horizon complet
    while len(photos) < 4:
        photos.append(photos[len(photos) % len(photos_bytes_list) if photos_bytes_list else 0].copy())

    n = len(photos)
    sector_w = w // n
    canvas = Image.new("RGB", (w, h), (27, 42, 74))

    for i, photo in enumerate(photos):
        # Chaque photo remplit entièrement son secteur (nette, sans flou)
        fitted = ImageOps.fit(photo, (sector_w + 2, h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (i * sector_w, 0))

    # Léger fondu entre secteurs pour éviter une coupe trop dure
    try:
        from PIL import ImageEnhance
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for i in range(1, n):
            x = i * sector_w
            odraw.rectangle([x - 6, 0, x + 6, h], fill=(20, 30, 50, 40))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    except Exception:
        pass

    if label:
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", 26)
        except Exception:
            font = ImageFont.load_default()
        pad = 10
        tw = draw.textlength(label, font=font) if hasattr(draw, "textlength") else len(label) * 12
        draw.rectangle([12, 12, 12 + tw + pad * 2, 48], fill=(27, 42, 74))
        draw.text((12 + pad, 18), label, fill=(217, 164, 65), font=font)

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return buf


def fetch_bytes(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "LocivoireDemo/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


class Command(BaseCommand):
    help = "Charge des données de démo (prestataires, locataires, maisons GPS, visites 360°)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Supprime les données démo existantes avant de recharger",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== Locivoire - Chargement demo ===\n"))

        if options["fresh"]:
            self.wipe_demo()

        with transaction.atomic():
            owners, tenants = self.create_users()
            props = self.create_properties(owners)
            self.attach_media_and_tours(props)
            self.create_bookings(tenants, props)
            self.create_favorites(tenants, props)

        self.stdout.write(self.style.SUCCESS("\n[OK] Demo prete !"))
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Comptes de test :"))
        self.stdout.write("  Prestataire : soro / soro123")
        self.stdout.write("  Prestataire : jean / jean123")
        self.stdout.write("  Prestataire (a valider) : amine / amine123")
        self.stdout.write("  Locataire   : kader / kader123")
        self.stdout.write("  Locataire   : marie / marie123")
        self.stdout.write("  Admin       : admin / admin123")
        self.stdout.write("")
        self.stdout.write("Ouvrez http://127.0.0.1:8000/ puis :")
        self.stdout.write("  1) Explorez la carte CI")
        self.stdout.write("  2) Cliquez un bien -> Visite immersive")
        self.stdout.write("  3) Connectez-vous admin pour valider les prestataires")

    def wipe_demo(self):
        self.stdout.write("Nettoyage des donnees demo...")
        from accounts.models import ContactMessage
        Booking.objects.all().delete()
        Favorite.objects.all().delete()
        PropertyImage.objects.all().delete()
        Room.objects.all().delete()
        Property.objects.all().delete()
        ContactMessage.objects.all().delete()
        User.objects.filter(
            username__in=["soro", "jean", "kader", "marie", "admin", "amine"]
        ).delete()
        self.stdout.write(self.style.WARNING("  Donnees precedentes effacees."))

    def create_users(self):
        self.stdout.write("Utilisateurs (admin + prestataires + locataires)...")
        specs = [
            ("soro", "Soro", "Kouassi", "owner", "soro@locivoire.ci", "soro123", "+2250712345678"),
            ("jean", "Jean", "Yapi", "owner", "jean@locivoire.ci", "jean123", "+2250987654321"),
            ("amine", "Amine", "Traoré", "owner", "amine@locivoire.ci", "amine123", "+2250500112233"),
            ("kader", "Kader", "Diallo", "tenant", "kader@locivoire.ci", "kader123", "+2250598765432"),
            ("marie", "Marie", "Kouamé", "tenant", "marie@locivoire.ci", "marie123", "+2250123456789"),
        ]
        owners, tenants = [], []
        for username, first, last, utype, email, pwd, phone in specs:
            verified = utype == "owner" and username != "amine"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first,
                    "last_name": last,
                    "user_type": utype,
                    "phone": phone,
                    "is_verified": verified,
                    "date_of_birth": datetime(1990, 1, 1).date(),
                    "place_of_birth": "Abidjan",
                },
            )
            user.set_password(pwd)
            user.user_type = utype
            user.is_verified = verified
            user.is_active = True
            user.save()
            if utype == "owner" and verified:
                owners.append(user)
            elif utype == "tenant":
                tenants.append(user)
            mark = "+" if created else "~"
            label = "Prestataire" if utype == "owner" else "Locataire"
            extra = " [a valider]" if utype == "owner" and not verified else ""
            self.stdout.write(f"  [{mark}] {username} ({label}{extra})")

        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@locivoire.ci",
                "first_name": "Admin",
                "last_name": "Locivoire",
                "user_type": "admin",
                "phone": "+2250700000000",
                "is_verified": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("admin123")
        admin.user_type = "admin"
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_verified = True
        admin.save()
        self.stdout.write(f"  [{' +' if created else '~'}] admin (Administrateur)")

        from accounts.models import ContactMessage
        ContactMessage.objects.get_or_create(
            email="amine@locivoire.ci",
            subject="Validation de mon compte prestataire",
            defaults={
                "name": "Amine Traoré",
                "phone": "+2250500112233",
                "message": (
                    "Bonjour, j’ai créé un compte prestataire et déposé mes pièces. "
                    "Pouvez-vous valider mon compte pour que je puisse publier mes biens ? Merci."
                ),
                "status": "new",
                "sender": User.objects.filter(username="amine").first(),
            },
        )

        return owners, tenants

    def create_properties(self, owners):
        self.stdout.write("\nMaisons sur la carte CI...")
        soro, jean = owners[0], owners[1]

        catalog = [
            # —— Abidjan (quartiers dans l'adresse) ——
            {
                "title": "Villa standing — Cocody Ambassades",
                "owner": soro,
                "description": "Villa moderne 5 chambres à Cocody. Jardin, garage, sécurité 24/7. Visite immersive disponible.",
                "property_type": "villa",
                "rental_mode": "entire", "price_period": "month",
                "address": "Cocody · Rue des Ambassades",
                "city": "Abidjan",
                "lat": 5.3599, "lng": -3.9880,
                "price": 450000, "rooms": 10, "beds": 5, "baths": 3, "area": 350,
                "featured": True, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Villa piscine — Riviera Golf",
                "owner": jean,
                "description": "Villa de standing avec piscine privée et jardin tropical. Quartier Riviera, Abidjan.",
                "property_type": "villa",
                "rental_mode": "entire", "price_period": "month",
                "address": "Riviera · Boulevard de la République",
                "city": "Abidjan",
                "lat": 5.3400, "lng": -3.9600,
                "price": 550000, "rooms": 8, "beds": 4, "baths": 4, "area": 450,
                "featured": True, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Maison moderne — Yopougon Selmer",
                "owner": soro,
                "description": "Maison récente 3 chambres, cour arrière, proche transports. Yopougon, Abidjan.",
                "property_type": "house",
                "rental_mode": "entire", "price_period": "month",
                "address": "Yopougon · Boulevard de la Paix",
                "city": "Abidjan",
                "lat": 5.3364, "lng": -4.0880,
                "price": 180000, "rooms": 6, "beds": 3, "baths": 2, "area": 180,
                "featured": False, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Appartement cosy — Marcory Zone 4",
                "owner": soro,
                "description": "Appartement meublé en résidence sécurisée. Balcon, parking. Marcory, Abidjan.",
                "property_type": "apartment",
                "rental_mode": "entire", "price_period": "month",
                "address": "Marcory · Avenue Franchet d'Esperey",
                "city": "Abidjan",
                "lat": 5.2970, "lng": -3.9950,
                "price": 160000, "rooms": 4, "beds": 2, "baths": 1, "area": 95,
                "featured": True, "room_defs": ROOMS_APT,
            },
            {
                "title": "Résidence Les Palmiers — Plateau",
                "owner": jean,
                "description": "Résidence sécurisée avec gardiennage. Appartement F3 lumineux, proche des affaires. Location du logement complet.",
                "property_type": "residence",
                "rental_mode": "entire", "price_period": "month",
                "address": "Plateau · Avenue Clozel",
                "city": "Abidjan",
                "lat": 5.3230, "lng": -4.0210,
                "price": 220000, "rooms": 5, "beds": 3, "baths": 2, "area": 140,
                "featured": True, "room_defs": ROOMS_APT,
            },
            {
                "title": "Résidence étudiante — Cocody II Plateaux",
                "owner": soro,
                "description": "Chambres meublées en résidence étudiante, wifi et sécurité. Location à la chambre / mois.",
                "property_type": "residence",
                "rental_mode": "by_room", "price_period": "month",
                "address": "Cocody · II Plateaux Vallon",
                "city": "Abidjan",
                "lat": 5.3550, "lng": -3.9980,
                "price": 45000, "rooms": 12, "beds": 12, "baths": 6, "area": 600,
                "featured": True, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Résidence Riviera — nuitée",
                "owner": jean,
                "description": "Suite meublée en résidence standing à Riviera. Idéale pour séjours courts, ménage inclus. Tarif à la nuit.",
                "property_type": "residence",
                "rental_mode": "entire", "price_period": "night",
                "address": "Riviera · Near Golf",
                "city": "Abidjan",
                "lat": 5.3420, "lng": -3.9620,
                "price": 35000, "rooms": 3, "beds": 1, "baths": 1, "area": 55,
                "featured": True, "room_defs": ROOMS_STUDIO,
            },
            {
                "title": "Résidence Bassam — chambres / nuit",
                "owner": soro,
                "description": "Chambres climatisées en résidence à Grand-Bassam. Location à la chambre, à la nuit.",
                "property_type": "residence",
                "rental_mode": "by_room", "price_period": "night",
                "address": "Quartier France",
                "city": "Grand-Bassam",
                "lat": 5.2118, "lng": -3.7388,
                "price": 18000, "rooms": 8, "beds": 8, "baths": 4, "area": 320,
                "featured": True, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Résidence Yamoussoukro Centre",
                "owner": jean,
                "description": "Résidence calme près de la basilique. Logement complet meublé, parking.",
                "property_type": "residence",
                "rental_mode": "entire", "price_period": "month",
                "address": "Centre administratif",
                "city": "Yamoussoukro",
                "lat": 6.8276, "lng": -5.2893,
                "price": 95000, "rooms": 4, "beds": 2, "baths": 2, "area": 110,
                "featured": False, "room_defs": ROOMS_APT,
            },
            {
                "title": "Studio meublé — Plateau Centre",
                "owner": jean,
                "description": "Studio lumineux au Plateau. Fibre, clim, proche commerces. Abidjan.",
                "property_type": "studio",
                "address": "Plateau · Avenue Chardy",
                "city": "Abidjan",
                "lat": 5.3230, "lng": -4.0210,
                "price": 45000, "rooms": 1, "beds": 1, "baths": 1, "area": 35,
                "featured": False, "room_defs": ROOMS_STUDIO,
            },
            {
                "title": "Villa familiale — Koumassi Remblais",
                "owner": jean,
                "description": "Villa 4 chambres à Koumassi, cour spacieuse. Idéale grande famille.",
                "property_type": "villa",
                "address": "Koumassi · Quartier Remblais",
                "city": "Abidjan",
                "lat": 5.2920, "lng": -3.9480,
                "price": 85000, "rooms": 7, "beds": 4, "baths": 2, "area": 220,
                "featured": True, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Appartement neuf — Treichville",
                "owner": soro,
                "description": "Appartement neuf proche du port et des commerces. Treichville, Abidjan.",
                "property_type": "apartment",
                "address": "Treichville · Boulevard Valéry Giscard d'Estaing",
                "city": "Abidjan",
                "lat": 5.3045, "lng": -4.0020,
                "price": 55000, "rooms": 4, "beds": 2, "baths": 1, "area": 88,
                "featured": False, "room_defs": ROOMS_APT,
            },
            {
                "title": "Maison calme — Abobo Sogefiha",
                "owner": jean,
                "description": "Maison abordable à Abobo, quartier résidentiel. Bon rapport qualité-prix.",
                "property_type": "house",
                "address": "Abobo · Sogefiha",
                "city": "Abidjan",
                "lat": 5.4180, "lng": -4.0150,
                "price": 40000, "rooms": 5, "beds": 3, "baths": 1, "area": 140,
                "featured": False, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Duplex moderne — Adjamé Liberté",
                "owner": soro,
                "description": "Duplex lumineux à Adjamé, proche gare et marchés. Abidjan.",
                "property_type": "apartment",
                "address": "Adjamé · Quartier Liberté",
                "city": "Abidjan",
                "lat": 5.3510, "lng": -4.0260,
                "price": 65000, "rooms": 5, "beds": 3, "baths": 2, "area": 120,
                "featured": True, "room_defs": ROOMS_APT,
            },
            {
                "title": "Villa mer — Port-Bouët Vridi",
                "owner": jean,
                "description": "Villa proche de la plage à Port-Bouët. Brise marine, terrasse.",
                "property_type": "villa",
                "address": "Port-Bouët · Vridi Canal",
                "city": "Abidjan",
                "lat": 5.2480, "lng": -3.9600,
                "price": 110000, "rooms": 6, "beds": 3, "baths": 2, "area": 200,
                "featured": True, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Appartement Angré — Cocody",
                "owner": soro,
                "description": "Appartement 3 pièces à Angré. Résidence sécurisée, parking.",
                "property_type": "apartment",
                "address": "Cocody · Angré 8e Tranche",
                "city": "Abidjan",
                "lat": 5.3920, "lng": -3.9700,
                "price": 70000, "rooms": 4, "beds": 2, "baths": 2, "area": 110,
                "featured": False, "room_defs": ROOMS_APT,
            },
            {
                "title": "Maison 2 étages — Yopougon Sicogi",
                "owner": jean,
                "description": "Grande maison Sicogi à Yopougon. Cour, garage, 4 chambres.",
                "property_type": "house",
                "address": "Yopougon · Cité Sicogi",
                "city": "Abidjan",
                "lat": 5.3280, "lng": -4.1050,
                "price": 68000, "rooms": 7, "beds": 4, "baths": 2, "area": 190,
                "featured": False, "room_defs": ROOMS_HOUSE,
            },
            # —— Autres villes ——
            {
                "title": "Maison familiale — Bouaké Centre",
                "owner": jean,
                "description": "Maison spacieuse à Bouaké, quartier calme. Visite pièce par pièce.",
                "property_type": "house",
                "address": "Quartier Air France",
                "city": "Bouaké",
                "lat": 7.6906, "lng": -5.0303,
                "price": 55000, "rooms": 5, "beds": 3, "baths": 2, "area": 160,
                "featured": True, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Villa Ahougnansou — Bouaké",
                "owner": soro,
                "description": "Villa récente à Ahougnansou. Jardin, 3 chambres, sécurité.",
                "property_type": "villa",
                "address": "Ahougnansou",
                "city": "Bouaké",
                "lat": 7.7050, "lng": -5.0450,
                "price": 80000, "rooms": 6, "beds": 3, "baths": 2, "area": 210,
                "featured": False, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Villa administrative — Yamoussoukro",
                "owner": soro,
                "description": "Villa proche des institutions à Yamoussoukro. Grand terrain, 4 chambres.",
                "property_type": "villa",
                "address": "Quartier Habitat",
                "city": "Yamoussoukro",
                "lat": 6.8276, "lng": -5.2893,
                "price": 90000, "rooms": 7, "beds": 4, "baths": 3, "area": 280,
                "featured": False, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Maison vue mer — San-Pédro",
                "owner": jean,
                "description": "Maison aérée près du port de San-Pédro. Climat océanique, terrasse.",
                "property_type": "house",
                "address": "Quartier Balmer",
                "city": "San-Pédro",
                "lat": 4.7485, "lng": -6.6363,
                "price": 70000, "rooms": 5, "beds": 3, "baths": 2, "area": 170,
                "featured": True, "room_defs": ROOMS_HOUSE,
            },
            {
                "title": "Appartement colonial — Grand-Bassam",
                "owner": soro,
                "description": "Appartement dans le quartier historique de Grand-Bassam. Charme et authenticité.",
                "property_type": "apartment",
                "address": "Rue France",
                "city": "Grand-Bassam",
                "lat": 5.2118, "lng": -3.7388,
                "price": 50000, "rooms": 3, "beds": 2, "baths": 1, "area": 85,
                "featured": False, "room_defs": ROOMS_APT,
            },
            {
                "title": "Villa savane — Korhogo",
                "owner": jean,
                "description": "Villa spacieuse à Korhogo. Quartier résidentiel, climat sec du Nord.",
                "property_type": "villa",
                "address": "Quartier Résidentiel",
                "city": "Korhogo",
                "lat": 9.4580, "lng": -5.6296,
                "price": 60000, "rooms": 6, "beds": 3, "baths": 2, "area": 200,
                "featured": True, "room_defs": ROOMS_VILLA,
            },
            {
                "title": "Maison centre — Daloa",
                "owner": soro,
                "description": "Maison confortable au centre de Daloa. Proche marchés et écoles.",
                "property_type": "house",
                "address": "Centre-ville",
                "city": "Daloa",
                "lat": 6.8774, "lng": -6.4502,
                "price": 48000, "rooms": 5, "beds": 3, "baths": 1, "area": 150,
                "featured": False, "room_defs": ROOMS_HOUSE,
            },
        ]

        props = []
        for item in catalog:
            prop, created = Property.objects.update_or_create(
                title=item["title"],
                defaults={
                    "owner": item["owner"],
                    "description": item["description"],
                    "property_type": item["property_type"],
                    "rental_mode": item.get("rental_mode", "entire"),
                    "price_period": item.get("price_period", "month"),
                    "address": item["address"],
                    "city": item["city"],
                    "country": "Côte d'Ivoire",
                    "latitude": Decimal(str(item["lat"])),
                    "longitude": Decimal(str(item["lng"])),
                    "price_per_room": Decimal(str(item["price"])),
                    "number_of_rooms": item["rooms"],
                    "number_of_bedrooms": item["beds"],
                    "number_of_bathrooms": item["baths"],
                    "area": Decimal(str(item["area"])),
                    "status": "available",
                    "is_featured": item["featured"],
                },
            )
            prop.rooms.all().delete()
            for i, (name, rtype) in enumerate(item["room_defs"]):
                Room.objects.create(
                    property=prop,
                    name=name,
                    room_type=rtype,
                    description=f"Pièce {name} — visite immersive disponible",
                    area=Decimal("20.00") + i,
                    floor_number=1,
                    order=i,
                )
            props.append((prop, item["room_defs"]))
            self.stdout.write(f"  [{' +' if created else '~'}] {prop.title} ({prop.address}, {prop.city})")
        return props

    def attach_media_and_tours(self, props):
        self.stdout.write("\nMedias + visites immersives (vraies photos)...")

        house_buffers = []
        for url in HOUSE_PHOTO_URLS:
            try:
                house_buffers.append(io.BytesIO(fetch_bytes(url)))
            except Exception:
                pass
        if house_buffers:
            self.stdout.write(f"  [OK] {len(house_buffers)} photos facades telechargees")
        else:
            self.stdout.write(self.style.WARNING("  Facades indisponibles, placeholders utilises"))

        # Cache des photos d'intérieur par type de pièce
        interior_cache = {}
        for rtype, urls in INTERIOR_PHOTO_URLS.items():
            buffers = []
            for url in urls:
                try:
                    buffers.append(fetch_bytes(url))
                except Exception:
                    pass
            if buffers:
                interior_cache[rtype] = buffers
                self.stdout.write(f"  [OK] {len(buffers)} photos interieur ({rtype})")

        room_to_interior = {
            "living_room": "living_room",
            "bedroom": "bedroom",
            "kitchen": "kitchen",
            "bathroom": "bathroom",
            "balcony": "balcony",
            "dining_room": "dining_room",
            "office": "general",
            "other": "general",
        }

        def interior_key_for(room):
            name = (room.name or "").lower()
            if "terrasse" in name or "balcon" in name:
                return "balcony"
            if any(w in name for w in ("jardin", "cour")) or "piscine" in name:
                return "garden"
            if any(w in name for w in ("couloir", "corridor", "entrée", "entree")):
                return "corridor"
            return room_to_interior.get(room.room_type, "general")

        colors = [
            (27, 42, 74),
            (47, 111, 107),
            (185, 130, 42),
            (60, 80, 120),
            (90, 60, 50),
        ]

        for idx, (prop, room_defs) in enumerate(props):
            prop.images.all().delete()

            # 4 photos carrousel (façades)
            for a in range(4):
                if house_buffers:
                    src = house_buffers[(idx * 4 + a) % len(house_buffers)]
                    src.seek(0)
                    data = src.read()
                else:
                    data = make_cover(
                        900, 560, colors[(idx + a) % len(colors)],
                        prop.city, f"Vue {a + 1}"
                    ).read()
                pi = PropertyImage(
                    property=prop,
                    image_type="normal",
                    is_primary=(a == 0),
                )
                pi.image.save(f"house_{prop.pk}_{a}.jpg", ContentFile(data), save=True)

            rooms = list(prop.rooms.all().order_by("order"))
            for r_i, room in enumerate(rooms):
                ikey = interior_key_for(room)
                pool = interior_cache.get(ikey) or interior_cache.get("general") or []

                # 2–4 photos réelles de la pièce (angles différents)
                photo_bytes_list = []
                if pool:
                    for p in range(min(4, max(2, len(pool)))):
                        photo_bytes_list.append(pool[(idx + r_i + p) % len(pool)])
                else:
                    photo_bytes_list.append(
                        make_cover(700, 450, colors[(idx + r_i) % len(colors)], room.name, "Piece").read()
                    )

                for p_i, room_data in enumerate(photo_bytes_list):
                    photo = PropertyImage(
                        property=prop,
                        room=room,
                        image_type="normal",
                        is_primary=False,
                    )
                    photo.image.save(
                        f"room_{prop.pk}_{room.pk}_{p_i}.jpg",
                        ContentFile(room_data),
                        save=True,
                    )

                # Pas de faux panorama 360 (trop zoomé) — la visite utilise les photos nettes

            self.stdout.write(f"  [OK] Visite maison : {prop.title} ({len(rooms)} pieces)")

    def create_bookings(self, tenants, props):
        self.stdout.write("\nReservations de demo...")
        kader, marie = tenants[0], tenants[1]
        today = timezone.now().date()

        samples = [
            (kader, props[0][0], today + timedelta(days=7), today + timedelta(days=14), "pending", 2),
            (marie, props[3][0], today + timedelta(days=10), today + timedelta(days=20), "approved", 1),
            (kader, props[4][0], today + timedelta(days=3), today + timedelta(days=10), "pending", 1),
        ]
        for tenant, prop, start, end, status, nrooms in samples:
            if prop.is_entire_rental:
                nrooms = 1
            total = prop.compute_booking_price(start, end, nrooms)
            booking, created = Booking.objects.get_or_create(
                tenant=tenant,
                property_obj=prop,
                start_date=start,
                defaults={
                    "end_date": end,
                    "number_of_rooms": nrooms,
                    "total_price": total,
                    "status": status,
                    "message": "Demande de démo Locivoire — intéressé(e) par une visite.",
                },
            )
            if created:
                self.stdout.write(f"  [+] {tenant.username} → {prop.title} ({status})")

    def create_favorites(self, tenants, props):
        self.stdout.write("\nFavoris...")
        kader, marie = tenants[0], tenants[1]
        for tenant, prop in [(kader, props[0][0]), (kader, props[3][0]), (marie, props[5][0])]:
            Favorite.objects.get_or_create(tenant=tenant, property_obj=prop)
        self.stdout.write("  [OK] Favoris crees")
