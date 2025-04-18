<<<<<<< HEAD
# Projet4-MAP
Project LEPL1507-2025



🔹 1. Pyomo = l'interface de modélisation

Pyomo est une librairie Python utilisée pour formuler, résoudre et analyser des problèmes d’optimisation mathématique. 

Mais il ne résout pas le problème à lui seul.
➡️ Il doit être connecté à un solveur (comme CBC ou Gurobi) pour vraiment "calculer".

🔸 2. SCIP = le solveur libre 
CBC (Coin-or Branch and Cut) est un solveur open-source capable de résoudre ton problème.



---CONFIGURATION---
pip install pyomo
sudo apt install coinor-cbc
=======
# Projet LEPL1507 Groupe 2
## Structure du projet

```
├── README.md
├── Recommandations.py
├── Recommandations_test.py
├── SIR_mine.py
├── files
│   ├── airports.csv
│   ├── capacities_airports.csv
│   ├── capacities_connexions.csv
│   ├── pre_existing_routes.csv
│   ├── prices.csv
│   ├── simulation_plots
│   ├── test_airports.csv
│   └── waiting_times.csv
├── objectif_B.py
├── robustesse.py
└── src
    ├── benchmark.py
    ├── data_processing.py
    ├── distance.py
    ├── genetique.py
    ├── interface.py
    ├── new_network.py
    ├── optimisation.py
    ├── plot_network.py
    ├── test_objectif1.py
    └── test_pygad.py
```

### genetique.py 

Contient toutes les fonctions nécessaires pour l'algorithme génétique. 


### distance.py
Contient la fonction distance qui calcule la distance entre 2 points sur la carte

### optimisation.py
Résolution de l'objectif 1 via un solver d'optimisation, nécessite:
- pyomo
- un solver d'optimisation (ex: cbc, scip, gurobi,...)

Il n'est pas nécessaire dans la résolution finale de **new_network**

### plot_network.py
Permet d'afficher le réseau sur une carte du monde. 

Arguments :
- G : graphe networkx du réseau
- airports.csv : csv contenant les informations des aéroports

Nécessite:
- cartopy

### interface.py

Code pour l'interface streamlite.

Nécessite :
- streamlite
- cartopy

### data_processing.py

Crée un graphe networkx à partir des fichiers du projet.

**Arguments:**
- airports.csv
- pre_existing_routes.csv

### test_pygad.py

Implémentation de l'algorithme génétique utilisant la librairie pygad. Encore une fois cette implémentation n'étant pas celle retenue, il n'est pas nécessaire pour le projet.

## Nouveau réseau aérien

### Librairies nécessaires

La fonction pour créer le nouveau réseau aérien se situe dans le fichier new_network.py. Afin d'utiliser cette fonction il faut posséder certaines librairies.
- numpy
- pandas
- networkx

Ce sont des librairies assez basiques mais si vous ne les possédez pas il faut tout simplement taper cette commande


````
pip install <library>
`````
ou si vous utilisez anaconda:
`````
conda install <library>
``````

Maintenant pour exécuter cette fonction il suffit d'exécuter le script **new_network.py**


## Interface de recommandations de vols

### Librairies nécessaires

- pandas 
- networkx
- matplotlib
- cartopy
- numpy
- streamlit

Streamlit permet d'avoir une interface facile et visuelle et cartopy nous permet de tracer les vols sur une carte. Encore une fois les installations sont les mêmes pour toutes les libraires : 

`````
pip install <library>
``````
ou 
`````
conda install <library>
``````

### Lancement de l'interface

Afin de lancer l'interface il suffit de faire :
`````
streamlit run src/interface.py
``````
Cela lancera l'interface avec les aéroports et tous les vols possibles qui nous ont été donnés lors du projet. 

**Attention l'interface se lancera dans votre navigateur, il faudra donc peut-être confirmer l'autorisation de streamlit pour utiliser votre navigateur.** 

***L'interface est également disponible via le lien suivant:***
https://lepl1507g02.streamlit.app
>>>>>>> 99ffc3bf28a39692ebcc257f670489e7b09b3469
