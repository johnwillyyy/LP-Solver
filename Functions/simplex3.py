import numpy as np

def create_tableau(c, A, b, is_max):
    """Constructs the initial tableau with slack variables as a normal 2D array, keeping row and column names separately."""
    if not is_max:
        c = -c  
    num_variables = A.shape[1]
    num_constraints = A.shape[0]

    tableau = np.hstack((A, np.eye(num_constraints), b.reshape(-1, 1)))
    tableau = np.vstack((tableau, np.hstack((-c, np.zeros(num_constraints + 1)))))

    column_names = [f"X{i+1}" for i in range(num_variables)] + [f"S{i+1}" for i in range(num_constraints)] + ["RHS"]
    row_names = [f"S{i+1}" for i in range(num_constraints)] + ["Z"]

    return tableau, column_names, row_names


def pivot(tableau, row, col):
    """Perform the pivot operation in the Simplex Tableau stored as a 2D array."""
    
    # Normalize the pivot row
    tableau[row] /= tableau[row, col]
    
    # Perform row operations
    for i in range(len(tableau)):
        if i != row:
            tableau[i] -= tableau[i, col] * tableau[row]
    
    return tableau


def simplex_with_visualization(tableau, column_names, row_names, is_max, tableau_steps=[]):
    """Simplex algorithm storing tableaux as a list of dictionaries for visualization."""
    tableaux = [{"tableau": tableau.tolist(), "columns": column_names, "rows": row_names.copy()}]  
    iteration = 1

    while True:
        if (tableau[-1, :-1] >= 0).all():  
            break  
        
        col_idx = np.argmin(tableau[-1, :-1])  
        
        if (tableau[:-1, col_idx] <= 0).all():  
            print("Problem is unbounded. Returning None.")
            return None, None, tableaux  

        ratios = tableau[:-1, -1] / tableau[:-1, col_idx]
        ratios[tableau[:-1, col_idx] <= 0] = np.inf  
        row_idx = np.argmin(ratios)  

        tableau = pivot(tableau, row_idx, col_idx)

        row_names[row_idx] = column_names[col_idx]  

        tableaux.append({
            "tableau": tableau.tolist(),
            "columns": column_names,
            "rows": row_names.copy()
        })

        iteration += 1

    solution = np.zeros(len(column_names) - 1)
    for i, var_name in enumerate(column_names[:-1]):  
        if var_name in row_names:  
            solution[i] = tableau[row_names.index(var_name), -1]

    objective_value = tableau[-1, -1] if is_max else -tableau[-1, -1]
    
    return solution.tolist(), objective_value, tableaux


def simplex_method(c, A, b, is_max=True):
    tableau, column_names, row_names = create_tableau(c, A, b, is_max)
    return simplex_with_visualization(tableau, column_names, row_names, is_max)
