# Locivoire - Plateforme de Location de Maisons

Plateforme de location immobilière en **Côte d'Ivoire** avec :
- Prestataires (propriétaires) et locataires
- Carte des biens disponibles
- Visites immersives 360° (sans casque VR)

## Démarrage rapide (démo)

```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py load_demo_data --fresh
python manage.py runserver
```

→ http://127.0.0.1:8000/

**Comptes :** `soro/soro123` (prestataire) · `kader/kader123` (locataire)

Voir aussi [DEMO.md](DEMO.md) pour le parcours client.

## Fonctionnalités

- Deux profils : **Locataires** et **Prestataires / Propriétaires**
- Recherche (type, ville, prix) + chips quartiers Abidjan
- **Carte Leaflet** centrée sur la Côte d'Ivoire
- **Visite immersive** pièce par pièce (photos 360°)
- Réservations, favoris, gestion des médias

## Technologies

- Django 5+
- Bootstrap 5 + charte Locivoire (navy / or)
- Leaflet (cartes)
- Pannellum (visites 360°)

## Licence

Projet développé pour Locivoire.
