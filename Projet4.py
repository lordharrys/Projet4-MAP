import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyomo.environ import *
import builtins
import distance


airports = pd.read_csv("files/airports.csv")
routes = pd.read_csv("files/pre_existing_routes.csv")

G = nx.DiGraph()

for _, row in airports.iterrows():
    G.add_node(row["ID"], name=row["name"], city=row["city"], country=row["country"], latitude=row["latitude"], longitude=row["longitude"])
    

edges = {}
for _, row in routes.iterrows():
    start, end = row["ID_start"], row["ID_end"]
    
    if start in G.nodes and end in G.nodes:
        lat1 = G.nodes[start]["latitude"]
        lon1 = G.nodes[start]["longitude"]
        lat2 = G.nodes[end]["latitude"]
        lon2 = G.nodes[end]["longitude"]
        dist = distance.distance(lat1, lon1, lat2, lon2)  
        G.add_edge(start, end, weight=dist)
        edges[(start, end)] = dist  


def plot_network(G):
    """
    Plots le graphe sur une carte de la Terre.

    Input:
        - G: un graphe networkx du problème.
    
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    for node in G.nodes():
        lat, lon = G.nodes[node]["latitude"], G.nodes[node]["longitude"]
        # Les noeuds sont nommés par leur ID
        ax.scatter(lon, lat, color='red', s=10, transform=ccrs.PlateCarree())
        ax.annotate(node, (lon, lat), color='black', fontsize=8, ha='right', va='top', transform=ccrs.PlateCarree())

    for start, end in G.edges():
        lat1, lon1 = G.nodes[start]["latitude"], G.nodes[start]["longitude"]
        lat2, lon2 = G.nodes[end]["latitude"], G.nodes[end]["longitude"]

        ax.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.3, transform=ccrs.PlateCarree())

    plt.title("Réseau aérien mondial avec Cartopy")
    plt.show()


def resolution(G, pairs_to_connect, edges, C):    
    
    # Création du modèle
    model = ConcreteModel()

    # Ici ce sont les variables binaires qui indiquent si on inclut l'arête dans notre réseau ou non
    model.x = Var(G.edges, within=Binary)
    
    # Variable qui représente la distance entre chaque paire d'aéroports qu'on veut lier
    model.d = Var(pairs_to_connect, within=NonNegativeReals)

    # Variable pour s'assurer qu'on inclut bien un chemin entre les paires qu'on veut lier
    # Une variable par noeud par paire à lier
    model.f = Var(pairs_to_connect, G.edges, within=NonNegativeReals)

    # Création de la fonction objectif : somme des distances des chemins entre paires + C * nbre d'arêtes
    model.obj = Objective(expr=builtins.sum(model.d[p] for p in pairs_to_connect)/len(pairs_to_connect) + C*builtins.sum(model.x[e] for e in G.edges),sense=minimize)
    
    # On ajoute une contrainte pour chaque paire qui dit que d >= somme des distances du chemin qu'on a choisi pour 
    # les lier
    for i in pairs_to_connect:
        model.add_component(f"shortest_path_{i}", Constraint(expr=model.d[i] == builtins.sum(edges[e] * model.f[i, e] for e in G.edges)))

    # Pour chaque paire on dit que la somme des chemins entrants = sortants sauf si on est au noeud dans la paire 
    # dans ce cas tu dois sortir plus que tu rentres et vice versa
    # Evidemment il y a pour chaque noeud une variable par paire
    for (p, q) in pairs_to_connect:
        for node in G.nodes:
            ini = builtins.sum(model.f[(p, q), i] for i in G.in_edges(node) if i in G.edges)
            out = builtins.sum(model.f[(p, q), i] for i in G.out_edges(node) if i in G.edges)
            if node == p:  
                model.add_component(f"source_{p}_{q}_{node}", Constraint(expr=out - ini == 1))
            elif node == q:  
                model.add_component(f"sink_{p}_{q}_{node}", Constraint(expr= ini - out == 1))
            else:  
                model.add_component(f"conservation_{p}_{q}_{node}", Constraint(expr=out - ini == 0))

    # Assure que une arête n'est utilisée uniquement si elle est prise en compte dans notre réseau
    for i in pairs_to_connect:
        for e in G.edges:
            model.add_component(f"activation_{i}_{e}", Constraint(expr=model.f[(p, q), e] <= model.x[e]))


    solver = SolverFactory('glpk')  
    solver.solve(model, tee=False)

    return model


