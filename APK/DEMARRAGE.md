# Locivoire Mobile App

Voir le guide complet : [APK/README.md](./APK/README.md)

## Démarrage rapide (APK debug)

```bash
# Terminal 1 — backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2 — app
cd APK
npm install
npm run android
```

Puis dans Android Studio : Run ▶

Package ID : `ci.locivoire.app`  
Admin démo : `admin` / `admin123`
