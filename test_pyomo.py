from pyomo.environ import *

# Création du modèle
model = ConcreteModel()

# Définition des variables de décision
model.x = Var(within=NonNegativeReals)  # Variable x >= 0
model.y = Var(within=NonNegativeReals)  # Variable y >= 0

# Définition de la fonction objectif
model.obj = Objective(expr=2*model.x + 3*model.y, sense=minimize)

# Définition des contraintes
model.constraint1 = Constraint(expr=model.x + model.y >= 4)
model.constraint2 = Constraint(expr=model.x - model.y <= 2)

# Résolution du modèle
solver = SolverFactory('glpk')  # Utilisation du solveur GLPK (vous pouvez utiliser d'autres solveurs comme 'cplex' ou 'gurobi')
solver.solve(model)

# Affichage des résultats
print(f"Valeur optimale de x = {model.x()}")  # Valeur optimale de x
print(f"Valeur optimale de y = {model.y()}")  # Valeur optimale de y
print(f"Valeur de la fonction objectif = {model.obj()}")  # Valeur optimale de la fonction objectif
