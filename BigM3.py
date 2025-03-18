import numpy as np
from simplex3 import simplex_with_visualization

M = 1e6  

def create_big_m_tableau(c, A, b, constraint_types, is_max=True):
    num_constraints, num_vars = A.shape
    if is_max:
        c = -np.array(c)  

    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    total_vars = num_vars + num_slack + num_surplus + num_artificial

    A_extended = np.zeros((num_constraints, total_vars))
    A_extended[:, :num_vars] = A
    slack_count = surplus_count = artificial_count = 0
    artificial_vars = []

    column_names = [f"x{i+1}" for i in range(num_vars)]
    row_names = [f"Constraint {i+1}" for i in range(num_constraints)]

    for i, t in enumerate(constraint_types):
        if t == "<=":
            A_extended[i, num_vars + slack_count] = 1
            column_names.append(f"s{slack_count+1}")
            slack_count += 1
        elif t == ">=":
            A_extended[i, num_vars + slack_count + surplus_count] = -1  
            column_names.append(f"s{surplus_count+1}")
            surplus_count += 1
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count] = 1 
            column_names.append(f"a{artificial_count+1}")
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count)
            artificial_count += 1
        elif t == "=":
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count] = 1  
            column_names.append(f"a{artificial_count+1}")
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count)
            artificial_count += 1
            
    column_names.append("RHS")

    c_extended = np.zeros(total_vars)
    c_extended[:num_vars] = c  
    for a_var in artificial_vars:
        c_extended[a_var] = M  

    tableau = np.column_stack((A_extended, b))
    objective_row = np.append(c_extended, [0])  
    tableau = np.row_stack((tableau, objective_row)) 

    tableaux_history = [tableau.copy()]

    for i, a_var in enumerate(artificial_vars):
        tableau[-1, :] -= M * tableau[i, :]
        tableaux_history.append(tableau.copy())

    return tableau, column_names, row_names, tableaux_history

def big_m_method(c, A, b, constraint_types, is_max=True):
    """Implements the Big M method using simplex."""
    tableau, column_names, row_names, tableaux_history = create_big_m_tableau(c, A, b, constraint_types, is_max)
    return simplex_with_visualization(tableau, column_names, row_names, tableaux_history)
