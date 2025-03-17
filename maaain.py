from solver import LinearProgrammingSolver

def main():
    c = [3,2]
    A = [
       [2,1],
      [1,2]
    ]
    b = [9,9]
    unrestricted_vars = [1] 
    constraints = ["<=" ,"<="]
    #constraint_types = ["<=", ">=", "="]
    #c=[5,-4,6,-8]
    #A=[[1,2,2,4],[2,-1,1,2],[4,-2,1,-1]]
    #b=[40,8,10]
    #unrestricted_vars=[]
    #c=[3,4,1]
    #A=[[3,10,5],
    #   [5,2,8],
    #   [8,10,3]
    #]
    #b=[120,6,105]
    #unrestricted_vars = []
    print("ana zh2ttt")
    solver = LinearProgrammingSolver(c, A, b, unrestricted_vars ,method="simplex", objective="max")
    optimal_value, x_values,tableau = solver.solve()
    solver.print_tableau_steps() 
    print("\nOptimal value:", optimal_value)
    print("Optimal solution (x values):", x_values)

if __name__ == "__main__":
    main()



