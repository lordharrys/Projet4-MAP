import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyomo.environ import *
import builtins
import distance

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
            model.add_component(f"activation_{i}_{e}", Constraint(expr=model.f[i, e] <= model.x[e]))


    solver = SolverFactory('scip')  
    solver.solve(model, tee=False)

    return model


