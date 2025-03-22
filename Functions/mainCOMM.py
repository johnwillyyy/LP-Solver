from solver import LinearProgrammingSolver
from dataProcessing import *
import numpy as np


# c = np.array([6,1])
# A = np.array([[-1,3], [1,-3],[1,1]])
# b = np.array([6,6,1])
# constraint_types = ["<=","=", ">="]
# objective = "max"

# c = np.array([1, -1, 3] )
# A = np.array([
#     [1, 1,0],
#     [1,0,1],
#     [0,1,1]
# ])
# b = np.array([20,5,10])
# constraint_types = ["<=", "=",">="]
# method = "bigm"
# objective = "max"

def main(received_data):

    problem_type, objective_type, technique, objective_coefficients, constraint_coefficients, constraint_operators, constraint_rhs, goal_coefficients, goal_operators, goal_rhs, goal_priority_type, goal_weights, goal_priorities, unrestricted_variables = process_lp_data(received_data)
    # print(problem_type)
    # print(objective_coefficients)
    # print(objective_type)
    # print(technique)
    # print(constraint_coefficients)
    # print(constraint_operators)
    # print(constraint_rhs)
    # print(goal_coefficients)
    # print(goal_operators)
    # print(goal_rhs)
    # print(goal_priority_type)
    # print(goal_weights)
    # print(goal_priorities)

    solver = LinearProgrammingSolver(objective_coefficients, constraint_coefficients, constraint_rhs, constraint_types=constraint_operators, method=technique, objective=objective_type,unrestricted_vars=unrestricted_variables)
    optimal_value, solution, tableau_steps = solver.solve()
    print("\nOptimal Solution:", solution)
    print("Optimal Value:", optimal_value)
    solver.print_tableau_steps()
    return solution, optimal_value, tableau_steps
   
