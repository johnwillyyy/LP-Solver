import numpy as np
from tabulate import tabulate

M = 1e6 


def create_first_tableau(c, A, b, constraint_types, vars_names, is_max=True, method=None,
                         goal_coeffs=[], goal_rhs=[], goal_signs=[], goal_constraints=False, priorities=[]):

    num_constraints, num_vars = A.shape
    if not is_max:
        c = -c

    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    num_goals = len(goal_coeffs) if goal_constraints else 0

    total_vars = num_vars + num_slack + num_surplus + num_artificial
    if goal_constraints:
        total_vars += 2 * num_goals 

    A_extended = np.zeros((num_constraints + num_goals, total_vars))
    if goal_constraints:
        A_extended[:num_goals, :num_vars] = goal_coeffs
        A_extended[num_goals:, :num_vars] = A
    else:
        A_extended[:num_constraints, :num_vars] = A


    column_names = vars_names.copy()
    slack_count, surplus_count, artificial_count, deviation_count = 1, 1, 1, 1
    artificial_vars = []
    basis = []

    j = num_vars
    if goal_constraints:
        for i in range(num_goals):
            A_extended[i, j] = -1  
            column_names.append(f"d{deviation_count}+")
            j += 1
            A_extended[i, j] = 1  
            column_names.append(f"d{deviation_count}-")
            basis.append(f"d{deviation_count}-")
            deviation_count += 1
            j += 1


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

    rhs = np.concatenate([goal_rhs, b]) if goal_constraints else b
    column_names.append("RHS")
    tableau = np.column_stack((A_extended, rhs))
    row_names = basis
    goal_m=False
    Z_rows = []
    if goal_constraints:
        for i, (sign, priority) in enumerate(zip(goal_signs, priorities)):
            Z_row = np.zeros(total_vars)
            if sign == ">=":
                Z_row[num_vars + 2 * i + 1] = 1  
                goal_m = False
            elif sign == "<=":
                Z_row[num_vars + 2 * i] = 1  
                goal_m = False
            Z_rows.append((priority, Z_row, f"G{i+1}"))

        Z_rows.sort(key=lambda x: x[0])  


    elif method in ["bigm", "twophase"]:
        goal_m = True
        if method == "bigm":
            c_extended = np.zeros(total_vars)
            c_extended[:num_vars] = -c
            for a_var in artificial_vars:
                c_extended[a_var] = M
        elif method == "twophase":
            c_extended = np.zeros(total_vars)
            for a_var in artificial_vars:
                c_extended[a_var] = 1  
        objective_row = np.append(c_extended, [0])  
        tableau = np.vstack((tableau, objective_row))
        row_names.append("Z")
    tableaux_history = []
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

    return tableau, column_names, row_names, artificial_vars, tableaux_history, Z_rows, goal_m


# # Example Usage
# c = np.array([3, 2])
# A = np.array([[1500, 3000]])
# b = np.array([15000])
# constraint_types = ['<=']
# vars_names = ['x1', 'x2']

# # Goal programming parameters
# goal_coeffs = np.array([
#     [200, 0],
#     [100, 400],
#     [0, 250]
# ])
# goal_rhs = [1000, 1200, 800]
# goal_signs = ['>=', '>=', '>=']
# priorities = [3, 2, 1]

# # Call the function
# tableau, column_names, row_names, artificial_vars, history, z_rows, goal_m = create_first_tableau(
#     c, A, b, constraint_types, vars_names, is_max=True, method="bigm",
#     goal_coeffs=goal_coeffs, goal_rhs=goal_rhs, goal_signs=goal_signs, goal_constraints=True, priorities=priorities
# )

# # Display the tableau
# print("Merged Goal Programming + LP Tableau:")
# print(tabulate(tableau, headers=column_names, showindex=row_names, tablefmt="fancy_grid"))
# print("z rows")
# print(z_rows)