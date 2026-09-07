# Locivoire — Application mobile (Play Store & App Store)

Application native **identique** au site Locivoire, basée sur [Capacitor](https://capacitorjs.com/).  
Elle affiche la même interface Django (carte, visites immersives, admin, réservations, etc.) dans un conteneur Android / iOS.

## Mise à jour automatique = déjà liée au site

L’app charge votre site via `server.url` (WebView).  
**Chaque modification du site Django apparaît dans l’app** dès le prochain chargement / pull-to-refresh — **sans republier** sur le Play Store ni l’App Store.

| Ce qui se met à jour tout seul | Ce qui demande une nouvelle version store |
|--------------------------------|-------------------------------------------|
| Pages, CSS, JS, templates | Changer le nom / icône de l’app |
| Nouveaux biens, textes, menus | Changer le package ID |
| Connexion, admin, cartes, visites | Nouvelles permissions natives (caméra, etc.) |
| Bugs UI corrigés sur le site | Changer l’URL du serveur (ex. nouveau domaine) |

En résumé : vous développez **une seule fois** (le site), l’app mobile suit.

## Prérequis

| Plateforme | Outils |
|------------|--------|
| Les deux | Node.js 18+, npm |
| Android (APK / Play Store) | Android Studio, JDK 17, SDK 34 |
| iOS (App Store) | macOS + Xcode 15+ (obligatoire pour publier sur l’App Store) |

Serveur Locivoire (Django) accessible depuis le téléphone / émulateur.

## Configuration de l’URL du site

Fichier `capacitor.config.json` → clé `server.url` :

| Environnement | URL typique |
|---------------|-------------|
| Émulateur Android | `http://10.0.2.2:8000` (pointe vers localhost du PC) |
| Téléphone (même Wi‑Fi) | `http://192.168.x.x:8000` (IP de votre PC) |
| Production (stores) | `https://votredomaine.ci` |

Avant publication Play Store / App Store, mettez **uniquement** l’URL HTTPS de production et retirez `cleartext` si possible.

Côté Django (`locivoire/settings.py`) :

```python
ALLOWED_HOSTS = ['*', 'votredomaine.ci', '10.0.2.2', '192.168.x.x']
```

(En production, listez les hôtes explicitement.)

## Installation

```bash
cd APK
npm install
npm run build:web
npx cap add android
npx cap add ios
npm run sync
```

> `ios` ne s’ajoute correctement que sur un Mac.

## Lancer en développement

1. Démarrez Django : `python manage.py runserver 0.0.0.0:8000`
2. Ouvrez le projet natif :

```bash
npm run android   # Android Studio
npm run ios       # Xcode (Mac)
```

3. Lancez l’app depuis Android Studio / Xcode.

## Générer un APK (Android)

### Debug (test rapide)

```bash
npm run build:apk:debug
```

Fichier généré :

`APK/android/app/build/outputs/apk/debug/app-debug.apk`

### Release (Play Store)

1. Créez un keystore (une seule fois) :

```bash
keytool -genkey -v -keystore locivoire-release.keystore -alias locivoire -keyalg RSA -keysize 2048 -validity 10000
```

2. Configurez `android/key.properties` (ne pas committer) :

```
storePassword=***
keyPassword=***
keyAlias=locivoire
storeFile=../locivoire-release.keystore
```

3. Dans Android Studio : **Build → Generate Signed Bundle / APK**  
   - Play Store recommande un **AAB** (Android App Bundle)  
   - Ou APK release pour distribution directe

```bash
cd android
./gradlew bundleRelease
```

## Publier sur le Play Store

1. Compte [Google Play Console](https://play.google.com/console)
2. Créez l’application « Locivoire »
3. Remplissez fiche (description CI, captures, classification, confidentialité)
4. Uploadez le **AAB** release
5. Tests internes → production

Package ID : `ci.locivoire.app`

## Publier sur l’App Store

1. Compte Apple Developer
2. Sur Mac : `npm run ios` → Xcode
3. Signing & Capabilities (Team Apple)
4. Archive → Upload vers App Store Connect
5. Métadonnées, captures iPhone/iPad, review Apple

Bundle ID : `ci.locivoire.app`

## Identité visuelle

- Nom : **Locivoire**
- Couleurs : navy `#101A30` / or `#D9A441`
- Splash : écran Locivoire + drapeau CI (chargé au démarrage)

## Structure

```
APK/
  capacitor.config.json   # URL serveur + plugins
  package.json
  scripts/prepare-www.js  # Génère le splash local
  www/                    # Web locale (splash)
  android/                # Projet Android Studio (après cap add)
  ios/                    # Projet Xcode (après cap add, Mac)
  README.md
```

## Comptes démo (même backend)

| Rôle | Identifiants |
|------|----------------|
| Admin | `admin` / `admin123` |
| Prestataire | `soro` / `soro123` |
| Locataire | `kader` / `kader123` |

## Important

- Cette app est un **shell natif** autour du site Locivoire : toute évolution du site Django apparaît automatiquement dans l’app (pas besoin de republier pour chaque petit changement UI, sauf changement de domaine / permissions).
- Pour les stores, un **HTTPS public** est requis.
- Les permissions caméra / fichiers (upload pièces d’identité, photos biens) sont gérées via le WebView ; ajoutez les permissions Android/iOS si le store le demande (voir `AndroidManifest.xml` / `Info.plist`).
