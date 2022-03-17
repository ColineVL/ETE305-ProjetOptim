# ETE305-ProjetOptim

Projet optimisation de ETE-305

## Pour le lancer

### Installer les modules

Dans la console, déplacez-vous dans le dossier ETE305-ProjetOptim.

```bash
pip install -r requirements.txt
```

### Lancer le code

```bash
python src\probleme\pbNordSud.py
```

En fonction de votre OS et de votre version de Python, il faudra peut-être changer la commande en `python3` ou mettre des `/` au lieu des `\`.

## Organisation

### Avancement projet

Nos notes d'idées, d'améliorations. Slides de la soutenance.

### Data

Les fichiers excel disponibles sur le LMS : données de base.

### References

Codes des premières séances en classe. Comment utiliser Pulp, comment modéliser des arrêts de centrale...

### Results

Excel résultats de l'optimisation. Graphes et captures d'écran des résultats.

### src

Le code en lui-même !

#### src/modelisation

Lecture du Excel contenant les données de production.

Classes Python : producteurs, zones, améliorations.

Valeurs trouvées sur internet.

#### src/postTraitementFiles

Extraction des solutions, depuis des variables Pulp vers des nombres.

Affichage de valeurs intéressantes (capacités des producteurs).

Affichage de graphes.

Export des données de production dans un classeur Excel.

#### src/problem

Le fichier principal à lancer.

Les variables du problème, les contraintes, l'objectif.
