# 📋 CAHIER DES CHARGES - LOCIVOIRE

**Plateforme de Location de Maisons en Côte d'Ivoire**

---

## 📌 1. INFORMATIONS GÉNÉRALES

### 1.1. Présentation du Projet
**LOCIVOIRE** est une plateforme web moderne de location de maisons en Côte d'Ivoire, permettant de mettre en relation des propriétaires/promoteurs immobiliers avec des locataires potentiels. La plateforme se distingue par son intégration de visites virtuelles en réalité augmentée (AR) pour offrir une expérience immersive aux utilisateurs.

### 1.2. Objectifs du Projet
- Faciliter la recherche et la location de biens immobiliers en Côte d'Ivoire
- Permettre aux propriétaires de gérer efficacement leurs propriétés et réservations
- Offrir une expérience utilisateur moderne avec des fonctionnalités innovantes (AR)
- Sécuriser les transactions et vérifier l'identité des utilisateurs
- Centraliser la gestion des réservations et favoris

### 1.3. Contexte et Justification
- Besoin croissant de solutions numériques pour l'immobilier en Côte d'Ivoire
- Réduction des déplacements physiques grâce aux visites virtuelles
- Amélioration de la transparence et de la confiance entre parties
- Modernisation du secteur de la location immobilière

---

## 🎯 2. OBJECTIFS ET FONCTIONNALITÉS

### 2.1. Profils Utilisateurs

#### 2.1.1. Locataires
**Rôle** : Rechercher et réserver des propriétés

**Fonctionnalités principales** :
- Inscription et authentification
- Recherche avancée de propriétés (filtres par type, ville, prix)
- Consultation des détails des propriétés (photos, descriptions, localisation GPS)
- Visualisation des propriétés en réalité augmentée
- Réservation de propriétés avec sélection de dates et nombre de chambres
- Gestion des réservations (suivi du statut : en attente, approuvée, rejetée)
- Ajout de propriétés aux favoris
- Tableau de bord personnel avec toutes les réservations

**Données requises** :
- Nom d'utilisateur, email, mot de passe
- Numéro de téléphone (optionnel)
- Date et lieu de naissance (optionnel)
- Photo de profil (optionnel)

#### 2.1.2. Propriétaires/Promoteurs
**Rôle** : Gérer et proposer des propriétés à la location

**Fonctionnalités principales** :
- Inscription et authentification avec vérification d'identité
- Upload de pièces d'identité (recto et verso)
- Ajout de propriétés avec détails complets
- Upload de multiples photos par propriété
- Gestion des chambres/pièces de chaque propriété
- Configuration de visites AR pour les propriétés
- Gestion des réservations (approbation/rejet)
- Réponse aux demandes de réservation
- Tableau de bord avec statistiques des propriétés
- Mise en avant de propriétés (featured)

**Données requises** :
- Nom d'utilisateur, email, mot de passe
- Numéro de téléphone
- Pièce d'identité recto (obligatoire)
- Pièce d'identité verso (obligatoire)
- Vérification par l'administrateur

### 2.2. Gestion des Propriétés

#### 2.2.1. Informations d'une Propriété
- **Titre** : Nom descriptif de la propriété
- **Description** : Description détaillée
- **Type** : Maison, Appartement, Villa, Studio, Terrain
- **Adresse complète** : Adresse, ville, pays (Côte d'Ivoire par défaut)
- **Coordonnées GPS** : Latitude et longitude pour la localisation
- **Prix** : Prix par chambre en FCFA
- **Caractéristiques** :
  - Nombre de pièces
  - Nombre de chambres
  - Nombre de salles de bain
  - Superficie (m²)
- **Statut** : Disponible, Louée, En attente, Indisponible
- **Mise en avant** : Propriété vedette (featured)

#### 2.2.2. Gestion des Chambres/Pièces
Chaque propriété peut contenir plusieurs chambres/pièces :
- **Types de pièces** : Chambre, Salon, Cuisine, Salle de bain, Salle à manger, Bureau, Balcon, Autre
- **Nom de la pièce** : Identifiant unique
- **Description** : Détails spécifiques
- **Superficie** : En m²
- **Étage** : Numéro d'étage
- **Ordre d'affichage** : Pour l'organisation

#### 2.2.3. Gestion des Images
- Upload de multiples images par propriété
- Association d'images à des chambres spécifiques (optionnel)
- Image principale (primary) pour l'affichage dans les listes
- Galerie d'images pour chaque propriété

#### 2.2.4. Recherche et Filtres
- **Recherche textuelle** : Par titre, description, adresse, ville
- **Filtres** :
  - Type de propriété
  - Ville
  - Prix minimum
  - Prix maximum
- **Pagination** : 12 propriétés par page
- **Tri** : Par date de création (plus récentes en premier)

### 2.3. Système de Réservation

#### 2.3.1. Processus de Réservation
1. Le locataire sélectionne une propriété disponible
2. Sélection des dates de début et de fin
3. Choix du nombre de chambres à louer
4. Ajout d'un message optionnel au propriétaire
5. Calcul automatique du prix total (prix par chambre × nombre de chambres × nombre de jours)
6. Soumission de la demande de réservation
7. Statut initial : "En attente"

#### 2.3.2. Gestion par le Propriétaire
- Consultation des demandes de réservation
- Approbation ou rejet de la demande
- Ajout d'une réponse au locataire
- Modification du statut :
  - En attente
  - Approuvée
  - Rejetée
  - Annulée
  - Terminée

#### 2.3.3. Informations de Réservation
- Locataire
- Propriété concernée
- Dates de début et de fin
- Nombre de chambres
- Prix total calculé automatiquement
- Message du locataire
- Réponse du propriétaire
- Statut
- Dates de création et de mise à jour

### 2.4. Système de Favoris
- Les locataires peuvent ajouter des propriétés à leurs favoris
- Liste des favoris accessible depuis le tableau de bord
- Suppression de favoris
- Un locataire ne peut ajouter une propriété qu'une seule fois aux favoris

### 2.5. Visite Virtuelle en Réalité Augmentée (AR)

#### 2.5.1. Fonctionnalités AR
- **Visualisation 3D** : Affichage des propriétés en 3D dans l'environnement réel
- **Mode AR avec marqueur** : Utilisation d'un marqueur imprimable (Hiro pattern)
- **Mode AR sans marqueur** : Visualisation 360° immersive
- **Mode 3D interactif** : Exploration libre de la propriété
- **Contrôles interactifs** :
  - Activation/désactivation du mode AR
  - Réinitialisation de la vue
  - Rotation de la scène
  - Zoom avant/arrière

#### 2.5.2. Configuration AR
- Association d'une visite AR à une propriété ou à une chambre spécifique
- URL de scène AR ou fichier de modèle 3D
- Génération de QR code pour accès rapide
- Instructions de visite pour les utilisateurs
- Activation/désactivation de la visite AR

#### 2.5.3. Compatibilité
- **Navigateurs** : Chrome, Firefox, Safari, Edge
- **Appareils** : Smartphones iOS et Android, tablettes, ordinateurs avec webcam
- **Technologies** : AR.js, A-Frame

---

## 🛠️ 3. SPÉCIFICATIONS TECHNIQUES

### 3.1. Architecture Technique

#### 3.1.1. Backend
- **Framework** : Django 5.2.7
- **Langage** : Python 3.x
- **Base de données** : SQLite (développement) / PostgreSQL recommandé (production)
- **Serveur web** : WSGI (Django development server / Gunicorn en production)

#### 3.1.2. Frontend
- **Framework CSS** : Bootstrap 5.3
- **Icônes** : Font Awesome 6.4
- **JavaScript** : Vanilla JavaScript + AR.js + A-Frame
- **Templates** : Django Templates
- **Build tool** : Webpack (optionnel)

#### 3.1.3. Gestion des Fichiers
- **Images** : Pillow 12.0.0+
- **Upload** : Django FileField/ImageField
- **Stockage** : Système de fichiers local (développement) / Cloud Storage recommandé (production)

### 3.2. Structure de l'Application

```
locivoire/
├── accounts/          # Application de gestion des utilisateurs
│   ├── models.py      # Modèle User personnalisé
│   ├── views.py       # Vues d'authentification et profil
│   ├── forms.py       # Formulaires d'inscription/connexion
│   └── urls.py        # Routes d'authentification
│
├── properties/        # Application de gestion des propriétés
│   ├── models.py      # Modèles Property, Room, PropertyImage, ARTour
│   ├── views.py       # Vues de liste, détail, recherche
│   ├── admin.py       # Interface d'administration
│   └── urls.py        # Routes des propriétés
│
├── bookings/          # Application de gestion des réservations
│   ├── models.py      # Modèles Booking, Favorite
│   ├── views.py       # Vues de réservation et AR
│   └── urls.py        # Routes des réservations
│
├── templates/         # Templates HTML
│   ├── base.html      # Template de base
│   ├── accounts/      # Templates d'authentification
│   ├── properties/    # Templates des propriétés
│   └── bookings/      # Templates des réservations et AR
│
├── static/            # Fichiers statiques
│   ├── css/           # Feuilles de style
│   └── js/            # Scripts JavaScript
│
├── media/             # Fichiers uploadés par les utilisateurs
│
└── locivoire/         # Configuration principale Django
    ├── settings.py    # Paramètres de l'application
    └── urls.py        # URLs principales
```

### 3.3. Modèles de Données

#### 3.3.1. User (accounts)
- `username` : Nom d'utilisateur unique
- `email` : Adresse email
- `user_type` : 'owner' ou 'tenant'
- `phone` : Numéro de téléphone (format validé)
- `date_of_birth` : Date de naissance
- `place_of_birth` : Lieu de naissance
- `profile_picture` : Photo de profil
- `id_card_front` : Pièce d'identité recto (obligatoire pour propriétaires)
- `id_card_back` : Pièce d'identité verso (obligatoire pour propriétaires)
- `is_verified` : Statut de vérification
- `created_at`, `updated_at` : Timestamps

#### 3.3.2. Property (properties)
- `owner` : ForeignKey vers User (type='owner')
- `title` : Titre de la propriété
- `description` : Description détaillée
- `property_type` : Type (house, apartment, villa, studio, land)
- `address` : Adresse complète
- `city` : Ville
- `country` : Pays (défaut: "Côte d'Ivoire")
- `latitude`, `longitude` : Coordonnées GPS
- `price_per_room` : Prix par chambre en FCFA
- `number_of_rooms` : Nombre de pièces
- `number_of_bedrooms` : Nombre de chambres
- `number_of_bathrooms` : Nombre de salles de bain
- `area` : Superficie en m²
- `status` : Statut (available, rented, pending, unavailable)
- `is_featured` : Mise en avant
- `created_at`, `updated_at` : Timestamps

#### 3.3.3. Room (properties)
- `property` : ForeignKey vers Property
- `room_type` : Type de pièce (bedroom, living_room, kitchen, etc.)
- `name` : Nom de la chambre
- `description` : Description
- `area` : Superficie en m²
- `floor_number` : Numéro d'étage
- `order` : Ordre d'affichage
- `created_at` : Timestamp

#### 3.3.4. PropertyImage (properties)
- `property` : ForeignKey vers Property
- `room` : ForeignKey vers Room (optionnel)
- `image` : Fichier image
- `is_primary` : Image principale
- `uploaded_at` : Timestamp

#### 3.3.5. ARTour (properties)
- `property` : OneToOneField vers Property (optionnel)
- `room` : OneToOneField vers Room (optionnel)
- `ar_scene_url` : URL de la scène AR
- `ar_model_file` : Fichier modèle 3D
- `qr_code` : Image QR code
- `instructions` : Instructions de visite
- `is_active` : Statut actif
- `created_at`, `updated_at` : Timestamps

#### 3.3.6. Booking (bookings)
- `tenant` : ForeignKey vers User (type='tenant')
- `property_obj` : ForeignKey vers Property
- `start_date` : Date de début
- `end_date` : Date de fin
- `number_of_rooms` : Nombre de chambres
- `total_price` : Prix total calculé automatiquement
- `status` : Statut (pending, approved, rejected, cancelled, completed)
- `message` : Message du locataire
- `owner_response` : Réponse du propriétaire
- `created_at`, `updated_at` : Timestamps

#### 3.3.7. Favorite (bookings)
- `tenant` : ForeignKey vers User (type='tenant')
- `property_obj` : ForeignKey vers Property
- `created_at` : Timestamp
- Contrainte unique : Un locataire ne peut ajouter une propriété qu'une seule fois

### 3.4. Sécurité

#### 3.4.1. Authentification
- Système d'authentification Django intégré
- Validation des mots de passe (longueur minimale, complexité)
- Protection CSRF sur tous les formulaires
- Sessions sécurisées

#### 3.4.2. Autorisations
- Accès restreint selon le type d'utilisateur
- Propriétaires : Gestion de leurs propriétés uniquement
- Locataires : Réservation et favoris uniquement
- Vérification d'identité pour les propriétaires

#### 3.4.3. Validation des Données
- Validation des formulaires côté serveur
- Validation des formats (email, téléphone, dates)
- Validation des fichiers uploadés (images uniquement)
- Protection contre les injections SQL (ORM Django)

### 3.5. Performance

#### 3.5.1. Optimisations
- Pagination des listes de propriétés (12 par page)
- `select_related` pour optimiser les requêtes
- Compression des images (Pillow)
- Mise en cache recommandée pour la production

#### 3.5.2. Chargement des Fichiers
- Upload asynchrone des images
- Lazy loading des images dans les galeries
- Optimisation des images pour le web

---

## 📱 4. INTERFACE UTILISATEUR

### 4.1. Design et Expérience Utilisateur

#### 4.1.1. Principes de Design
- Interface moderne et responsive
- Design adaptatif (mobile-first)
- Navigation intuitive
- Feedback visuel pour toutes les actions
- Accessibilité (WCAG 2.1 niveau AA recommandé)

#### 4.1.2. Pages Principales

**Page d'accueil** :
- Liste des propriétés disponibles
- Barre de recherche et filtres
- Cartes de propriétés avec image principale, titre, prix, ville
- Pagination

**Page de détails d'une propriété** :
- Galerie d'images
- Informations complètes
- Carte Google Maps (si coordonnées GPS disponibles)
- Bouton de réservation
- Bouton d'ajout aux favoris
- Bouton de visite AR (si disponible)
- Liste des chambres/pièces

**Tableau de bord locataire** :
- Liste des réservations avec statut
- Liste des favoris
- Actions rapides

**Tableau de bord propriétaire** :
- Liste des propriétés
- Statistiques (nombre de réservations, revenus)
- Gestion des réservations
- Ajout/modification de propriétés

### 4.2. Responsive Design
- Mobile : Optimisé pour écrans 320px et plus
- Tablette : Optimisé pour écrans 768px et plus
- Desktop : Optimisé pour écrans 1024px et plus

---

## 🔒 5. SÉCURITÉ ET CONFIDENTIALITÉ

### 5.1. Protection des Données
- Chiffrement des mots de passe (hash Django)
- Protection des données personnelles
- Stockage sécurisé des pièces d'identité
- Accès restreint aux fichiers médias

### 5.2. Validation des Utilisateurs
- Vérification des propriétaires par l'administrateur
- Système de flags `is_verified`
- Validation des pièces d'identité

### 5.3. Conformité
- Respect du RGPD (si applicable)
- Protection des données personnelles
- Politique de confidentialité recommandée

---

## 🚀 6. DÉPLOIEMENT ET MAINTENANCE

### 6.1. Environnement de Développement
- Python 3.x
- Django 5.2.7
- Environnement virtuel (venv)
- Base de données SQLite pour le développement

### 6.2. Environnement de Production (Recommandations)
- Serveur web : Nginx + Gunicorn
- Base de données : PostgreSQL
- Stockage de fichiers : AWS S3 / Cloud Storage
- CDN pour les fichiers statiques
- SSL/HTTPS obligatoire
- Variables d'environnement pour les secrets

### 6.3. Maintenance
- Sauvegardes régulières de la base de données
- Monitoring des erreurs
- Mises à jour de sécurité
- Logs d'activité

---

## 📊 7. CRITÈRES D'ACCEPTATION

### 7.1. Fonctionnalités Obligatoires
- ✅ Inscription et authentification pour locataires et propriétaires
- ✅ Gestion complète des propriétés (CRUD)
- ✅ Recherche et filtres de propriétés
- ✅ Système de réservation avec calcul automatique
- ✅ Gestion des favoris
- ✅ Interface AR fonctionnelle
- ✅ Tableaux de bord pour chaque type d'utilisateur
- ✅ Upload et gestion d'images

### 7.2. Performance
- Temps de chargement des pages < 3 secondes
- Images optimisées pour le web
- Pagination efficace

### 7.3. Sécurité
- Protection CSRF active
- Validation des données côté serveur
- Authentification sécurisée
- Accès restreint selon les rôles

### 7.4. Compatibilité
- Compatibilité navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Responsive sur mobile, tablette et desktop
- Fonctionnement AR sur appareils compatibles

---

## 📅 8. PLANIFICATION ET PHASES

### Phase 1 : Développement Core (Terminée)
- Modèles de données
- Authentification
- Gestion des propriétés
- Recherche et filtres

### Phase 2 : Fonctionnalités Avancées (Terminée)
- Système de réservation
- Favoris
- Tableaux de bord

### Phase 3 : Réalité Augmentée (Terminée)
- Intégration AR.js
- Visites virtuelles
- Mode 360°

### Phase 4 : Améliorations Futures (À planifier)
- Notifications par email
- Système de paiement en ligne
- Chat entre locataires et propriétaires
- Système de notation et avis
- Application mobile native
- Intégration avec services de cartographie avancés

---

## 📝 9. DOCUMENTATION

### 9.1. Documentation Technique
- README.md avec instructions d'installation
- Documentation des modèles
- Guide de déploiement
- Guide de développement

### 9.2. Documentation Utilisateur
- Guide d'utilisation pour locataires
- Guide d'utilisation pour propriétaires
- FAQ
- Guide de la fonctionnalité AR

---

## 👥 10. ÉQUIPE ET CONTACTS

### 10.1. Rôles
- **Développeur** : Développement et maintenance
- **Administrateur** : Gestion des utilisateurs et vérifications
- **Support** : Assistance aux utilisateurs

---

## 📌 11. NOTES IMPORTANTES

### 11.1. Limitations Actuelles
- Base de données SQLite en développement (non recommandée pour production)
- Pas de système de paiement intégré
- Pas de notifications automatiques
- Pas de système de messagerie intégré

### 11.2. Recommandations pour la Production
- Migration vers PostgreSQL
- Implémentation d'un système de paiement
- Ajout de notifications (email/SMS)
- Mise en place d'un système de backup automatique
- Configuration HTTPS
- Monitoring et logging avancés
- Tests automatisés

---

## 📎 ANNEXES

### A. Glossaire
- **AR** : Augmented Reality (Réalité Augmentée)
- **CRUD** : Create, Read, Update, Delete
- **FCFA** : Franc de la Communauté Financière d'Afrique
- **GPS** : Global Positioning System
- **QR Code** : Quick Response Code

### B. Technologies et Bibliothèques
- Django 5.2.7
- Pillow 12.0.0+
- Bootstrap 5.3
- Font Awesome 6.4
- AR.js
- A-Frame

### C. Liens Utiles
- Documentation Django : https://docs.djangoproject.com/
- AR.js Documentation : https://ar-js-org.github.io/AR.js-Docs/
- Bootstrap Documentation : https://getbootstrap.com/docs/

---

**Document créé le** : [Date de création]  
**Version** : 1.0  
**Dernière mise à jour** : [Date de mise à jour]

---

*Ce cahier des charges est un document évolutif et peut être mis à jour selon les besoins du projet.*

