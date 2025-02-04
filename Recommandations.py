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
        values = 1
    dijkstra()
    
    return


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