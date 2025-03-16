from solver import LinearProgrammingSolver

def main():
    #c = [3,2]
    #A = [
    #   [2,1],
    #  [1,2]
    #]
    #b = [9,9]
    #unrestricted_vars = [1] 
    #constraint_types = ["<=", ">=", "="]
    c=[5,-4,6,-8]
    A=[[1,2,2,4],[2,-1,1,2],[4,-2,1,-1]]
    b=[40,8,10]
    unrestricted_vars=[]
    solver = LinearProgrammingSolver(c, A, b, unrestricted_vars , method="simplex", objective="min")
    optimal_value, x_values,tableau = solver.solve()
    solver.print_tableau_steps() 
    print("\nOptimal value:", optimal_value)
    print("Optimal solution (x values):", x_values)

if __name__ == "__main__":
    main()



