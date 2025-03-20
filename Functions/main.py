from solver import LinearProgrammingSolver
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

# c = np.array([4, 1]) 
# A = np.array([[3,1], [4,3],[1,2]])
# b = np.array([3,6,4])
# constraint_types = ["=", ">=","<="]
# unrestricted = np.array([]) 
# objective = "min"

c = np.array([1, 2,1]) 
A = np.array([[1, 1,1], [2, -5,1]])
b = np.array([7, 10])
constraint_types = ["=", ">="]
unrestricted= np.array([]) 
objective = "max"
print(A)
solver = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="bigm", objective=objective,unrestricted_vars=unrestricted)
optimal_value, solution, tableau_steps = solver.solve()
print("\nOptimal Solution:", solution)
print("Optimal Value:", optimal_value)
solver.print_tableau_steps() #beeeeeeeeekkhhhhhh
print("---------------------------------------------------------------------------------------------")
print("carcourrr")
solver1 = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method="twophase", objective=objective,unrestricted_vars=unrestricted)
optimal_value, solution, tableau_steps = solver1.solve()
print("\nOptimal Solution:", solution)
print("Optimal Value:", optimal_value)
solver1.print_tableau_steps()

