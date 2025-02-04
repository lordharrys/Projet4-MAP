# Objectif II
import tkinter as tk
"""
Input: 
airports.csv
new_routes.csv
waiting_times.csv
prices.csv

Ouput:
path                array of edges to visit
"""
def recommandations(airports, new_routes, waiting_times, prices):
    
    root = tk.Tk()
    choix = tk.StringVar()
    options = ["Distance", "Temps", "Prix"]
    for option in options:
        tk.Radiobutton(root, text=option, variable=choix, value=option).pack(anchor="w")
    if choix.get() == "Distance":
        values = new_routes
    if choix.get() == "Temps":
        values = waiting_times
    if choix.get() == "Prix":
        values = prices
        
    start_choice = tk.Combobox(root, values=airports, state="readonly")
    end_choice = tk.Combobox(root, values=airports, state="readonly")
    # attention si aéroports pas connexes
    start = start_choice.get()
    end = end_choice.get()
    if not start or not end:
        tk.messagebox.showwarning("Erreur", "Veuillez sélectionner un aéroport de départ et d'arrivée.")
        return
    btn_valider = tk.Button(root, text="Meilleur trajet", command=dijkstra(V, E, values, start, end))
    
    root.mainloop()


"""
Input: 
V                   array of vertices
E                   array of edges
values              array of edges' values
start               starting airport
end                 ending airport
"""
def dijkstra(V, E, values, start, end):

    return