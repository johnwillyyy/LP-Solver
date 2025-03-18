import numpy as np

# Function to perform pivot operation
def pivot(tableau, row, col):
    """Perform the pivot operation in Simplex Tableau."""
    tableau[row] = tableau[row] / tableau[row, col]
    for i in range(len(tableau)):
        if i != row:
            tableau[i] -= tableau[i, col] * tableau[row]
    return tableau

# Simplex algorithm implementation with enhanced visualization
def simplex_with_visualization(c, A, b, is_max=True):
    """Simplex algorithm that prints each iteration's tableau in the console.
    
    Args:
        c (array): Coefficients of the objective function.
        A (array): Coefficients of the constraints.
        b (array): Right-hand side of the constraints.
        is_max (bool): True for maximization problem, False for minimization problem.
        
    Returns:
        solution: Optimal values for the decision variables.
        objective_value: Optimal value of the objective function.
    """
    
    # Convert to maximization if minimizing (negate the objective function)
    if not is_max:
        c = -c
    
    # Add slack variables by extending A and c
    tableau = np.hstack((A, np.eye(len(A)), b.reshape(-1, 1)))  # Slack variables and RHS
    tableau = np.vstack((tableau, np.hstack((-c, np.zeros(len(b) + 1)))))  # Objective function row
    
    # Column names: X1, X2, ..., S1, S2, ..., RHS
    num_variables = A.shape[1]
    num_constraints = A.shape[0]
    column_names = [f"X{i+1}" for i in range(num_variables)] + [f"S{i+1}" for i in range(num_constraints)] + ["RHS"]
    
    # Row names: constraint rows (S1, S2, ...) and the objective row (Z)
    row_names = [f"S{i+1}" for i in range(num_constraints)] + ["Z"]
    
    # Initial tableau display before iterations
    solution, objective_value = None, None
    visualize_tableau(tableau, column_names, row_names, None, None, None, initial=True)

    iteration = 1  # Track iteration number
    
    while True:
        # Check if the solution is optimal (all coefficients in the objective row are non-negative)
        if np.all(tableau[-1, :-1] >= 0):
            break

        # Choose entering variable (pivot column)
        col = np.argmin(tableau[-1, :-1])
        entering_var = column_names[col]

        # Check for unbounded solution
        if np.all(tableau[:-1, col] <= 0):
            raise ValueError("Problem is unbounded")

        # Choose leaving variable (pivot row)
        ratios = np.full_like(tableau[:-1, -1], np.inf)  # Initialize with infinity
        non_zero_mask = tableau[:-1, col] > 0  # Mask to avoid division by zero
        ratios[non_zero_mask] = tableau[:-1, -1][non_zero_mask] / tableau[:-1, col][non_zero_mask]
        row = np.argmin(ratios)
        leaving_var = row_names[row]

        # Get the original pivot element value before row modification
        pivot_element = tableau[row, col]

        # Perform the pivot operation
        tableau = pivot(tableau, row, col)
        
        # Update row names based on the current basic variable position
        row_names[row] = entering_var  # Update leaving variable
        row_names[-1] = "Z"  # Keep the objective row name

        # Print the tableau for the current iteration
        visualize_tableau(tableau, column_names, row_names, row, col, iteration, entering_var, leaving_var, pivot_element)
        
        # Increase iteration count
        iteration += 1

    # Extract the solution from the tableau
    solution = np.zeros(c.shape)
    for i in range(len(solution)):
        if np.any(tableau[:-1, i] == 1) and np.all(tableau[:-1, i] >= 0):
            solution[i] = tableau[np.argmax(tableau[:-1, i]), -1]

    # For minimization, revert the sign of the objective value
    objective_value = tableau[-1, -1] if is_max else -tableau[-1, -1]
    print(f"Optimal solution: {solution}")
    print(f"Optimal objective value: {objective_value}") 
    return solution, objective_value

# Function to print the tableau with specified colors
def visualize_tableau(tableau, col_labels, row_labels, pivot_row, pivot_col, iteration, entering_var=None, leaving_var=None, pivot_element=None, initial=False):
    """Print the current tableau in the console for each iteration, with the pivot element highlighted."""
    
    print(f"\n{'='*40}")
    if initial:
        print(f"Initial Tableau (before iterations)")
    else:
        print(f"Simplex Tableau - Iteration {iteration}")
        print(f"Entering: {entering_var}, Leaving: {leaving_var}, Pivot Element: {pivot_element}")

    # Print the column headers
    print(f"{'':<10}", end="")
    for label in col_labels:
        print(f"{label:<10}", end="")
    print()

    # Print the rows with labels
    for row_label, row in zip(row_labels, tableau):
        print(f"{row_label:<10}", end="")
        for value in row:
            print(f"{value:<10.2f}", end="")
        print()
    print(f"{'='*40}")

# Example data
c_max = np.array([2, 3])
A_max = np.array([
    [1, 2],
    [4, 3]
])
b_max = np.array([6, 12])

# Solve the maximization problem and visualize iterations
simplex_with_visualization(c_max, A_max, b_max, is_max=True)
