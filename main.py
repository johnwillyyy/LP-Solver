from solver import LinearProgrammingSolver
import numpy as np

c = [1, -1, 3] 
A = np.array([
    [1, 1,0],
    [1,0,1],
    [0,1,1]
])
b = [20,5,10]
constraint_types = ["<=", "=",">="]
method = "bigm"
objective = "max"

solver = LinearProgrammingSolver(c, A, b, constraint_types=constraint_types, method=method, objective=objective)
optimal_value, solution, tableau_steps = solver.solve()
print("\nOptimal Solution:", solution)
print("Optimal Value:", optimal_value)
solver.print_tableau_steps()