import numpy as np

def pivot(tableau, row, col):
    tableau[row] /= tableau[row, col] 
    for i in range(len(tableau)):
        if i != row:
            tableau[i] -= tableau[i, col] * tableau[row]  
    return tableau

def simplex_with_visualization(tableau, column_names, row_names, is_max=True, tableau_steps=[], goal_rows=[]):
    tableaux = tableau_steps.copy() if tableau_steps else []  

    if not tableau_steps:  
        tableaux.append({
            "tableau": tableau.copy().tolist(),
            "columns": column_names[:],
            "rows": row_names[:]
        })

    iteration = 1

    while True:
        if (tableau[-1, :-1] >= 0).all():  
            break  
        col_idx = np.argmin(tableau[-1, :-1])  
        entering = column_names[col_idx]
        if (tableau[:-1, col_idx] <= 0).all():  
            print("Problem is unbounded.")
            return "UNBOUNDED",None, None, tableaux  

        stop_due_to_goal = False
        for idx, goal_row in enumerate(goal_rows):
            if goal_row[col_idx] != 0: 
                print(f"Stopped due to non-zero element in goal row {idx}, column {col_idx}.")
                stop_due_to_goal = True
                tableaux.append({
                    "tableau": tableau.copy().tolist(),
                    "columns": column_names[:],
                    "rows": row_names[:],         
                    "note": "Stopped due to non-zero element in goal row {idx}, column {col_idx}"           
                })
                break

        if stop_due_to_goal:
            return "UNBOUNDED",None, None, tableaux

        ratios = tableau[:-1, -1] / tableau[:-1, col_idx]
        ratios[tableau[:-1, col_idx] <= 0] = np.inf 
        row_idx = np.argmin(ratios)  
        leaving = row_names[row_idx] 

        tableau = pivot(tableau, row_idx, col_idx)

        row_names[row_idx] = column_names[col_idx]  
        tableaux.append({
            "tableau": tableau.copy().tolist(),
            "columns": column_names[:],
            "rows": row_names[:],
            "note": f"Entering variable = {entering}, Leaving variable = {leaving}"
        })
        
        iteration += 1

    solution = np.zeros(len(column_names) - 1)
    for i, var_name in enumerate(column_names[:-1]):  
        if var_name in row_names:  
            solution[i] = tableau[row_names.index(var_name), -1]

    objective_value = tableau[-1, -1] if is_max else -tableau[-1, -1]
    
    return "OPTIMAL",solution.tolist(), objective_value, tableaux

