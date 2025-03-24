import numpy as np
from basicSimplex import *
from createFirstTableau import *


def remove_artificial_variables(tableau, column_names, row_names, artificial_vars):
    #print("\nDEBUG: Column Names Before Removing Artificial Vars:", column_names)
    artificial_vars_to_remove = [col for col in artificial_vars if f"a{col - len(column_names)}" not in row_names]
    tableau = np.delete(tableau, artificial_vars_to_remove, axis=1)
    column_names = [col for i, col in enumerate(column_names) if i not in artificial_vars_to_remove]
    #print("\nDEBUG: Column Names After Removing Artificial Vars:", column_names)
    return tableau, column_names



def transition_to_phase2(tableau, c, column_names, tableaux_history, is_max):
    """ Converts Phase 1 tableau into Phase 2 by updating the objective row. """
    num_vars = len(c)
    num_rows, num_cols = tableau.shape
    c_extended = np.zeros(num_cols - 1)
    c_extended[:num_vars] = -c  if is_max else c
    tableau[-1, :-1] = c_extended
    row_order = [f"x{i+1}" for i in range(num_rows - 1)]+["Z"] 
    tableaux_history.append({
        "tableau": tableau.copy().tolist(),  
        "columns": column_names[:],  
        "rows": row_order
    })
    #tableaux_history.append(tableau.copy())
    for col_idx in range(num_cols - 1):
        col_values = tableau[:-1, col_idx]  
        if np.count_nonzero(col_values) == 1 and np.sum(col_values) == 1:
            row_idx = np.where(col_values == 1)[0][0]  
            factor = tableau[-1, col_idx]  
            tableau[-1, :] -= factor * tableau[row_idx, :]
            tableaux_history.append({
                "tableau": tableau.copy().tolist(),  
                "columns": column_names[:],  
                "rows": row_order
            }) 
            #tableaux_history.append(tableau.copy())  
    return tableau


def two_phase_simplex(c, A, b, constraint_types, is_max,vars_names=None):
    """ Implements the Two-Phase Simplex method. """
    if vars_names is None:
        vars_names = [f"X{i+1}" for i in range(len(c))]  

    tableau, column_names, row_names, artificial_vars, tableaux_history,n = create_first_tableau(c, A, b, constraint_types,vars_names, is_max,"twophase")

    status,solution, phase1_value, phase1_tableaux = simplex_with_visualization(tableau, column_names, row_names, False, tableaux_history)

    if phase1_value is None :
        print("UNBOUNDED solution or problem is unbounded.")
        return "UNBOUNDED",None, None, phase1_tableaux  
    
    if abs(phase1_value) > 1e-6:
        return "INFEASIBLE ",None, None, phase1_tableaux  
    
    tableau, column_names = remove_artificial_variables(tableau, column_names, row_names, artificial_vars)
    tableaux_history.clear()
    tableau = transition_to_phase2(tableau, c, column_names, tableaux_history, is_max)
    status,solution, objective_value, phase2_tableaux = simplex_with_visualization(tableau, column_names, row_names, is_max, tableaux_history)
    return status,solution, objective_value, phase1_tableaux + phase2_tableaux
