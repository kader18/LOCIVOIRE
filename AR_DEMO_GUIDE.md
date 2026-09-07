# 🎯 Guide de la Démo AR - Locivoire

## ✨ Fonctionnalités AR Disponibles

### 1. **Modèles 3D Intégrés**
- ✅ Maison 3D complète avec :
  - Structure principale (bleu)
  - Toit (rouge)
  - Porte (marron)
  - Fenêtres (bleu ciel)
  - Cheminée (gris)
  - Informations flottantes (titre, prix, caractéristiques)

### 2. **Deux Modes de Visualisation**

#### Mode AR avec Marqueur
- Utilise le marqueur Hiro (pattern recognition)
- Plus précis et stable
- Téléchargez et imprimez le marqueur
- Placez-le sur une surface plane
- Pointez votre caméra vers le marqueur

#### Mode 360° Sans Marqueur
- Visualisation immersive
- Explorez la maison en 3D
- Navigation avec souris/doigts
- Pas besoin de marqueur

### 3. **Contrôles Interactifs**
- **Mode AR** : Active/désactive le mode AR
- **Réinitialiser** : Remet la vue à zéro
- **Rotation** : Fait pivoter la maison
- **Zoomer** : Approche la caméra
- **Dézoomer** : Éloigne la caméra

## 🚀 Comment Tester

### Option 1 : Via la Navigation
1. Cliquez sur **"Démo AR"** dans le menu
2. Choisissez une propriété
3. Cliquez sur **"Voir en AR"**

### Option 2 : Via une Propriété
1. Allez sur la page d'une propriété
2. Cliquez sur **"Visite virtuelle AR"**
3. La démo AR s'ouvre automatiquement

### Option 3 : URL Directe
```
http://127.0.0.1:8000/bookings/ar-demo/[ID_PROPRIETE]/
```

## 📱 Sur Mobile

1. **Ouvrez la page AR** sur votre smartphone
2. **Autorisez l'accès à la caméra**
3. **Pour le mode avec marqueur** :
   - Téléchargez le marqueur Hiro
   - Imprimez-le sur une feuille A4
   - Placez-le sur une table
   - Pointez votre caméra vers le marqueur
4. **Pour le mode sans marqueur** :
   - Pointez vers un espace ouvert
   - La maison apparaît en 3D

## 💻 Sur Desktop

1. **Ouvrez la page AR** dans votre navigateur
2. **Autorisez l'accès à la webcam**
3. **Explorez en mode 360°** :
   - Utilisez la souris pour regarder autour
   - Cliquez et glissez pour pivoter
   - Utilisez la molette pour zoomer
4. **Mode avec marqueur** :
   - Téléchargez et imprimez le marqueur
   - Tenez-le devant la caméra

## 🎨 Caractéristiques Visuelles

### Modèle 3D de la Maison
- **Structure** : Cube bleu (#4CC3D9)
- **Toit** : Cône rouge (#EF2D5E)
- **Porte** : Marron (#8B4513)
- **Fenêtres** : Bleu ciel (#87CEEB)
- **Cheminée** : Gris (#696969)
- **Animation** : Rotation automatique de 360°

### Informations Flottantes
- Titre de la propriété
- Prix par chambre
- Nombre de pièces et ville
- Affichage en 3D dans l'espace AR

### Environnement
- **Ciel** : Bleu ciel (#87CEEB)
- **Sol** : Vert (#90EE90) avec pattern
- **Éclairage** : Ambiant + Directionnel + Point

## 🔧 Technologies Utilisées

- **AR.js 3.4.2** : Bibliothèque AR web
- **A-Frame 1.4.0** : Framework 3D/VR
- **Marqueur Hiro** : Pattern recognition standard
- **WebRTC** : Accès à la caméra

## 📋 Checklist de Test

- [ ] Ouvrir la page de démo AR
- [ ] Autoriser l'accès à la caméra
- [ ] Voir la maison en 3D (mode sans marqueur)
- [ ] Télécharger le marqueur Hiro
- [ ] Tester avec le marqueur (mode AR)
- [ ] Utiliser les contrôles (zoom, rotation)
- [ ] Tester sur mobile
- [ ] Tester sur desktop

## 🐛 Dépannage

### La caméra ne s'active pas
- Vérifiez les permissions du navigateur
- Utilisez HTTPS (localhost fonctionne)
- Essayez un autre navigateur (Chrome recommandé)

### Le modèle ne s'affiche pas
- Vérifiez la console du navigateur (F12)
- Assurez-vous que AR.js est chargé
- Videz le cache du navigateur

### Le marqueur n'est pas détecté
- Imprimez le marqueur en haute qualité
- Assurez-vous d'avoir une bonne lumière
- Tenez le marqueur à plat
- Évitez les reflets

## 🎯 Exemples de Propriétés avec AR

Les propriétés suivantes ont des visites AR actives :
1. **Villa 10 pièces - Cocody** (ID: 1)
2. **Maison moderne 6 pièces - Yopougon** (ID: 2)
3. **Villa luxueuse 8 pièces - Riviera** (ID: 4)

## 📸 Capture d'écran

Pour tester rapidement :
1. Allez sur : `http://127.0.0.1:8000/properties/ar-demo/`
2. Cliquez sur une propriété
3. Vous verrez la maison en 3D !

---

**Bonne exploration AR ! 🚀**

