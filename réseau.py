from pyomo.environ import *
from data_preprocessing import data_preprocessing



def reseau(airports, routes, C):
    model = ConcreteModel()
    model.x = Var(routes, within=Binary)
    model.obj = Objective(rule=objective(model, routes, C), sense=minimize)
    solver = SolverFactory('glpk')
    solver.solve(model)


def objective(model, routes, C):

    total_cost = C * sum(model.x[e] for e in routes)




airports, routes, G = data_preprocessing("files/airports.csv", "files/pre_existing_routes.csv")