import numpy as np


def pivot(tableau, row, col):
    """Perform the pivot operation in Simplex Tableau."""
    tableau[row] = tableau[row] / tableau[row, col]
    for i in range(len(tableau)):
        if i != row:
            tableau[i] -= tableau[i, col] * tableau[row]
    return tableau


def create_tableau(c, A, b, is_max=True):
    """Constructs the initial tableau with slack variables.
    
    Args:
        c (array): Coefficients of the objective function.
        A (array): Coefficients of the constraints.
        b (array): Right-hand side of the constraints.
        is_max (bool): True for maximization, False for minimization.

    Returns:
        tableau (numpy array): The initial simplex tableau.
        column_names (list): Column labels for tracking variables.
        row_names (list): Row labels for tracking variables.
    """
    if not is_max:
        c = -c 
    num_variables = A.shape[1]
    num_constraints = A.shape[0]
    tableau = np.hstack((A, np.eye(num_constraints), b.reshape(-1, 1)))
    tableau = np.vstack((tableau, np.hstack((-c, np.zeros(num_constraints + 1)))))
    column_names = [f"X{i+1}" for i in range(num_variables)] + [f"S{i+1}" for i in range(num_constraints)] + ["RHS"]
    row_names = [f"S{i+1}" for i in range(num_constraints)] + ["Z"]
    return tableau, column_names, row_names


def simplex_with_visualization(tableau, column_names, row_names, tableau_steps=[]):
    """Simplex algorithm that prints and stores each iteration's tableau.

    Args:
        tableau (array): The initial simplex tableau.
        column_names (list): Column labels.
        row_names (list): Row labels.
        tableau_steps (list): Steps before starting Simplex (Big M eliminations).

    Returns:
        solution (array): Optimal values for the decision variables.
        objective_value (float): Optimal objective function value.
        tableaux (list of arrays): History of tableaus at each iteration.
    """
    
    
    tableaux = tableau_steps.copy() if tableau_steps else []  
    if not tableau_steps:  
        tableaux.append(tableau.copy())  
    iteration = 1  

    while True:
        if np.all(tableau[-1, :-1] >= 0):
            break
        col = np.argmin(tableau[-1, :-1])
        entering_var = column_names[col]
        if np.all(tableau[:-1, col] <= 0):
            raise ValueError("Problem is unbounded")
        ratios = np.full_like(tableau[:-1, -1], np.inf) 
        non_zero_mask = tableau[:-1, col] > 0 
        ratios[non_zero_mask] = tableau[:-1, -1][non_zero_mask] / tableau[:-1, col][non_zero_mask]
        row = np.argmin(ratios)
        leaving_var = row_names[row]
        tableau = pivot(tableau, row, col)
        row_names[row] = entering_var 
        tableaux.append(tableau.copy())
        iteration += 1
    solution = np.zeros(len(column_names) - 1)
    for i in range(len(solution)):
        if np.any(tableau[:-1, i] == 1) and np.all(tableau[:-1, i] >= 0):
            solution[i] = tableau[np.argmax(tableau[:-1, i]), -1]
    objective_value = tableau[-1, -1]
    return solution, objective_value, tableaux

def simplex_method(c,A,b,is_max=True):
    tableau, column_names, row_names = create_tableau(c,A,b,is_max)
    return simplex_with_visualization(tableau, column_names, row_names)

# # Example data
# c_max = np.array([5, -4, 6, -8])
# A_max = np.array([[1, 2, 2, 4], [2, -1, 1, 2], [4, -2, 1, -1]])
# b_max = np.array([40, 8, 10])

# # Preprocess the tableau
# tableau, column_names, row_names = create_tableau(c_max, A_max, b_max, is_max=False)

# # Solve the problem using the modified simplex function
# solution, objective_value, tableaux = simplex_with_visualization(tableau, column_names, row_names)

# # Print stored tableaus
# for i, t in enumerate(tableaux):
#     print(f"\nTableau at Iteration {i}:")
#     print(t)
