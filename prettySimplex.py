import numpy as np
import pandas as pd

def pivot(tableau, row, col):
    """Perform the pivot operation in Simplex Tableau."""
    tableau[row] = tableau[row] / tableau[row, col]
    for i in range(len(tableau)):
        if i != row:
            tableau[i] -= tableau[i, col] * tableau[row]
    return tableau

def simplex_with_visualization(c, A, b, is_max=True):
    """Simplex algorithm that returns optimal values, objective value, and iteration details."""
    
    if not is_max:
        c = -c  
    tableau = np.hstack((A, np.eye(len(A)), b.reshape(-1, 1)))  
    tableau = np.vstack((tableau, np.hstack((-c, np.zeros(len(b) + 1)))))  
    num_variables = A.shape[1]
    num_constraints = A.shape[0]
    column_names = [f"X{i+1}" for i in range(num_variables)] + [f"S{i+1}" for i in range(num_constraints)] + ["RHS"]
    row_names = [f"S{i+1}" for i in range(num_constraints)] + ["Z"]
    iterations = []
    iteration = 1  

    while True:
        # Store current tableau
        iterations.append({
            "iteration": iteration - 1,  
            "tableau": tableau.copy(),
            "row_names": row_names.copy(),
            "column_names": column_names.copy(),
            "pivot_element": None,
            "entering": None,
            "leaving": None
        })
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
        pivot_element = tableau[row, col]
        tableau = pivot(tableau, row, col)
        row_names[row] = entering_var 
        iterations[-1].update({
            "pivot_element": pivot_element,
            "entering": entering_var,
            "leaving": leaving_var
        })
        iteration += 1

    solution = np.zeros(c.shape)
    for i in range(len(solution)):
        if np.any(tableau[:-1, i] == 1) and np.all(tableau[:-1, i] >= 0):
            solution[i] = tableau[np.argmax(tableau[:-1, i]), -1]
    optimal_value = tableau[-1, -1] if is_max else -tableau[-1, -1]
    return optimal_value, solution, iterations

# Example problem
c_max = np.array([5,-4,6,-8])
A_max = np.array([[1,2,2,4],[2,-1,1,2],[4,-2,1,-1]])
b_max = np.array([40,8,10])



optimal_value, values, iterations = simplex_with_visualization(c_max, A_max, b_max, is_max=False)

# Print optimal values
print(f"Optimal Objective Value: {optimal_value}")
print(f"Optimal Variable Values: {values}")

# Store and format iterations
tableau_logs = []

for it in iterations:
    iteration_info = f"\nIteration {it['iteration']}:\n"
    iteration_info += f"Pivot Element: {it['pivot_element']}, Entering: {it['entering']}, Leaving: {it['leaving']}\n"

    # Create formatted table
    df = pd.DataFrame(it['tableau'], index=it['row_names'], columns=it['column_names'])
    iteration_info += df.to_string()

    tableau_logs.append(iteration_info)

# Combine all iterations and print
final_output = "\n\n".join(tableau_logs)
print(final_output)

# # Save to file
# with open("simplex_iterations.txt", "w") as file:
#     file.write(final_output)
