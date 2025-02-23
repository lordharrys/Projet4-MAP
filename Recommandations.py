# Objectif II
import tkinter as tk
import networkx as nx
"""
Input: 
airports.csv
new_routes.csv
waiting_times.csv
prices.csv

Ouput:
path                array of edges to visit
"""

def recommandations_interface(G, waiting_times, prices,J,time):
    root = tk.Tk()
    root.title("Recommandations")
    
    preference = tk.StringVar()
    preference.set("Distance")
    
    Question1 = tk.Label(root, text="Quel critère est le plus important pour vous ?")
    Question1.pack()
    tk.Radiobutton(root, text="Distance", value="Distance", variable=preference).pack()
    tk.Radiobutton(root, text="Temps", value="Temps", variable=preference).pack()
    tk.Radiobutton(root, text="Prix", value="Prix", variable=preference).pack()
    
    
    start = tk.StringVar()
    start.set("Aéroport de départ")
    Question2 = tk.Label(root, text="Aéroport de départ : ")
    Question2.pack()
    for airport in G.nodes:
        tk.Radiobutton(root, text=airport, value=airport, variable=start).pack()

    
    end = tk.StringVar()
    end.set("Aéroport d'arrivée")
    Question3 = tk.Label(root, text="Aéroport d'arrivée : ")
    Question3.pack()
    for airport in G.nodes:
        tk.Radiobutton(root, text=airport, value=airport, variable=end).pack()

    
    Confirm3 = tk.Button(root, text="Confirmer le trajet", command=lambda: confirm_traject(root,start.get(),end.get(),G,J,preference.get(),prices,time,waiting_times))
    Confirm3.pack()
    
    tk.mainloop()

def confirm_traject(root,start,end,G,J,preference,prices,time,waiting_times):
        if(start,end) not in J:
            if dfs(start, end, G)==False:
                label = tk.Label(root, text="Ce trajet n'est pas possible.")
                label.pack()
                return
        label2 = tk.Label(root, text="Trajet confirmé.")
        label2.pack()
        
        if preference == "Distance":
            values = nx.get_edge_attributes(G, "weight")
        elif preference == "Temps":
            values = time
        elif preference == "Prix":
            values = prices
        else:
            label = tk.Label(root, text="Veuillez entrer un critère valide.")
            label.pack()
            return

        routes_values = nx.DiGraph(G)
        if preference != "Distance":
            for u, v in routes_values.edges:
                routes_values[u][v]["weight"] = values.get((u, v))
                if preference == "Temps":
                    if u != start:
                        routes_values[u][v]["weight"] += waiting_times[u]

        solution = nx.shortest_path(G, source=start, target=end, weight="weight")
        label = tk.Label(root, text=f"Chemin trouvé: {solution}")
        label.pack()


def dfs(start, end, G):
    visited = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current == end:
            return True
        if current not in visited:
            visited.add(current)
            stack.extend(neighbor for neighbor in G.neighbors(current) if neighbor not in visited)
    return False