# Locivoire — Démo client

Plateforme simple de **location immobilière en Côte d'Ivoire** avec :

- **Prestataires** (propriétaires) et **locataires**
- **Carte** des maisons disponibles en CI
- **Visites immersives 360°** (sans casque VR)
- Recherche par ville / type / prix

## Lancer en 3 commandes

```powershell
cd c:\Users\pelmansion.soro\Desktop\LOCIVOIRE
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py load_demo_data --fresh
python manage.py runserver
```

Ouvrir : http://127.0.0.1:8000/

## Comptes de test

| Rôle | Identifiant | Mot de passe |
|------|-------------|--------------|
| Prestataire | `soro` | `soro123` |
| Prestataire | `jean` | `jean123` |
| Locataire | `kader` | `kader123` |
| Locataire | `marie` | `marie123` |

## Parcours démo (2 minutes)

1. **Accueil** — Hero + recherche + chips villes ivoiriennes  
2. **Carte** — Biens placés à Abidjan, Bouaké, Yamoussoukro, San-Pédro, Grand-Bassam…  
3. **Fiche bien** — Photos, prix, carte locale  
4. **Visite immersive** — Bouton « Visite virtuelle » → pièces 360°  
5. **Connexion locataire** (`kader`) → réserver / favoris  
6. **Connexion prestataire** (`soro`) → tableau de bord / médias  

## Recharger les données

```powershell
python manage.py load_demo_data --fresh
```
