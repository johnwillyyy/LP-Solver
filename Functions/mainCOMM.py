from solver import LinearProgrammingSolver
from dataProcessing import *
from goal import *
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
    # print('ffffff')
    # print(goal_coefficients)
    # print(goal_operators)
    # print(goal_rhs)
    # print(goal_priority_type)
    # print(goal_weights)
    # print(goal_priorities)



    A = np.array([[25.,50.]])
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

    print(A)
    print(constraint_coefficients)
    if np.array_equal(A, constraint_coefficients):
        print('oofff')
    else:
        print('lolll')




    is_goal = False
    if problem_type == 'goal':
        is_goal = True

    


    solver = LinearProgrammingSolver(c=objective_coefficients, A=constraint_coefficients, b=constraint_rhs, constraint_types=constraint_operators, method=technique, objective=objective_type,unrestricted_vars=unrestricted_variables, is_goal=is_goal,
                                     goal_coeffs=goal_coefficients, goal_rhs=goal_rhs,goal_signs= goal_operators,priorities=goal_priorities)
    
    if is_goal:
        goal_status, solution,tableaux = solver.solve()
        return goal_status, solution, tableaux
    else:
        status,optimal_value, solution, tableaux = solver.solve()
        print("\nStatus:")
        print("\nOptimal Solution:", solution)
        print("Optimal Value:", optimal_value)
        solver.print_tableau_steps()
        return  status,solution,optimal_value, tableaux


   
