import numpy as np
from simplex3 import simplex_with_visualization
from createFirtTable import create_first_tableau
M = 1e6 

def big_m_method(c, A, b, constraint_types, is_max=True):
    """Implements the Big M method while maintaining correct variable order."""
    tableau, column_names, row_names, artificial_vars, tableaux_history = create_first_tableau(c, A, b, constraint_types, is_max,"bigm")
    solution, objective_value, tableaux = simplex_with_visualization(tableau, column_names, row_names, is_max, tableaux_history)
    if solution is None:
        print("Problem is unbounded. Returning None but keeping tableau steps.")
        return None, None, tableaux 
    if any(abs(solution[var]) > 1e-6 for var in artificial_vars):
        print("No feasible solution (artificial variables remain nonzero).")
        return None, None, tableaux

    return solution, objective_value, tableaux