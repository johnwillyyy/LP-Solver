import numpy as np
from simplex3 import simplex_with_visualization
from createFirstTableau import create_first_tableau
from tabulate import tabulate

def solve_goal_programming(tableau, column_names, row_names, Z_rows, goal_m):

    tableaux_history = []  
    goal_status = []       
    goal_rows=[]
    for priority, Z_row, goal_name in Z_rows:
        print(f"\nProcessing Goal: {goal_name} (Priority {priority})")       
        if Z_row.shape[0] < tableau.shape[1]:
            Z_row = np.pad(Z_row, (0, tableau.shape[1] - Z_row.shape[0]))
        
        tableau = np.vstack((tableau, Z_row))
        row_names.append(goal_name)

        tableaux_history.append({
            "tableau": tableau.tolist(),
            "columns": column_names,
            "rows": row_names.copy(),
            
        })

        
        for i, basic_var in enumerate(row_names[:-1]): 
            if basic_var in column_names:
                basic_col_idx = column_names.index(basic_var)
                if Z_row[basic_col_idx] != 0:
                    tableau[-1, :] -= tableau[i, :] * Z_row[basic_col_idx]
                    tableaux_history.append({
                    "tableau": tableau.tolist(),
                    "columns": column_names,
                    "rows": row_names.copy(),
                    
                })
        solution, objective_value, steps = simplex_with_visualization(tableau, column_names, row_names, is_max=True if goal_m else False,goal_rows=goal_rows)
        
        for idx, step in enumerate(steps):
            tableaux_history.append({
                "tableau": step["tableau"],
                "columns": step["columns"],
                "rows": step["rows"]
            })
        
        # if solution is None:
        #     goal_status.append((goal_name, "Not satisfied"))
        #     print(f"Goal {goal_name} could not be satisfied (Unbounded problem).")
        #     continue

        goal_rows.append(tableau[-1, :])
        print("carcour")
        print(goal_rows[-1])
        z_row_final = tableau[-1, :]
        coefficients_positive = np.all(z_row_final[:-1] >= 0) 
        rhs_zero = z_row_final[-1] == 0 

        if coefficients_positive and rhs_zero:
            status = "Satisfied"
        else:
            status = "Not Satisfied"

        goal_status.append((goal_name, status))
        print(f"Goal {goal_name}: {status}")
        
        # tableaux_history.append({
        #     "tableau": tableau.tolist(),
        #     "columns": column_names,
        #     "rows": row_names.copy(),
        #     "goal_status": (goal_name, status)
        # })

    return tableaux_history, goal_status, solution

def goal_programming(A, b, constraint_types, vars_names, goal_coeffs, goal_rhs, goal_signs, priorities):
    tableau, column_names, row_names, artificial_vars, history, Z_rows, goal_m = create_first_tableau(
        c=np.zeros(A.shape[1]),
        A=A,
        b=b,
        constraint_types=constraint_types,
        vars_names=vars_names,
        is_max=True,
        method=None,
        goal_coeffs=goal_coeffs,
        goal_rhs=goal_rhs,
        goal_signs=goal_signs,
        goal_constraints=True,
        priorities=priorities
    )
    tableaux, goal_status, solution= solve_goal_programming(tableau, column_names, row_names, Z_rows, goal_m)
    return tableaux, goal_status, solution

# def print_tableau(tableau_data, step_number):
#     """
#     Print a formatted tableau with headers and an optional note.
#     """
#     note = tableau_data.get("note", f"Step {step_number}")
#     print(f"\n{note}:")
#     print(tabulate(tableau_data["tableau"], headers=tableau_data["columns"], showindex=tableau_data["rows"], tablefmt="grid"))

# # Example Input
# A = np.array([[25, 50]])
# b = np.array([80000])
# constraint_types = ['<=']
# vars_names = ['x1', 'x2']

# # Goal programming parameters
# goal_coeffs = np.array([
#     [0.50, 0.25],
#     [3, 5]
# ])
# goal_rhs = [700, 9000]
# goal_signs = ['<=', '>=']
# priorities = [1, 2]



# # Solve Goal Programming
# tableaux, goal_status, solution = goal_programming(
#     A, b, constraint_types, vars_names, goal_coeffs, goal_rhs, goal_signs, priorities
# )
# print("solution",solution)
# # Display all tableaus with statuses
# for i, tableau_data in enumerate(tableaux):
#     print_tableau(tableau_data, i + 1)
#     if "goal_status" in tableau_data:
#         print(f"Goal Status: {tableau_data['goal_status']}")

# # Print final goal statuses
# print("\nFinal Goal Status:")
# for goal, status in goal_status:
#     print(f"{goal}: {status}")