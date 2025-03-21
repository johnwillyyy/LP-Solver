import numpy as np
from tabulate import tabulate  

M = 1e6  

def create_first_tableau(c, A, b, constraint_types, vars_names,is_max=True, method=None):
    """Creates the initial tableau for the Big M method with correct variable order and unique names."""
    print("john")
    print(A)
    print(b)
    print(c)
    num_constraints, num_vars = A.shape
    if not is_max:
        c = -c  
    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    total_vars = num_vars + num_slack + num_surplus + num_artificial
    A_extended = np.zeros((num_constraints, total_vars))
    A_extended[:, :num_vars] = A  
    slack_count, surplus_count, artificial_count = 1, 1, 1
    artificial_vars = []
    column_names = vars_names
    j = num_vars
    basics = []
    
    for i, t in enumerate(constraint_types):
        if t == "<=":
            A_extended[i, j] = 1  
            column_names.append(f"s{slack_count}") 
            basics.append(f"s{slack_count}")
            slack_count += 1
            j += 1
        elif t == ">=":
            A_extended[i, j] = -1  
            column_names.append(f"sp{surplus_count}") 
            surplus_count += 1
            j += 1
            A_extended[i, j] = 1  
            column_names.append(f"a{artificial_count}")  
            basics.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
        elif t == "=":
            A_extended[i, j] = 1  
            column_names.append(f"a{artificial_count}") 
            basics.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
    column_names.append("RHS")  
    row_names = basics[:]  
    row_names.append("Z")  
    if method == "bigm":
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
    tableaux_history=[]

    tableaux_history.append({
                "tableau": tableau.tolist(),  
                "columns": column_names,
                "rows": row_names.copy()
            })
    for row_idx in range(num_constraints):  
        if any(A_extended[row_idx, a] == 1 for a in artificial_vars):  
            if method == "bigm":
                tableau[-1, :] -= M * tableau[row_idx, :] 
            else:
                tableau[-1, :] -= tableau[row_idx, :]  

            tableaux_history.append({
                "tableau": tableau.tolist(),  
                "columns": column_names,
                "rows": row_names.copy()
            })
    return tableau, column_names, row_names, artificial_vars, tableaux_history