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
    preferences = input("Quel critère est le plus important pour vous ? (Distance, Temps, Prix) : ")
    if preferences == "Distance":
        values = new_routes
    if preferences == "Temps":
        values = waiting_times
    if preferences == "Prix":
        values = prices
    else:
        print("Veuillez entrer un critère valide.")
        return
    start = input("Aéroport de départ : ")
    if start not in airports:
        print("Veuillez entrer un aéroport valide.")
        return
    end = input("Aéroport d'arrivée : ")
    if end not in airports:
        print("Veuillez entrer un aéroport valide.")
        return
    # si dans la liste J pas besoin
    if dfs(start, end, new_routes)==False:
        print("Ce trajet n'est pas possible.")
        return
    dijkstra(airports, new_routes, values, start, end)
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

def dfs(start, end, new_routes):
    visited = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current == end:
            return True
        if current not in visited:
            visited.add(current)
            stack.extend(new_routes[current])
    return False