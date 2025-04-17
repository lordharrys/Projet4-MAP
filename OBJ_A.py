
import pandas as pd
import networkx as nx
from src.distance import distance
from pyomo.environ import *






############    STEP 1 : Create the DIRECTED GRAPH


def data_processing(file1,file2, route):
    t_airports = pd.read_csv(file1)
    capacities_airports = pd.read_csv(file2)
    airports = pd.merge(t_airports, capacities_airports, left_on='ID', right_on='airportsID', how='left')
    routes = pd.read_csv(route)
    
    
    G = nx.DiGraph()
    for _, row in airports.iterrows():
        G.add_node(row["ID"], name=row["name"], capacity= row["capacity"], latitude=row["latitude"], longitude=row["longitude"])
        

        edges = {}
        for _, row in routes.iterrows():
            start, end = row["ID_start"], row["ID_end"]
            if start in G.nodes and end in G.nodes:
                lat1 = G.nodes[start]["latitude"]
                lon1 = G.nodes[start]["longitude"]
                lat2 = G.nodes[end]["latitude"]
                lon2 = G.nodes[end]["longitude"]
            
                dist = distance(lat1, lat2, lon1,lon2)  
            
                G.add_edge(start, end, distance=dist,capacity=row["connexion capacity"])      
                edges[(start, end)] = dist  
            
    return G
 


            
############    STEP 2 : Modelisation of the problem using Pyomo + solver



def objective_A(source,puits,F,m):
    
    G = data_processing('files/airports.csv','files/capacities_airports.csv', 'files/capacities_connexions.csv')
    F_max, flow_dict = nx.maximum_flow(G, source, puits) # Compute the MAXIMUM FLOW using the library NetworkX
    
    model = ConcreteModel()
    model.V = Set(initialize=G.nodes())  
    model.E = Set(initialize=G.edges()) 
    
    model.x = Var(model.E, domain=NonNegativeReals)  # Flow
    model.y = Var(model.E, domain=Binary)            # Binary variable 
    
    model.obj= Objective(expr=sum(G[u][v]['distance'] * model.y[u, v] for u, v in model.E), sense=minimize) 
    
    
    # Source 
    model.source_constraint = Constraint(expr=sum(model.x[source, j] for j in model.V) - sum(model.x[j, source] for j in model.V) == F)

    # Puits 
    model.sink_constraint = Constraint(expr=sum(model.x[j, puits] for j in model.V) - sum(model.x[puits, j] for j in model.V) == F)

    # Noeuds intermédiaires
    model.flow_conservation = Constraint(model.V - {source, puits}, rule=lambda model, i: sum(model.x[j, i] for j in model.V) - sum(model.x[i, j] for j in model.V) == 0)

    # Contraintes de capacité
    model.flow_limit = Constraint(model.E, rule=lambda model, i, j: model.x[i, j] <= G[i][j]["connexion capacity"] * model.y[i, j])

   # Cas 1 
   
    if(F<=F_max):
        solver = SolverFactory('glpk') 
        solver.solve(model)
        for (i, j) in model.E:
            print(f"Flot de l'aéroport {i} à l'aéroport {j} = {model.x[(i, j)].value}")
            
        dist_tot=0
        for(i,j) in model.E:
            dist_tot+=model.x[(i,j)].value*G[i][j]['distance']
        print("Distance moyenne parcourue =", dist_tot/F)
            
        
    else: 
        for i in range(m):
            F_i = F_max if i < m - 1 else F - (m - 1) * F_max
            print(f"--- Lancement du flot {i+1}/{m} : taille = {F_i} ---")
            solution_i = objective_A(source, puits, F_i) 
            print(f"Solution pour le flot {i+1}: {solution_i}")
        

           

objective_A("BKK", "ADD", 1000,5) 
   
    








