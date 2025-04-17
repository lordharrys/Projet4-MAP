# Projet LEPL1507 Groupe 2
## Structure du projet
## new_network

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

Maintenant pour exécuter cette fonction il faut tout simplement taper cette commande:
`````
python main.py <airports.csv> <pre_existing_routes.csv> <wanted_journeys.csv> <C>
`````

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