import numpy as np
from simplex3 import simplex_with_visualization
from createFirtTable import create_first_tableau

def remove_artificial_variables(tableau, artificial_vars, column_names, row_names, tableaux_history):
    artificial_vars = sorted(artificial_vars, reverse=True)
    for var in artificial_vars:
        if var < len(column_names):  
            tableau = np.delete(tableau, var, axis=1)
            del column_names[var]
    return tableau, column_names, row_names


def transition_to_phase2(tableau, c, column_names, tableaux_history):
    num_vars = len(c)
    num_rows, num_cols = tableau.shape
    c_extended = np.zeros(num_cols - 1)
    c_extended[:num_vars] = -c  
    tableau[-1, :-1] = c_extended
    tableaux_history.append(tableau.copy())  
    for col_idx in range(num_cols - 1):
        col_values = tableau[:-1, col_idx]  
        if np.count_nonzero(col_values) == 1 and np.sum(col_values) == 1:
            row_idx = np.where(col_values == 1)[0][0]  
            factor = tableau[-1, col_idx]  
            tableau[-1, :] -= factor * tableau[row_idx, :]  
            tableaux_history.append(tableau.copy())  
    return tableau


def two_phase_simplex(c, A, b, constraint_types, is_max):
    tableau, column_names, row_names, artificial_vars, tableaux_history = create_first_tableau(c, A, b, constraint_types, is_max, "twophase")
    solution, phase1_value, phase1_tableaux = simplex_with_visualization(tableau, column_names, row_names, False, tableaux_history)
    if phase1_value is None or abs(phase1_value) > 1e-6:
        print("No feasible solution or problem is unbounded.")
        return None, None, phase1_tableaux  
    tableau, column_names, row_names = remove_artificial_variables(tableau, artificial_vars, column_names, row_names, tableaux_history)
    tableau = transition_to_phase2(tableau, c, column_names, tableaux_history)
    solution, objective_value, phase2_tableaux = simplex_with_visualization(tableau, column_names, row_names, is_max, tableaux_history)
    return solution, objective_value, phase1_tableaux + phase2_tableaux
