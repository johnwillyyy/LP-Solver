import scipy.optimize as opt
import numpy as np
import warnings


warnings.simplefilter("ignore", category=DeprecationWarning)

def simplex_solver(c, A, b, maximize=False):
    num_vars = len(c)  
    num_constraints = len(b)  
    if maximize:
        c = [-ci for ci in c]
    slack_identity = np.eye(num_constraints)
    initial_tableau = np.hstack([A, slack_identity, np.array(b).reshape(-1, 1)])
    objective_row = np.array(c + [0] * (num_constraints + 1))  
    initial_tableau = np.vstack([initial_tableau, objective_row])
    tableau_steps = [np.round(initial_tableau, 5)] 
    res = opt.linprog(c, A_ub=A, b_ub=b, method="simplex")
    if "tableau_steps" in res:
        for step in res["tableau_steps"]:
           tableau_steps.append(np.round(step, 5))
    optimal_value = np.round(-res.fun if maximize else res.fun, 5)
    x_values = np.round(res.x, 5)
    return optimal_value, x_values, tableau_steps
