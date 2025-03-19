import numpy as np

M = 1e6 

def create_first_tableau(c, A, b, constraint_types, is_max=True, method=None):
    """Creates the initial tableau for the Big M method with correct variable order and unique names."""
    num_constraints, num_vars = A.shape
    if not is_max:
        c = -c 
    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    total_vars = num_vars + num_slack + num_surplus + num_artificial
    A_extended = np.zeros((num_constraints, total_vars))
    A_extended[:, :num_vars] = A  
    slack_count = 1
    surplus_count = 1
    artificial_count = 1
    artificial_vars = []
    column_names = [f"x{i+1}" for i in range(num_vars)]
    row_names = [f"Constraint {i+1}" for i in range(num_constraints)]

    for i, t in enumerate(constraint_types):
        if t == "<=":
            A_extended[i, num_vars + slack_count - 1] = 1  
            column_names.append(f"s{slack_count}") 
            slack_count += 1
        elif t == ">=":
            A_extended[i, num_vars + num_slack + surplus_count - 1] = -1  
            column_names.append(f"sp{surplus_count}") 
            surplus_count += 1
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count - 1] = 1  
            column_names.append(f"a{artificial_count}")  
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count - 1)
            artificial_count += 1
        elif t == "=":
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count - 1] = 1 
            column_names.append(f"a{artificial_count}") 
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count - 1)
            artificial_count += 1
    column_names.append("RHS")  
    
    if method =="bigm":
        c_extended = np.zeros(total_vars)
        c_extended[:num_vars] = -c  
        for a_var in artificial_vars:
            c_extended[a_var] = M    
        objective_row = np.append(c_extended, [0]) 
    else:
        phase1_c = np.zeros(total_vars)
        for a_var in artificial_vars:
            phase1_c[a_var] = 1  
        objective_row = np.append(phase1_c, [0])

    tableau = np.column_stack((A_extended, b)) 
    tableau = np.row_stack((tableau, objective_row))  
    tableaux_history = [tableau.copy()]
    for row_idx in range(num_constraints):  
        if any(A_extended[row_idx, a] == 1 for a in artificial_vars):  
            if method == "bigm":
                tableau[-1, :] -= M * tableau[row_idx, :] 
            else:
                tableau[-1, :] -= tableau[row_idx, :]  
            tableaux_history.append(tableau.copy())
    return tableau, column_names, row_names, artificial_vars, tableaux_history

