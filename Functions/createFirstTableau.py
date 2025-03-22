import numpy as np
from tabulate import tabulate

M = 1e6  # Arbitrary large value for penalization (Big M method)

def create_first_tableau(c, A, b, constraint_types, vars_names, is_max=True, method=None,
                          goal_coeffs=[], goal_rhs=[], goal_signs=[], goal_constraints=False):

    num_constraints, num_vars = A.shape
    if not is_max:
        c = -c

    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])

    # Ensure num_goals is set to 0 when goal_constraints is False
    num_goals = 0
    if goal_constraints:
        num_goals = len(goal_coeffs)

    total_vars = num_vars + num_slack + num_surplus + num_artificial
    if goal_constraints:
        total_vars += 2 * num_goals  # Adding deviation variables for each goal

    # Correcting the number of rows in A_extended
    A_extended = np.zeros((num_constraints + num_goals, total_vars))
    A_extended[:num_constraints, :num_vars] = A  # Add decision variable coefficients for system constraints

    column_names = vars_names.copy()
    slack_count, surplus_count, artificial_count, deviation_count = 1, 1, 1, 1
    artificial_vars = []

    j = num_vars

    # Goal Programming Variables
    if goal_constraints:
        for i in range(num_goals):
            # Add deviation variables for goals
            A_extended[i, j] = -1  # Positive deviation (d+)
            column_names.append(f"d{deviation_count}+")
            j += 1
            A_extended[i, j] = 1  # Negative deviation (d-)
            column_names.append(f"d{deviation_count}-")
            deviation_count += 1
            j += 1

    # System Constraints
    for i, t in enumerate(constraint_types):
        row_idx = num_goals + i if goal_constraints else i
        if t == "<=":
            A_extended[row_idx, j] = 1  # Slack variable
            column_names.append(f"s{slack_count}")
            slack_count += 1
            j += 1
        elif t == ">=":
            A_extended[row_idx, j] = -1  # Surplus variable
            column_names.append(f"sp{surplus_count}")
            surplus_count += 1
            j += 1
            A_extended[row_idx, j] = 1  # Artificial variable
            column_names.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
        elif t == "=":
            A_extended[row_idx, j] = 1  # Artificial variable
            column_names.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1

    # RHS Values
    rhs = np.concatenate([goal_rhs, b]) if goal_constraints else b
    column_names.append("RHS")
    tableau = np.column_stack((A_extended, rhs))

    row_names = [f"g{i+1}" for i in range(num_goals)] if goal_constraints else []
    row_names.extend([f"c{i+1}" for i in range(num_constraints)])  # System constraints
    row_names.append("Z")

    # Objective Function Row (Big M or Phase 1 method)
    if method == "bigm":
        c_extended = np.zeros(total_vars)
        c_extended[:num_vars] = -c
        for a_var in artificial_vars:
            c_extended[a_var] = M  # Penalize artificial variables in Big M
        objective_row = np.append(c_extended, [0])
    else:
        phase1_c = np.zeros(total_vars)
        for a_var in artificial_vars:
            phase1_c[a_var] = 1  # Penalize artificial variables in Phase 1
        objective_row = np.append(phase1_c, [0])

    # Stack the objective row
    tableau = np.vstack((tableau, objective_row))
    
    # Add Z rows for Goal Programming
    if goal_constraints:
        Z_rows = []
        for i, sign in enumerate(goal_signs):
            Z_row = np.zeros(total_vars)
            if sign == ">=":
                Z_row[num_vars + 2 * i + 1] = 1  # Penalize the negative deviation (d-)
            elif sign == "<=":
                Z_row[num_vars + 2 * i] = 1  # Penalize the positive deviation (d+)
            print(Z_row)
            print('wefew')
            Z_rows.append(Z_row)

        # Add Z rows to the tableau
        # for Z_row in Z_rows:
        #     tableau = np.vstack((tableau, np.append(Z_row, [0])))  # Add the Z row to tableau
        #     row_names.append(f"Z{i+1}")  # Add the corresponding Z row name

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
            elif method == "twophase":
                tableau[-1, :] -= tableau[row_idx, :]  
            tableaux_history.append({
                "tableau": tableau.tolist(),  
                "columns": column_names,
                "rows": row_names.copy()
            })

    print("Merged Goal Programming + LP Tableau:")
    print(tabulate(tableau, headers=column_names, showindex=row_names, tablefmt="fancy_grid"))

    return tableau, column_names, row_names, artificial_vars, tableaux_history




# Define input parameters

# Define input parameters
c = np.array([3, 2])
A = np.array([
    [1, 2],
    [2, 1],
    [1, 1]
])
b = np.array([6, 6, 4])
constraint_types = ['<=', '>=', '=']
vars_names = ['x1', 'x2']

# Goal programming parameters
goal_coeffs = np.array([
    [200, 0],
    [100, 400],
    [0, 250]
])
goal_rhs = [1000, 1200, 800]
goal_signs = ['>=', '>=', '>=' ]

# Call the function
tableau, column_names, row_names,bb , bbfd = create_first_tableau(
    c, A, b, constraint_types, vars_names, is_max=True, method="bigm",
    goal_coeffs=goal_coeffs,goal_rhs=goal_rhs,goal_signs=goal_signs,goal_constraints=True
)

# Display the tableau
print("Merged Goal Programming + LP Tableau:")
print(tabulate(tableau, headers=column_names, showindex=row_names, tablefmt="fancy_grid"))
