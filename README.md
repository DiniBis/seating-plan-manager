# Plan de Classe - Gestionnaire de Places

Une application Python avec interface graphique pour gérer facilement les plans de classe et l'attribution des places aux élèves.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)

## Fonctionnalités

- **Interface graphique intuitive** avec Tkinter
- **Plan de classe configurable** : choix entre 4 ou 6 rangées
- **Import des élèves** depuis fichiers CSV
- **Attribution simple** : clic gauche pour assigner, clic droit pour libérer
- **Sauvegarde/Chargement** des plans au format JSON
- **Visualisation claire** avec tableau et numérotation des places
- **Gestion automatique** de la liste des élèves disponibles

## Installation

### Prérequis
- Python 3.7 ou supérieur
- Tkinter (généralement inclus avec Python)

### Installation
1. Clonez ou téléchargez les fichiers du projet
2. Aucune installation de dépendances supplémentaires requise (utilise uniquement les modules Python standard)

## Utilisation

### Lancement de l'application
```bash
python scripts/classroom_app.py
```

### Guide d'utilisation

#### 1. Chargement des élèves
- Cliquez sur **"Charger CSV"**
- Sélectionnez votre fichier CSV contenant les noms des élèves
- Les élèves apparaissent dans la liste de droite

#### 2. Configuration du plan
- Utilisez le menu déroulant pour choisir **4 ou 6 rangées**
- Le plan se met à jour automatiquement

#### 3. Attribution des places
- **Sélectionnez un élève** dans la liste de droite
- **Clic gauche** sur une place libre pour l'assigner
- **Clic droit** sur une place occupée pour la libérer

#### 4. Sauvegarde
- **"Sauvegarder"** : enregistre le plan actuel au format JSON
- **"Charger Plan"** : charge un plan précédemment sauvegardé
- **"Réinitialiser"** : remet à zéro le plan de classe

## Format des fichiers

### Fichier CSV des élèves
Le fichier CSV doit contenir un nom d'élève par ligne :
```csv
Martin Chafut
Étienne Lantier 
Ambroise Croizat
```

### Fichier de sauvegarde JSON
Les plans sont sauvegardés au format JSON avec :
- Configuration des rangées et colonnes
- Positions des élèves
- Liste complète des élèves

## Interface utilisateur

### Zone principale
- **Plan de classe** : visualisation graphique avec tableau en haut
- **Liste des élèves** : élèves disponibles à droite
- **Contrôles** : boutons de gestion en haut

### Codes couleur
- **Gris clair** : place libre (affiche R1P1, R2P3, etc.)
- **Bleu clair** : place occupée (affiche le nom de l'élève)
