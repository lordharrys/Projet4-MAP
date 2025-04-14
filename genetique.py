import pandas as pd
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import data_processing
import Projet4



def build_graph_from_solution(solution, P, P_edges):
    G = nx.DiGraph()
    for bit, (u, v) in zip(solution, P):
        if bit == 1:
            #print("Adding edge:", (u, v))

            G.add_edge(u, v, weight=P_edges[(u, v)])
    return G

def all_paths_exist(G, J):
    for a, b in J:
        if not G.has_node(a) or not G.has_node(b):
            return False
    return all(nx.has_path(G, a, b) for a, b in J)

def dijkstra_distance(G, a, b):
    try:
        return nx.dijkstra_path_length(G, a, b, weight='weight')
    except:
        return float('inf')

def evaluate(solution, P, J, P_edges, C):
    """
    Evaluation de la solution
    @param solution: Solution binaire
    @param P: Liste des arêtes possibles
    @param J: Liste des trajets à satisfaire
    @param P_edges: Dictionnaire des poids des arêtes
    @param C: Coefficient de pénalité pour le nombre d'arêtes
    @return: Coût total de la solution
    """
    G = build_graph_from_solution(solution, P, P_edges)
    #print(f"Noeuds du graphe : {G.nodes}")
    if not all_paths_exist(G, J):
        return 1e9  # Pénalité
    total_dist = sum(dijkstra_distance(G, a, b) for (a, b) in J) / len(J)
    return total_dist + C * sum(solution)

def generate_initial_population_with_paths(pop_size, P, G_possible, J, extra_edges=100):
    edge_index = {edge: idx for idx, edge in enumerate(P)}
    population = []
    pop_path = int(pop_size * 0.3)
    pop_random = pop_size - pop_path

    # Génération basée sur les plus courts chemins
    for _ in range(pop_path):
        individual = [0] * len(P)
        for (src, dst) in J:
            if nx.has_path(G_possible, src, dst):
                path = nx.dijkstra_path(G_possible, src, dst, weight='weight')
                for i in range(len(path) - 1):
                    edge = (path[i], path[i + 1])
                    if edge in edge_index:
                        individual[edge_index[edge]] = 1
        # Ajout aléatoire d'extra_edges connexions
        zero_indices = [i for i, val in enumerate(individual) if val == 0]
        if len(zero_indices) > extra_edges:
            selected = random.sample(zero_indices, extra_edges)
            for idx in selected:
                individual[idx] = 1
        population.append(individual)

    # Génération totalement aléatoire
    for _ in range(pop_random):
        population.append([random.randint(0, 1) for _ in range(len(P))])

    return population

def generate_initial_population(pop_size, P):
    return [[random.randint(0, 1) for _ in range(len(P))] for _ in range(pop_size)]



def crossover(p1, p2):
    """
    Crossover entre deux solutions.
    @param p1: Première solution
    @param p2: Deuxième solution
    @return: Nouvelle solution résultant du croisement
    """
    return [random.choice([g1, g2]) for g1, g2 in zip(p1, p2)]

def mutate(solution, rate=0.05):
    """
    Mutate a solution by flipping bits with a given mutation rate.
    @param solution: The solution to mutate
    @param rate: Mutation rate
    @return: Mutated solution
    """
    return [1 - gene if random.random() < rate else gene for gene in solution]

def tournament_selection(population, scores, k=5):
    selected = random.sample(list(zip(population, scores)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def genetic_algorithm(G,P, J, P_edges, C, generations=200, pop_size=300):
    """
    Algorithme génétique pour optimiser le réseau de routes.
    @param G: Graphe initial
    @param P: Liste des arêtes possibles
    @param J: Liste des trajets à satisfaire
    @param P_edges: Dictionnaire des poids des arêtes
    @param C: Coefficient de pénalité pour le nombre d'arêtes
    @param generations: Nombre de générations
    @param pop_size: Taille de la population
    @return: Coût total optimisé et les arêtes sélectionnées
    """
    population = generate_initial_population(pop_size, P)
    print("Population initiale générée.")
    best_scores = []
    for gen in range(generations):
        print(f"Génération {gen + 1}")
        population.sort(key=lambda s: evaluate(s, P, J, P_edges, C))
        scores = [evaluate(ind, P, J, P_edges, C) for ind in population]
        elite_size = int(pop_size * 0.25)
        top = population[:elite_size]
        children = []
        while len(children) < pop_size - len(top):
            p1 = tournament_selection(population, scores)
            p2 = tournament_selection(population, scores)
            child = crossover(p1, p2)
            mutation_rate = max(0.02, 0.1 * (1 - gen / generations))
            child = mutate(child, rate=mutation_rate)
            children.append(child)
        population = top + children
        best_scores.append(evaluate(population[0], P, J, P_edges, C))
    best = min(population, key=lambda s: evaluate(s, P, J, P_edges, C))
    best_cost = evaluate(best, P, J, P_edges, C)
    selected_edges = [edge for bit, edge in zip(best, P) if bit == 1]
    
    plt.plot(best_scores)
    plt.title("Évolution du coût au fil des générations")
    plt.xlabel("Génération")
    plt.ylabel("Coût")
    plt.grid()
    plt.show()

    return best_cost, selected_edges


# Modifie le graphe pour qu'il garde uniquement les arêtes sélectionnées
def modify_graph(G, selected_edges):
    G_new = G.copy()
    for edge in G.edges:
        if edge not in selected_edges:
            #print("Removing edge:", edge)
            G_new.remove_edge(edge[0], edge[1])

    return G_new 

# Import des données
file = "files/airports.csv"
route = "files/pre_existing_routes.csv"
G, P_edges = data_processing.data_processing(file, route)
P = list(P_edges.keys())
#print("Noeuds du graphe :", G.nodes())
G_copy = G.copy()

# Liste des trajets à satisfaire
number_of_pairs = 40
pairs = [random.sample(list(G.nodes()), 2) for _ in range(number_of_pairs)]
print("Paires d'aéroports à relier :", pairs)

# Lancer l'algorithme génétique
C = 5000
best_cost, selected_edges = genetic_algorithm(G,P, pairs, P_edges, C)
print("Coût total optimisé avec l'algorithme génétique :", best_cost)
model = Projet4.resolution(G_copy, pairs, P_edges, C)
print("Coût total optimisé avec le modèle :", model.obj())
#G_new = modify_graph(G, selected_edges)


# Test vraie solution
#model = Projet4.resolution(G_new, J, P_edges, C)
#print("Coût total optimisé avec les deux algos :", model.obj())
