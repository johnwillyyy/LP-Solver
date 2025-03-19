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
    c = np.array([1,2,1]) 
    A = np.array([[1, 1,1], [2, -5,1]])
    b = np.array([7, 10])

    constraint_types = ["=", ">="]


    objective = "max"
    solver = LinearProgrammingSolver(objective_coefficients, constraint_coefficients, constraint_rhs, constraint_types=constraint_operators, method=technique, objective=objective_type)
    optimal_value, solution, tableau_steps = solver.solve()
    print("\nOptimal Solution:", solution)
    print("Optimal Value:", optimal_value)
    solver.print_tableau_steps()
    return solution, optimal_value, tableau_steps
    # print("---------------------------------------------------------------------------------------------")
    # print("carcourrr")
    # solver1 = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="twophase", objective=objective)
    # optimal_value, solution, tableau_steps = solver1.solve()
    # print("\nOptimal Solution:", solution)
    # print("Optimal Value:", optimal_value)
    # solver1.print_tableau_steps()

