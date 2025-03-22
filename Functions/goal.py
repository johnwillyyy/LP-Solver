import numpy as np
from tabulate import tabulate

M = 1e6  # Arbitrary large value for penalization (Big M method)

def create_goal_programming_tableau(goal_coeffs, goal_rhs, goal_signs, 
                                    constraint_coeffs, constraint_rhs, constraint_signs):
    """
    Creates the initial tableau for a Goal Programming problem with slack, surplus, and artificial variables.
    Parameters:
    - goal_coeffs: 2D array where each row represents a goal constraint's coefficients.
    - goal_rhs: Array of right-hand side values for the goal constraints.
    - goal_signs: List of signs for the goal constraints (e.g., ['>=', '<=', '=']).
    - constraint_coeffs: 2D array of coefficients for the system constraints.
    - constraint_rhs: Array of right-hand side values for the system constraints.
    - constraint_signs: List of signs for the system constraints (e.g., ['<=', '>=', '=']).

    Returns:
    - tableau: The initial simplex tableau for the goal programming problem.
    - column_names: List of variable names (including decision variables, slack, surplus, artificial, and RHS).
    - row_names: List of row names for constraints (including goal and system constraints).
    """
    num_goals, num_vars = goal_coeffs.shape
    num_constraints = constraint_coeffs.shape[0]

    # Determine the number of additional variables
    num_slack = sum(1 for t in constraint_signs if t == "<=") 
    num_surplus = sum(1 for t in constraint_signs if t == ">=") 
    num_artificial = sum(1 for t in constraint_signs if t in [">=", "="]) 
    total_vars = num_vars + 2 * num_goals + num_slack + num_surplus + num_artificial

    # Initialize the extended tableau
    A_extended = np.zeros((num_goals + num_constraints, total_vars))
    A_extended[:num_goals, :num_vars] = goal_coeffs  # Add decision variable coefficients
    A_extended[num_goals:, :num_vars] = constraint_coeffs

    # Column names and indices
    column_names = [f"x{i+1}" for i in range(num_vars)]  # Decision variables
    slack_count, surplus_count, artificial_count, deviation_count = 1, 1, 1, 1
    artificial_vars = []

    # Add goal constraint variables
    j = num_vars
    for i, sign in enumerate(goal_signs):
    #     if sign == "<=":
    #         A_extended[i, j] = 1  # Slack variable
    #         column_names.append(f"s{slack_count}")
    #         slack_count += 1
    #         j += 1
    #     elif sign == ">=":
    #         A_extended[i, j] = -1  # Surplus variable
    #         column_names.append(f"sp{surplus_count}")
    #         surplus_count += 1
    #         j += 1
    #         A_extended[i, j] = 1  # Artificial variable
    #         column_names.append(f"a{artificial_count}")
    #         artificial_vars.append(j)
    #         artificial_count += 1
    #         j += 1
    #     elif sign == "=":
    #         A_extended[i, j] = 1  # Artificial variable
    #         column_names.append(f"a{artificial_count}")
    #         artificial_vars.append(j)
    #         artificial_count += 1
    #         j += 1

        # Add positive and negative deviation variables
        A_extended[i, j] = -1  # Positive deviation
        column_names.append(f"d+{deviation_count}")
        j += 1
        A_extended[i, j] = 1  # Negative deviation
        column_names.append(f"d-{deviation_count}")
        deviation_count += 1
        j += 1
    
    # Add system constraint variables
    for i, sign in enumerate(constraint_signs):
        row_idx = num_goals + i
        if sign == "<=":
            A_extended[row_idx, j] = 1  # Slack variable
            column_names.append(f"s{slack_count}")
            slack_count += 1
            j += 1
        elif sign == ">=":
            A_extended[row_idx, j] = -1  # Surplus variable
            column_names.append(f"sp{surplus_count}")
            surplus_count += 1
            j += 1
            A_extended[row_idx, j] = 1  # Artificial variable
            column_names.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
        elif sign == "=":
            A_extended[row_idx, j] = 1  # Artificial variable
            column_names.append(f"a{artificial_count}")
            artificial_vars.append(j)
            artificial_count += 1
            j += 1
    

    # Add RHS values
    rhs = np.concatenate([goal_rhs, constraint_rhs])
    column_names.append("RHS")
    tableau = np.column_stack((A_extended, rhs))

    # Generate row names
    row_names = [f"g{i+1}" for i in range(num_goals)]  # Goal rows
    row_names.extend([f"c{i+1}" for i in range(num_constraints)])  # System constraint rows
    # row_names.append("Z")  # Objective function row
    # [2,0,1]     
    # # Construct the objective function row
    # Z_row = np.zeros(total_vars)
    # for a_var in artificial_vars:
    #     Z_row[a_var] = M  # Penalize artificial variables in the objective
    # for i in range(num_goals):
    #     Z_row[num_vars + 2 * i] = 1  # Positive deviation
    #     Z_row[num_vars + 2 * i + 1] = 1  # Negative deviation
    # tableau = np.row_stack((tableau, np.append(Z_row, [0])))  # Add Z row to tableau

    return tableau, column_names, row_names


# Define input parameters
goal_coeffs = np.array([
    [200,0],
    [100,400],
    [0,250]
])
goal_rhs = [1000,1200,800]
goal_signs = ['>=', '>=', ">="]  # Types of goal constraints

constraint_coeffs = np.array([
    [15,30]
])
constraint_rhs = [150]
constraint_signs = [ '<=']  # Types of system constraints

# Create tableau
tableau, column_names, row_names = create_goal_programming_tableau(
    goal_coeffs, goal_rhs, goal_signs, constraint_coeffs, constraint_rhs, constraint_signs
)

# Display the tableau
print("Goal Programming Tableau:")
print(tabulate(tableau, headers=column_names, showindex=row_names, tablefmt="fancy_grid"))
