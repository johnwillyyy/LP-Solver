import numpy as np
M = 1e6 

def count_variable_types(constraint_types):
    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    return num_slack, num_surplus, num_artificial

def initialize_tableau(A, b, goal_coeffs, goal_rhs, goal_constraints, total_vars, num_goals):
    num_constraints, num_vars = A.shape
    A_extended = np.zeros((num_constraints + num_goals, total_vars))
    if goal_constraints:
        A_extended[:num_goals, :num_vars] = goal_coeffs
        A_extended[num_goals:, :num_vars] = A
    else:
        A_extended[:num_constraints, :num_vars] = A
    rhs = np.concatenate([goal_rhs, b]) if goal_constraints else b
    return A_extended, rhs

def add_goal_variables(A_extended, column_names, basis, num_goals, num_vars):
    j = num_vars
    deviation_count = 1
    for i in range(num_goals):
        A_extended[i, j] = -1  
        column_names.append(f"d{deviation_count}+")
        j += 1
        A_extended[i, j] = 1  
        column_names.append(f"d{deviation_count}-")
        basis.append(f"d{deviation_count}-")
        deviation_count += 1
        j += 1
    return j

def add_constraint_variables(A_extended, column_names, basis, constraint_types, goal_constraints, num_goals, num_vars):
    slack_count, surplus_count, artificial_count = 1, 1, 1
    artificial_vars = []
    j = num_vars
    for i, t in enumerate(constraint_types):
        row_idx = num_goals + i if goal_constraints else i
        if t == "<=":
            A_extended[row_idx, j] = 1
            column_names.append(f"s{slack_count}")
            basis.append(f"s{slack_count}")
            slack_count += 1
            j += 1
        elif t == ">=":
            A_extended[row_idx, j] = -1
            column_names.append(f"e{surplus_count}")
            surplus_count += 1
            j += 1
            A_extended[row_idx, j] = 1  
            column_names.append(f"a{artificial_count}")
            basis.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
        elif t == "=":
            A_extended[row_idx, j] = 1 
            column_names.append(f"a{artificial_count}")
            basis.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
    return artificial_vars

def create_objective_row(method, c, num_vars, total_vars, artificial_vars):
    c_extended = np.zeros(total_vars)
    if method == "simplex":
        c_extended[:num_vars] = -c
    elif method == "bigm":
        c_extended[:num_vars] = -c
        for a_var in artificial_vars:
            c_extended[a_var] = M  
    elif method == "twophase":
        for a_var in artificial_vars:
            c_extended[a_var] = 1  
    return np.append(c_extended, [0])

def create_first_tableau(c, A, b, constraint_types, vars_names, is_max=True, method=None,
                         goal_coeffs=[], goal_rhs=[], goal_signs=[], goal_constraints=False, priorities=[]):
    if not is_max:
        c = -c
    Z_rows=[]
    num_constraints, num_vars = A.shape
    num_slack, num_surplus, num_artificial = count_variable_types(constraint_types)
    num_goals = len(goal_coeffs) if goal_constraints else 0
    total_vars = num_vars + num_slack + num_surplus + num_artificial + (2 * num_goals if goal_constraints else 0)
    
    A_extended, rhs = initialize_tableau(A, b, goal_coeffs, goal_rhs, goal_constraints, total_vars, num_goals)
    column_names = vars_names.copy()
    basis = []
    j = num_vars
    
    if goal_constraints:
        j = add_goal_variables(A_extended, column_names, basis, num_goals, num_vars)
    
    artificial_vars = add_constraint_variables(A_extended, column_names, basis, constraint_types, goal_constraints, num_goals, num_vars)
    
    column_names.append("RHS")
    tableau = np.column_stack((A_extended, rhs))
    row_names = basis
    
    if method in ["bigm", "twophase", "simplex"]:
        objective_row = create_objective_row(method, c, num_vars, total_vars, artificial_vars)
        tableau = np.vstack((tableau, objective_row))
        row_names.append("Z")
    
    tableaux_history = [{"tableau": tableau.tolist(), "columns": column_names, "rows": row_names.copy()}]
    
    if method in ["bigm", "twophase"]:
        for row_idx in range(num_constraints):  
            if any(A_extended[row_idx, a] == 1 for a in artificial_vars):  
                tableau[-1, :] -= (1e6 if method == "bigm" else 1) * tableau[row_idx, :]  
                tableaux_history.append({"tableau": tableau.tolist(), "columns": column_names, "rows": row_names.copy()})
    
    if goal_constraints and priorities is not None and len(priorities) >= 1:
        Z_rows = []
        for i, (sign, priority) in enumerate(zip(goal_signs, priorities)):
            Z_row = np.zeros(tableau.shape[1])
            if sign == ">=":
                Z_row[num_vars + 2 * i + 1] = 1  
            elif sign == "<=":
                Z_row[num_vars + 2 * i] = 1  
            Z_rows.append((priority, Z_row, f"G{i+1}"))
        
        Z_rows.sort(key=lambda x: x[0])  
        sorted_z_tableau = np.vstack([z[1] for z in Z_rows])
        row_names = [z[2] for z in Z_rows] + row_names
        tableau = np.vstack((sorted_z_tableau, tableau))
    
    if method == "simplex":
        return tableau, column_names, row_names
    elif method in ["bigm", "twophase"]:
        return tableau, column_names, row_names, artificial_vars, tableaux_history
    else:
        return tableau, column_names, row_names, artificial_vars, tableaux_history,Z_rows