from solver import LinearProgrammingSolver
import numpy as np
from goal import *

c = np.array([3,4,1])
A = np.array([[3,10,5], [5,2,8],[8,10,3]])
b = np.array([120,6,105])
constraint_types = ["<=","<=", "<="]
unrestricted = np.array([])
objective = "max"

solver = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="simplex", objective=objective,unrestricted_vars=unrestricted)
status,optimal_value, solution, tableau_steps = solver.solve()

print("\nStatus:", status)
print("\nOptimal Solution:", solution)
print("Optimal Value:", optimal_value)
solver.print_tableau_steps() #beeeeeeeeekkhhhhhh

# #######unbounded example
# c = np.array([2, 2] )
# A = np.array([
#     [1, 2],
#     [1,1]
# ])
# b = np.array([5,3])
# constraint_types = [">=", ">="]
# unrestricted = np.array([]) 
# objective = "max"

# #####infeasible
# c = np.array([1,1] )
# A = np.array([
#     [1, 1],
#     [1,1]
# ])
# b = np.array([5,2])
# constraint_types = [">=", "<="]
# unrestricted = np.array([]) 
# objective = "max"


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
# unrestricted = np.array([]) 
# method = "bigm"
# objective = "max"

# c = np.array([4, 1]) 
# A = np.array([[3,1], [4,3],[1,2]])
# b = np.array([3,6,4])
# constraint_types = ["=", ">=","<="]
# unrestricted = np.array([]) 
# objective = "min"

# c = np.array([1, 2,1]) 
# A = np.array([[1, 1,1], [2, -5,1]])
# b = np.array([7, 10])
# constraint_types = ["=", ">="]
# unrestricted= np.array([]) 
# objective = "max"
# print(A)
# solver = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="bigm", objective=objective,unrestricted_vars=unrestricted)
# status,optimal_value, solution, tableau_steps = solver.solve()
# print("\n Status:", status)
# print("\nOptimal Solution:", solution)
# print("Optimal Value:", optimal_value)
# solver.print_tableau_steps() #beeeeeeeeekkhhhhhh




# print("---------------------------------------------------------------------------------------------")
# print("carcourrr")
# solver1 = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="twophase", objective=objective,unrestricted_vars=unrestricted)
# status,optimal_value, solution, tableau_steps = solver1.solve()
# print("\n Status:", status)
# print("\nOptimal Solution:", solution)
# print("Optimal Value:", optimal_value)
# solver1.print_tableau_steps()


