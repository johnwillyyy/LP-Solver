from solver import LinearProgrammingSolver
from dataProcessing import *
from goal import *
import numpy as np


def main(received_data):

    problem_type, objective_type, technique, objective_coefficients, constraint_coefficients, constraint_operators, constraint_rhs, goal_coefficients, goal_operators, goal_rhs, goal_type,goal_priorities,goal_weights, unrestricted_variables = process_lp_data(received_data)

    is_goal = False
    if problem_type == 'goal':
        is_goal = True

    solver = LinearProgrammingSolver(c=objective_coefficients, A=constraint_coefficients, b=constraint_rhs, constraint_types=constraint_operators, method=technique, objective=objective_type,unrestricted_vars=unrestricted_variables, is_goal=is_goal,
                                     goal_coeffs=goal_coefficients, goal_rhs=goal_rhs,goal_signs= goal_operators,priorities=goal_priorities)
    print('zzzzz')
    print(goal_type)
    print(goal_weights)
    print(goal_priorities)
    if is_goal:
        goal_status, solution,tableaux = solver.solve()
        return "", goal_status, solution, tableaux
    
    else:
        status,optimal_value, solution, tableaux = solver.solve()
        # print("\nStatus:")
        # print("\nOptimal Solution:", solution)
        # print("Optimal Value:", optimal_value)
        return  status,solution,optimal_value, tableaux


   
