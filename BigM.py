import scipy.optimize as opt
import numpy as np
import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

def big_m_method(c, A, b, constraint_types, maximize=False):
    M = 1e6  
    num_constraints, num_vars = A.shape
    if maximize:
        c = -np.array(c)  
    num_slack = sum(1 for t in constraint_types if t == "<=")
    num_surplus = sum(1 for t in constraint_types if t == ">=")
    num_artificial = sum(1 for t in constraint_types if t in [">=", "="])
    total_vars = num_vars + num_slack + num_surplus + num_artificial
    A_extended = np.zeros((num_constraints, total_vars))
    A_extended[:, :num_vars] = A
    slack_count = surplus_count = artificial_count = 0
    artificial_vars = []

    for i, t in enumerate(constraint_types):
        if t == "<=":
            A_extended[i, num_vars + slack_count] = 1
            slack_count += 1
        elif t == ">=":
            A_extended[i, num_vars + slack_count + surplus_count] = -1  
            surplus_count += 1
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count] = 1 
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count)
            artificial_count += 1
        elif t == "=":
            A_extended[i, num_vars + num_slack + num_surplus + artificial_count] = 1  
            artificial_vars.append(num_vars + num_slack + num_surplus + artificial_count)
            artificial_count += 1
    c_extended = np.zeros(total_vars)
    c_extended[:num_vars] = c 
    for a_var in artificial_vars:
        c_extended[a_var] = M 
    tableau_steps = []
    initial_tableau = np.column_stack((A_extended, b))
    objective_row = np.append(c_extended, [0])  
    initial_tableau = np.row_stack((initial_tableau, objective_row)) 
    tableau_steps.append(np.round(initial_tableau, 5))
    res = opt.linprog(c_extended, A_eq=A_extended, b_eq=b, method="simplex")
    if "tableau_steps" in res:
        for step in res["tableau_steps"]:
           tableau_steps.append(np.round(step, 5))
    optimal_value = np.round(-res.fun if maximize else res.fun, 5)
    x_values = np.round(res.x, 5)
    return optimal_value, x_values, tableau_steps



# c = [1, 2, 1]  
# A = np.array([
#     [1, 1, 1],
#     [2, -5, 1]
# ])
# b = [7, 10]
# constraint_types = ["=", ">="]
# opt_type = "max"

# solution, optimal_value, tableau_steps = big_m_method(c, A, b, constraint_types, opt_type)

# print("Optimal Solution:", solution)
# print("Optimal Value:", optimal_value)


# print("\n=== Tableau Steps ===")
# for i, step in enumerate(tableau_steps):
#     print(f"\nTableau at Step {i}:")
#     for row in step:
#         print("  ".join(f"{val:.5f}" for val in row))
