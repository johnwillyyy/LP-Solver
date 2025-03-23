import numpy as np
from simplex3 import simplex_with_visualization
from createFirstTableau import create_first_tableau
from tabulate import tabulate

def solve_goal_programming(tableau, column_names, row_names, Z_rows, goal_m):

    tableaux_history = []  
    goal_status = []       
    goal_rows=[]
    solution =[]
    for priority, Z_row, goal_name in Z_rows:
        #print(f"\nProcessing Goal: {goal_name} (Priority {priority})")       
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
        
        for idx, step in enumerate(steps[1:]):
            tableaux_history.append({
                "tableau": step["tableau"],
                "columns": step["columns"],
                "rows": step["rows"]
            })
            
        
        goal_rows.append(tableau[-1, :])
        # print("carcour")
        # print(goal_rows[-1])
        z_row_final = tableau[-1, :]
        coefficients_positive = np.all(z_row_final[:-1] >= 0) 
        rhs_zero = z_row_final[-1] == 0 


        if coefficients_positive and rhs_zero:
            status = "Satisfied"
        else:
            status = "Not Satisfied"

        goal_status.append((goal_name, status))
        tableaux_history.pop()
        #print(f"Goal {goal_name}: {status}")
        solution = []
        for var in column_names:
            if var.startswith('x'):  
                if var in row_names:  
                    row_idx = row_names.index(var)
                    solution.append(tableau[row_idx, -1]) 
                else:  
                    solution.append(0)
    return  goal_status, solution,tableaux_history

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
    goal_status,solution,tableaux= solve_goal_programming(tableau, column_names, row_names, Z_rows, goal_m)  

    return  goal_status, solution,tableaux

def print_tableau(tableau_data, step_number):
    print(tabulate(tableau_data["tableau"], headers=tableau_data["columns"], showindex=tableau_data["rows"], tablefmt="grid"))

# Example Input
A = np.array([[25,50]])
b = np.array([80000])
constraint_types = ['<=']
vars_names = ['x1','x2']

# Goal programming parameters
goal_coeffs = np.array([
    [0.5,0.25],
    [3,5]
    
])
goal_rhs = np.array([700, 9000])
goal_signs = np.array(['<=','>='])
priorities = np.array([1,2])   



# Solve Goal Programming
goal_status, solution,tableaux = goal_programming(
    A, b, constraint_types, vars_names, goal_coeffs, goal_rhs, goal_signs, priorities
)

# Display all tableaus with statuses
for i, tableau_data in enumerate(tableaux):
    print_tableau(tableau_data, i + 1)
    
# Print final goal statuses
print("\nFinal Goal Status:")
for goal, status in goal_status:
    print(f"{goal}: {status}")

print("solution",solution)
