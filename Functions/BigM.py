from simplex import *
from createFirstTableau import create_first_tableau
M = 1e6 

def big_m_method(c, A, b, constraint_types, is_max=True,vars_names=None):
    if vars_names is None:
        vars_names = [f"X{i+1}" for i in range(len(c))]  
    tableau, column_names, row_names, artificial_vars, tableaux_history = create_first_tableau(c, A, b, constraint_types, vars_names,is_max,"bigm")
    status,solution, objective_value, tableaux = simplex_with_visualization(tableau, column_names, row_names, is_max, tableaux_history)
    if solution is None:
        print("Problem is unbounded.")
        return "UNBOUNDED",None, None, tableaux 
    if any(abs(solution[var]) > 0 for var in artificial_vars):
        print("No feasible solution ")
        return "INFEASIBLE",None, None, tableaux

    return status,solution, objective_value, tableaux