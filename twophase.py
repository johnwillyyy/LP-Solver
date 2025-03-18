import numpy as np
from simplex3 import simplex_with_visualization

def create_phase1_tableau(c, A, b, constraint_types,is_max):
    """Creates the initial Phase 1 tableau for the Two-Phase Simplex method."""
    if not is_max:
        c = -c 
    num_constraints, num_vars = A.shape
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

    # Objective function for Phase 1: Minimize sum of artificial variables
    phase1_c = np.zeros(total_vars)
    for a_var in artificial_vars:
        phase1_c[a_var] = 1 

    tableau = np.column_stack((A_extended, b))
    objective_row = np.append(phase1_c, [0])
    tableau = np.row_stack((tableau, objective_row))
    tableaux_history = [tableau.copy()]
    for i, a_var in enumerate(artificial_vars):
        tableau[-1, :] -= tableau[i, :]
        tableaux_history.append(tableau.copy())
    return tableau, column_names, row_names, artificial_vars, tableaux_history


def two_phase_simplex(c, A, b, constraint_types,is_max):
    tableau, column_names, row_names, artificial_vars,tableaux_history = create_phase1_tableau(c, A, b, constraint_types,is_max)
    solution, phase1_value, phase1_tableaux = simplex_with_visualization(tableau, column_names, row_names, tableaux_history)

    if abs(phase1_value) > 1e-6:
        print("No feasible solution.")
        return None, None, phase1_tableaux

    tableau = remove_artificial_variables(tableau, artificial_vars)
    column_names = [col for i, col in enumerate(column_names) if i not in artificial_vars]
    
    tableau[-1, :-1] = np.append(-c, [0]) 
    solution, objective_value, phase2_tableaux = simplex_with_visualization(tableau, column_names, row_names)
    
    return solution, objective_value, phase1_tableaux + phase2_tableaux


def remove_artificial_variables(tableau, artificial_vars):
    """Remove artificial variables from the tableau"""
    tableau = np.delete(tableau, artificial_vars, axis=1)
    return tableau


# c = np.array([1, 2,1])
# A = np.array([[1, 1,1], [2, -5,1]])
# b = np.array([7, 10])
# constraint_types = ["=", ">="]
# is_max = True
# solution, objective_value, tableaux = two_phase_simplex(c, A, b, constraint_types, is_max)
# print("\nFinal Solution:", solution)
# print("Optimal Objective Value:", objective_value)
# for i, t in enumerate(tableaux):
#     print(f"\nTableau at Iteration {i}:")
#     print(t)
