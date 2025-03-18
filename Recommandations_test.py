from Recommandations import recommandations_interface
import networkx as nx
from distance import distance
import data_processing
import Projet4

G, edges = data_processing.data_processing("files/airports.csv", "files/pre_existing_routes.csv")


# Create a small graph with 5 airports
G = nx.DiGraph()

pairs_to_connect = [('LOS', 'BOS'),('YYZ','BOS'),('JFK','YYZ'),('AKL','LOS'),('AKL','LAX'),('IAH','LAX'),('IAH','JFK')]
model = Projet4.resolution(G, pairs_to_connect, edges, 0)

# Test the recommandations function
recommandations_interface(G, waiting_times, prices,J,time)