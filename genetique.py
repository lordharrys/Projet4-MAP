import pandas as pd
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import data_processing
import Projet4





def dijkstra_distance(G, a, b):
    try:
        return nx.dijkstra_path_length(G, a, b, weight='weight')
    except:
        return float('inf')

def evaluate(solution, J, C):
    """
    Évaluation d'une solution avec Dijkstra par source et cache basé sur tuple(solution)
    """
    G = nx.DiGraph([(start, end, {"weight" : weight}) for start , end, weight in solution])
  
     
    sources = {At for At, _ in J}
    try:
        dijkstra_results = {
            At: nx.single_source_dijkstra_path_length(G, At, weight='weight')
            for At in sources
        }
    except:
        return 1e9

    total_distance = 0
    for At, Al in J:
        try:
            total_distance += dijkstra_results[At][Al]
        except:
                return 1e9  # si un trajet est impossible

    total_dist = total_distance / len(J)
    

    return total_dist + C * len(solution)


def generate_initial_population(pop_size, P):
    return [random.sample(P, random.randint(len(P)//3, len(P))) for _ in range(pop_size)]




def crossover(parent1, parent2):
    """Croisement entre deux parents."""
    split = random.randint(1, min(len(parent1), len(parent2))-1)
    child = list(set(parent1[:split] + parent2[split:]))
    return child



def mutate(individual, P, mutation_rate=0.1):
    """
    Mutation d'un individu sous forme de liste d'arêtes.
    Ajoute ou retire une arête avec une certaine probabilité.
    """
    if random.random() < mutation_rate:
        if random.random() < 0.5 and len(individual) > 1:
            # Suppression aléatoire d'une arête existante
            individual.remove(random.choice(individual))
        else:
            # Ajout d'une arête aléatoire non déjà présente
            available_edges = list(set(P) - set(individual))
            if available_edges:
                individual.append(random.choice(available_edges))
    return individual

def tournament_selection(population, scores, k=5):
    selected = random.sample(list(zip(population, scores)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def genetic_algorithm(P, J, C, generations=100, pop_size=150):
    """
    Algorithme génétique pour optimiser le réseau de routes (individus = liste d'arêtes).
    """
    population = generate_initial_population(pop_size, P)
    print("Population initiale générée.")
    best_scores = []

    for gen in range(generations):
        print(f"Génération {gen + 1}")

        # Évaluation avec cache
        fitnesses_with_individuals = [
            (evaluate(ind, J, C), ind)
            for ind in population
        ]
        fitnesses_with_individuals.sort(key=lambda x: x[0])
        population = [ind for _, ind in fitnesses_with_individuals]
        scores = [fit for fit, _ in fitnesses_with_individuals]

        # Sélection des meilleurs
        elite_size = int(pop_size * 0.25)
        top = population[:elite_size]
        children = []

        # Génération des enfants
        while len(children) < pop_size - len(top):
            p1 = tournament_selection(population, scores)
            p2 = tournament_selection(population, scores)
            child = crossover(p1, p2)
            child = mutate(child, P, mutation_rate=0.1)
            children.append(child)

        population = top + children
        best_scores.append(scores[0])

    # Sélection finale du meilleur
    best = population[0]
    best_cost = scores[0]

    # Affichage de l'évolution
    plt.plot(best_scores)
    plt.title("Évolution du coût au fil des générations")
    plt.xlabel("Génération")
    plt.ylabel("Coût")
    plt.grid()
    plt.show()

    return best_cost, best



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
number_of_pairs = 100


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
C = 1
pairs = generate_unique_pairs(list(G.nodes()), number_of_pairs, directed=True)
print("Paires générées :", pairs)
best_cost, selected_edges = genetic_algorithm(P, pairs, C)
print("Coût total optimisé avec l'algorithme génétique :", best_cost)
model = Projet4.resolution(G_copy, pairs, P_edges, C)
print("Coût total optimisé avec le modèle :", model.obj())


