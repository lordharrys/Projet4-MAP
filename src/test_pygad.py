import pandas as pd
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import data_processing as data_processing
import Projet4 as Projet4
import pygad
import genetique 



def build_graph(solution, P):
    G = nx.DiGraph()
    for i, bit in enumerate(solution):
        if bit == 1:
            u, v, w = P[i]
            G.add_edge(u, v, weight=w)
    return G


def new_network(airports, pre_existing_routes, J, C):
    G, P_edges = data_processing.data_processing(airports, pre_existing_routes)
    P = []
    for start, end in P_edges.keys():
        P.append((start, end, P_edges[(start, end)]))

    def fitness_func(ga_instance, solution, solution_idx):
        G = build_graph(solution, P)

        try:
            sources = {a for a, _ in pairs}
            dijkstra_results = {
                a: nx.single_source_dijkstra_path_length(G, a, weight='weight') for a in sources
            }
        except:
            return -1e8  # grosse pénalité

        total_distance = 0
        for a, b in pairs:
            try:
                total_distance += dijkstra_results[a][b]
            except:
                return -1e8  # pénalité si pas de chemin

        avg_distance = total_distance / len(pairs)
        total_edges = sum(solution)

        fitness = - (avg_distance + C * total_edges)  # ⚠️ NEGATIF car PyGAD MAXIMISE
        return fitness
    
    num_genes = len(P)
    ga_instance = pygad.GA(
        num_generations=100,
        num_parents_mating=30,
        fitness_func=fitness_func,
        sol_per_pop=100,
        num_genes=num_genes,
        gene_type=int,
        gene_space=[0, 1],
        mutation_type="random",
        mutation_probability=0.1,
        crossover_type="single_point",
        stop_criteria="saturate_20"
    )
    ga_instance.run()
    ga_instance.plot_fitness()

    solution, solution_fitness, _ = ga_instance.best_solution()
    selected_edges = [P[i] for i in range(len(solution)) if solution[i] == 1]
    return selected_edges, -solution_fitness


# Import des données
file = "files/airports.csv"
route = "files/pre_existing_routes.csv"
G, P_edges = data_processing.data_processing(file, route)
P = []
for start, end in P_edges.keys():
    P.append((start, end, P_edges[(start, end)]))
#print("Noeuds du graphe :", G.nodes())
G_copy = G.copy()

# Liste des trajets à satisfaire
number_of_pairs = 1000


def generate_unique_pairs(nodes, number_of_pairs, directed=True):
    seen = set()
    pairs = []

    while len(pairs) < number_of_pairs:
        a, b = random.sample(nodes, 2)
        pair = (a, b) if directed else tuple(sorted((a, b)))
        if pair not in seen:
            seen.add(pair)
            pairs.append((a, b))  # garder (a,b) même si non orienté pour compatibilité
    return pairs
# Lancer l'algorithme génétique
C = 1000
pairs = generate_unique_pairs(list(G.nodes()), number_of_pairs, directed=True)

_, cost = new_network(file, route, pairs, C)
print("Coût total optimisé avec PyGAD :", cost)

best_cost, selected_edges = genetique.genetic_algorithm(P, pairs, C)
print("Meilleur coût avec l'algorithme génétique :", best_cost)
sum = 0
for start, end in pairs:
    sum += nx.shortest_path_length(G_copy, start, end, weight='weight')
sum /= len(pairs)
print("Coût total avant optimisation :", sum+len(selected_edges)*C)
#model = Projet4.resolution(G_copy, pairs, P_edges, C)
#print("Coût total optimisé avec le modèle :", model.obj())


