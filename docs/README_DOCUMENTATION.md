# Documentation LocIvoire

## Charte d'Identité de Marque

Ce dossier contient le **document officiel d'identité de marque** de LocIvoire.

### Fichiers disponibles

| Fichier | Description |
|---------|-------------|
| `IDENTITE_MARQUE_LOCIVOIRE.html` | Version HTML complète avec mise en forme professionnelle et tous les accents |
| `IDENTITE_MARQUE_LOCIVOIRE.pdf` | Version PDF générée automatiquement |
| `generate_brand_pdf.py` | Script Python pour régénérer le PDF |

### Obtenir une version PDF optimale

**Option recommandée** (qualité maximale, tous les accents) :
1. Ouvrir `IDENTITE_MARQUE_LOCIVOIRE.html` dans Chrome ou Edge
2. Appuyer sur `Ctrl + P` (Imprimer)
3. Choisir **« Enregistrer au format PDF »**
4. Enregistrer le fichier

**Option alternative** (génération automatique) :
```powershell
pip install fpdf2
python docs\generate_brand_pdf.py
```
