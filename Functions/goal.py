import numpy as np
from basicSimplex import *
from createFirstTableau import *
from tabulate import tabulate

def remove_duplicates(tableaux_history):
    unique_tableaux = []
    
    for item in tableaux_history:
        is_duplicate = any(
            existing_item['tableau'] == item['tableau'] and
            existing_item['columns'] == item['columns'] and
            existing_item['rows'] == item['rows']
            for existing_item in unique_tableaux
        )
        if not is_duplicate:
            unique_tableaux.append(item)
    return unique_tableaux

def solve_goal_programming(tableau, column_names, row_names, Z_rows, goal_constraints, weights=None):
    tableaux_history = []  
    goal_status = []       
    solution = []
    goal_rows=[]

    if weights is not None:
        print("caroooo")
        print("Weights:", weights)
        print("Goal Constraints:", goal_constraints)

        # if len(goal_constraints) != len(weights):
        #     raise ValueError("Mismatch: goal_constraints and weights must have the same length")

        # print("\nWeighted Goal Programming ")

        d_plus_indices = [i for i, name in enumerate(column_names) if name.endswith("+")]
        d_minus_indices = [i for i, name in enumerate(column_names) if name.endswith("-")]

        if len(d_plus_indices) < len(weights) or len(d_minus_indices) < len(weights):
            raise ValueError("Mismatch: Not enough deviation variable indices for the number of goals.")

        weighted_Z_row = np.zeros(tableau.shape[1])

        for goal_idx, weight in enumerate(weights):
            if goal_idx >= len(goal_constraints):
                raise IndexError(f"goal_idx {goal_idx} out of range for goal_constraints")

            if goal_constraints[goal_idx] == "<=":  
                weighted_Z_row[d_plus_indices[goal_idx]] = weight
            elif goal_constraints[goal_idx] == ">=":  
                weighted_Z_row[d_minus_indices[goal_idx]] = weight

        tableau = np.vstack((tableau, weighted_Z_row))
        row_names.append("z")

        tableaux_history.append({
            "tableau": tableau.tolist(),
            "columns": column_names,
            "rows": row_names.copy(),
        })

        for i, basic_var in enumerate(row_names[:-1]):  
            if basic_var in column_names:
                basic_col_idx = column_names.index(basic_var)
                pivot_value = tableau[i, basic_col_idx]
                if pivot_value != 0:
                    tableau[-1, :] -= (tableau[-1, basic_col_idx] / pivot_value) * tableau[i, :]

                tableaux_history.append({
                    "tableau": tableau.tolist(),
                    "columns": column_names,
                    "rows": row_names.copy(),
                })

        status, solution, objective_value, steps = simplex_with_visualization(
            tableau, column_names, row_names, is_max=False  
        )

        for step in steps:
            tableaux_history.append({
                "tableau": step["tableau"],
                "columns": step["columns"],
                "rows": step["rows"],
                "note": step.get("note", "")
            })

        solution = []
        for var in column_names:
            if var.startswith('x'):  
                if var in row_names:  
                    row_idx = row_names.index(var)
                    solution.append(tableau[row_idx, -1]) 
                else:  
                    solution.append(0)

        for goal_idx in range(len(weights)):
            goal_name = f"G{goal_idx+1}"

            d_minus_var = column_names[d_minus_indices[goal_idx]] if goal_constraints[goal_idx] == ">=" else None
            d_plus_var = column_names[d_plus_indices[goal_idx]] if goal_constraints[goal_idx] == "<=" else None

            if (d_minus_var and d_minus_var not in row_names) or (d_plus_var and d_plus_var not in row_names):
                goal_status.append((goal_name, "Satisfied"))
            else:
                goal_status.append((goal_name, "Not Satisfied"))

    else:
        print("\nPreemptive Goal Programming ")
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
            #print(tabulate(tableau, headers=column_names, showindex=row_names, tablefmt="grid"))


            for i, basic_var in enumerate(row_names[:-1]): 
                if basic_var in column_names:
                    basic_col_idx = column_names.index(basic_var)
                    if Z_row[basic_col_idx] != 0:  
                        tableau = pivot(tableau, i, basic_col_idx) 
                        tableaux_history.append({
                            "tableau": tableau.tolist(),
                            "columns": column_names,
                            "rows": row_names.copy(),
                        })

            status,solution, objective_value, steps = simplex_with_visualization(tableau, column_names, row_names, is_max=False,goal_rows=goal_rows)
            
            for idx, step in enumerate(steps[1:]):
                tableaux_history.append({
                    "tableau": step["tableau"],
                    "columns": step["columns"],
                    "rows": step["rows"],
                    "note": step["note"]
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
            # if(len(tableaux_history)>1):
            # tableaux_history.pop()
            #print(f"Goal {goal_name}: {status}")
            solution = []
            for var in column_names:
                if var.startswith('x'):  
                    if var in row_names:  
                        row_idx = row_names.index(var)
                        solution.append(tableau[row_idx, -1]) 
                    else:  
                        solution.append(0)
                
        # tableaux_history.pop()
        tableaux_history = remove_duplicates(tableaux_history)
    return  goal_status, solution,tableaux_history


def goal_programming(A, b, constraint_types, vars_names, goal_coeffs, goal_rhs, goal_signs, priorities=None, weights=None):
    # if weights is not None:
    #     priorities = None

    tableau, column_names, row_names, artificial_vars, history, Z_rows = create_first_tableau(
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

    goal_status, solution, tableaux = solve_goal_programming(
        tableau, column_names, row_names, Z_rows, goal_constraints=goal_signs,weights=weights
    )

    return goal_status, solution, tableaux



def print_tableau(tableau_data, step_number):
    print(tabulate(tableau_data["tableau"], headers=tableau_data["columns"], showindex=tableau_data["rows"], tablefmt="grid"))
