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
def recommandations(G, waiting_times, prices,J,time):
    preferences = input("Quel critère est le plus important pour vous ? (Distance, Temps, Prix) : ")
    if preferences == "Distance":
        values = nx.get_edge_attributes(G, "weight")
    elif preferences == "Temps":
        values = time
    elif preferences == "Prix":
        values = prices
    else:
        print("Veuillez entrer un critère valide.")
        return
    start = input("Aéroport de départ : ")
    if start not in G.nodes:
        print("Veuillez entrer un aéroport valide.")
        return
    end = input("Aéroport d'arrivée : ")
    if end not in G.nodes:
        print("Veuillez entrer un aéroport valide.")
        return
    if(start,end) not in J:
        if dfs(start, end, G)==False:
            print("Ce trajet n'est pas possible.")
            return
        
    routes_values = nx.DiGraph(G)
    if(preferences != "Distance"):
        for u, v in routes_values.edges:
            routes_values[u][v]["weight"] = values.get((u, v))
            if preferences == "Temps":
                if u != start :
                    routes_values[u][v]["weight"] += waiting_times[u]
    
    solution = nx.shortest_path(G, source=start, target=end, weight="weight")
    print("chemin trouvé yay")
    print(solution)
    return


def recommandations_interface(G, waiting_times, prices,J,time):
    window = tk.Tk()
    window.title("Recommandations")
    
    Question1 = tk.Label(window, text="Quel critère est le plus important pour vous ? ")
    Question1.pack()
    preference = tk.Scrollbar(window)
    preference.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(window, yscrollcommand=preference.set)
    listbox.insert(tk.END, "Distance")
    listbox.insert(tk.END, "Temps")
    listbox.insert(tk.END, "Prix")
    listbox.pack()
    preference.config(command=listbox.yview)
    
    listbox.bind("<ButtonRelease-1>", lambda event: on_item_click(event, listbox))
    
    window.mainloop()
    
def on_item_click(event,listbox):
    clicked_item = listbox.get(listbox.nearest(event.y))  # Get the item where the click occurred
    return clicked_item


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