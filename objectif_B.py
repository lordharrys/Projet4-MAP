import data_processing
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import matplotlib.pyplot as plt
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend


#define a region that contains the airports in a certain perimeter around the starting airport
def define_region(latitude,longitude,perimeter,airports):
    region = []
    for airport in airports:
        if (latitude - perimeter <= airports[airport]["latitude"] <= latitude + perimeter) and (longitude - perimeter <= airports[airport]["longitude"] <= longitude + perimeter):
                region.append(airport)
    return region

#return the degrees of the nodes in the region that are connected to nodes outside the region
def get_region_degrees(G,region):
    degrees = {}
    for node in region:
        degrees[node] = 0
    for node in G.nodes:
        if node in region:
            for neighbor in G.neighbors(node):
                if neighbor not in region:
                    degrees[node] +=1
    return degrees

#remove the npdes with the highest degrees outside the region from the graph
def remove_edges(G,edges,degrees):
    sorted_degrees = dict(sorted(degrees.items(), key=lambda item: item[1]))
    for key in list(sorted_degrees.keys())[-5:]:
        G.remove_node(key)
    return G,edges

#Objectif B when we know where the disease started
def objectif_B_start(G,edges,start,perimeter):
    region_disease = define_region(G.nodes[start]["latitude"],G.nodes[start]["longitude"],perimeter,G.nodes)
    degrees_region_disease = get_region_degrees(G,region_disease)
    G,edges = remove_edges(G,edges,degrees_region_disease)
    return G,edges
 
 
#Objectif B when we don't know where the disease started
def objectif_B(G):
    closeness_centrality = nx.closeness_centrality(G)
    sorted_closeness = dict(sorted(closeness_centrality.items(), key=lambda item: item[1]))

    # Supprimer les 15 aéroports ayant la centralité de proximité la plus faible (les plus proches de tous les autres)
    airports_to_remove = list(sorted_closeness.keys())[:15]
    for airport in airports_to_remove:
        G.remove_node(airport)
    return G



### SIR model ###
def SIR_model():
    G_SIR, routes = data_processing.data_processing("files/airports.csv", "files/pre_existing_routes.csv")
    model = ep.SIRModel(G_SIR)

    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter('gamma', 0.005)
    cfg.add_model_parameter("fraction_infected", 0.05)
    model.set_initial_status(cfg)

    removed_nodes = set()
    fermés = []
    iterations = model.iteration_bunch(75)
    infected_nodes = set()
    extinction_time = 0

    for t in iterations[:25]:
        infected_nodes.update([node for node, status in t["status"].items() if status == 1])

    # Fermer les aéroports les moins centraux
    closeness_centrality = nx.closeness_centrality(G_SIR)
    sorted_closeness = sorted(closeness_centrality, key=closeness_centrality.get)

    airports_to_remove = sorted_closeness[:15]
    for airport in airports_to_remove:
        model.status[airport] = 2

    G_SIR.remove_nodes_from(airports_to_remove)  # Supprime réellement du graphe

    # Continuer la simulation après la fermeture
    for i, t in enumerate(iterations[25:], start=25):
        infected_nodes.update([node for node, status in t["status"].items() if status == 1])
        if not infected_nodes:  # Si plus d'infectés
            extinction_time = i
            break  # Arrêter la simulation

        removed_nodes.update(infected_nodes)
        fermés.extend(infected_nodes)

    print(f"Nombre d'aéroports fermés : {len(fermés)}")
    print(f"Temps d'extinction : {extinction_time}")

    trends = model.build_trends(iterations)
    viz = DiffusionTrend(model, trends)
    viz.plot()
    plt.savefig("sir_simulation.png")
    plt.show()
    plt.close()

SIR_model()