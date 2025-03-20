import numpy as np
import numpy as np

def create_goal_programming_tableau(goal_coeffs, goal_rhs, goal_signs, 
                                    constraint_coeffs, constraint_rhs, constraint_signs):
    """
    Constructs the initial tableau for a goal programming problem.

    Parameters:
    - goal_coeffs: 2D array where each row represents a goal constraint's coefficients.
    - goal_rhs: Array representing the right-hand side values of goals.
    - goal_signs: List of operator signs for goals (e.g., ['>=', '<=', '=']).
    - constraint_coeffs: 2D array for standard constraint coefficients.
    - constraint_rhs: Array for constraint right-hand side values.
    - constraint_signs: List of constraint operator signs (e.g., ['>=', '<=']).

    Returns:
    - tableau: The initial simplex tableau
    - column_names: Column names including decision, slack, and deviation variables
    - row_names: Row names labeled as deviation variables for goals and standard constraints
    """

    num_variables = goal_coeffs.shape[1]
    num_goals = goal_coeffs.shape[0]
    num_constraints = constraint_coeffs.shape[0]

    # Initialize deviation variables (d+ and d- for every goal)
    d_plus = np.zeros((num_goals, num_goals))
    d_minus = np.zeros((num_goals, num_goals))

    # Column names start with decision variables
    column_names = [f"X{i+1}" for i in range(num_variables)]

    # Add deviation variable columns (both d+ and d- for all goals)
    for i in range(num_goals):
        column_names.append(f"d{i+1}+")
        column_names.append(f"d{i+1}-")

    # Assign deviation variables based on goal signs & name the row after the active deviation variable
    row_names = []
    for i, sign in enumerate(goal_signs):
        if sign == ">=":
            d_minus[i, i] = 1  # Active deviation variable d-
            d_plus[i, i] = -1  # Inactive deviation variable d+
            row_names.append(f"d{i+1}-")  # Name row after active deviation variable
        elif sign == "<=":
            d_plus[i, i] = 1  # Active deviation variable d+
            d_minus[i, i] = -1  # Inactive deviation variable d-
            row_names.append(f"d{i+1}+")  # Name row after active deviation variable
        elif sign == "=":
            d_plus[i, i] = 1
            d_minus[i, i] = -1
            row_names.append(f"d{i+1}+")  # Can name after either, since both are active

    # Construct goal constraints section
    goal_table = np.hstack((goal_coeffs, d_plus, d_minus, goal_rhs.reshape(-1, 1)))

    # Slack variables for standard constraints
    slack_matrix = np.zeros((num_constraints, num_constraints))
    constraint_column_names = []

    for i, sign in enumerate(constraint_signs):
        if sign == "<=":
            slack_matrix[i, i] = 1  # Add slack variable
            constraint_column_names.append(f"S{i+1}")
        elif sign == ">=":
            slack_matrix[i, i] = 1  # Surplus variable (should be positive, not negative)
            constraint_column_names.append(f"S{i+1}")

    # Construct constraints section
    constraint_table = np.hstack((constraint_coeffs, slack_matrix, np.zeros((num_constraints, goal_table.shape[1] - num_variables - num_goals * 2)), constraint_rhs.reshape(-1, 1)))

    # Append constraint names to row names
    row_names.extend([f"C{i+1}" for i in range(num_constraints)])

    # Combine goals and constraints
    tableau = np.vstack((goal_table, constraint_table))

    # Construct Z-row for the objective function
    z_row = np.zeros(tableau.shape[1])

    goal_col_offset = num_variables  # Offset due to decision variables

    for i, sign in enumerate(goal_signs):
        if sign == ">=":
            z_row[goal_col_offset + (2 * i) + 1] = 1  # Minimize d-
        elif sign == "<=":
            z_row[goal_col_offset + (2 * i)] = 1  # Minimize d+
        elif sign == "=":
            z_row[goal_col_offset + (2 * i)] = 1  # Minimize d+
            z_row[goal_col_offset + (2 * i) + 1] = 1  # Minimize d-

    tableau = np.vstack((tableau, z_row))

    # Final column and row names
    column_names += constraint_column_names + ["RHS"]
    row_names.append("Z")

    return tableau, column_names, row_names


goal_coeffs = np.array([
    [1, 2],  # First goal equation
    [3, 1]   # Second goal equation
])

goal_rhs = np.array([10, 15])  # Goal target values
goal_signs = [">=", "<="]  # Goal conditions

constraint_coeffs = np.array([
    [2, 1],  # First constraint
    [1, 3]   # Second constraint
])

constraint_rhs = np.array([20, 30])  # Constraint RHS
constraint_signs = ["<=", ">="]  # Constraint signs

tableau, columns, rows = create_goal_programming_tableau(goal_coeffs, goal_rhs, goal_signs,
                                                         constraint_coeffs, constraint_rhs, constraint_signs)


print(columns)
print(rows)
print(tableau)