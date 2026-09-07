# Fonctionnalité de Réalité Augmentée - Locivoire

## 🎯 Vue d'ensemble

Locivoire intègre une fonctionnalité de **visite virtuelle en réalité augmentée** permettant aux locataires de visualiser les propriétés dans leur environnement réel via leur smartphone ou ordinateur.

## ✨ Fonctionnalités

### 1. **Visualisation AR Interactive**
- Affichage 3D des propriétés dans l'environnement réel
- Mode 360° pour explorer la propriété
- Contrôles tactiles et à la souris
- Zoom et rotation de la vue

### 2. **Technologies utilisées**
- **AR.js** : Bibliothèque JavaScript open-source pour la réalité augmentée web
- **A-Frame** : Framework webVR pour créer des expériences 3D/VR
- Compatible avec tous les navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Fonctionne sur mobile et desktop

### 3. **Modes de visualisation**
- **Mode AR avec marqueur** : Utilise un marqueur imprimable pour positionner la propriété
- **Mode AR sans marqueur** : Visualisation 360° immersive
- **Mode 3D interactif** : Exploration libre de la propriété

## 🚀 Comment utiliser

### Pour les locataires :
1. Naviguez vers la page de détails d'une propriété
2. Cliquez sur le bouton **"Visite virtuelle AR"** (si disponible)
3. Autorisez l'accès à votre caméra
4. Sur mobile : pointez votre caméra vers un espace ouvert
5. Explorez la propriété en 3D dans votre environnement

### Pour les propriétaires :
1. Connectez-vous à votre tableau de bord
2. Ajoutez une visite AR à votre propriété via l'admin Django
3. Configurez les instructions et options AR

## 📱 Compatibilité

### Navigateurs supportés :
- ✅ Chrome (Android & Desktop) - **Recommandé**
- ✅ Firefox (Android & Desktop)
- ✅ Safari (iOS 11+ & macOS)
- ✅ Edge (Desktop)

### Appareils :
- ✅ Smartphones (iOS & Android)
- ✅ Tablettes
- ✅ Ordinateurs avec webcam

## 🔧 Configuration technique

### Structure de données
```python
class ARTour(models.Model):
    property = OneToOneField(Property)  # Propriété associée
    ar_scene_url = URLField()          # URL d'une scène AR externe
    ar_model_file = FileField()        # Fichier modèle 3D (.gltf, .glb)
    qr_code = ImageField()             # QR Code pour accès rapide
    instructions = TextField()          # Instructions d'utilisation
    is_active = BooleanField()         # Activation de la visite
```

### Intégration dans les templates
```html
<!-- Lien vers la visite AR -->
<a href="{% url 'bookings:ar_tour' property.pk %}">
    Visite virtuelle AR
</a>
```

## 🎨 Personnalisation

### Ajouter un modèle 3D personnalisé
1. Exportez votre modèle 3D au format GLTF ou GLB
2. Uploadez-le via l'admin Django dans le champ `ar_model_file`
3. Le modèle sera automatiquement affiché dans la visite AR

### Créer un QR Code
Utilisez un service comme [QR Code Generator](https://www.qr-code-generator.com/) pour créer un QR code pointant vers l'URL de la visite AR.

## 📊 Propriétés avec AR actives

Les propriétés suivantes ont actuellement des visites AR actives :
- ✅ Villa 10 pièces - Cocody
- ✅ Maison moderne 6 pièces - Yopougon
- ✅ Villa luxueuse 8 pièces - Riviera

## 🔒 Sécurité et confidentialité

- L'accès à la caméra est demandé uniquement pour la fonctionnalité AR
- Aucune donnée vidéo n'est stockée ou transmise
- Les visites AR sont accessibles uniquement aux utilisateurs connectés
- Les propriétaires peuvent activer/désactiver les visites AR

## 🐛 Dépannage

### La caméra ne s'active pas
- Vérifiez que vous avez autorisé l'accès à la caméra
- Assurez-vous d'utiliser HTTPS (requis pour accéder à la caméra)
- Essayez un autre navigateur

### Le modèle 3D ne s'affiche pas
- Vérifiez que le fichier est au format GLTF ou GLB
- Assurez-vous que le fichier est bien uploadé
- Videz le cache du navigateur

### Performance lente
- Fermez les autres applications utilisant la caméra
- Utilisez une connexion internet stable
- Réduisez la qualité du modèle 3D si nécessaire

## 🔮 Améliorations futures

- [ ] Support des modèles 3D photoréalistes
- [ ] Visite guidée avec hotspots interactifs
- [ ] Intégration avec les plans au sol
- [ ] Mode VR pour casques VR
- [ ] Partage social des visites AR
- [ ] Analytics des visites AR

## 📞 Support

Pour toute question ou problème concernant la fonctionnalité AR, contactez l'équipe de développement.

---

**Développé avec ❤️ pour Locivoire**

