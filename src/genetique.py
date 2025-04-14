import pandas as pd
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import data_processing as data_processing
import Projet4 as Projet4


def evaluate(solution, J, C):
    """
    Évaluation d'une solution avec Dijkstra par source et cache basé sur tuple(solution)
    """
    G = nx.DiGraph([(start, end, {"weight" : weight}) for start , end, weight in solution])
  
     
    sources = {src for src, dest in J}
    try:
        shortest_paths = {src: nx.single_source_dijkstra_path_length(G, src, weight='weight') for src in sources}
    except:
        return 1e9

    total_distance = 0
    for src,dest in J:
        try:
            total_distance += shortest_paths[src][dest]
        except:
                return 1e9  # si un trajet est impossible
    

    return total_distance / len(J) + C * len(solution)


def generate_initial_population(pop_size, P):
    return [random.sample(P, random.randint(len(P)//4, len(P))) for i in range(pop_size)]




def crossover(parent1, parent2):
    """
    Croisement entre deux parents. 
    """
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

def genetic_algorithm(P, J, C, generations=100, pop_size=100):
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






