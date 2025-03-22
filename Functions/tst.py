from solver import LinearProgrammingSolver
import numpy as np
def main():
    # c = np.array([3,2])
    # A = np.array([
    #    [2,1],
    #   [1,2]
    # ])
    # b = np.array([9,9])
    # unrestricted= [1] 
    # constraints = ["<=" ,"<="]
    #constraint_types = ["<=", ">=", "="]
    # c=np.array([5,-4,6,-8])
    # A=np.array([[1,2,2,4],[2,-1,1,2],[4,-2,1,-1]])
    # b=np.array([40,8,10])
    # unrestricted=np.array([])
    # # c=np.array([3,4,1])
    # # A=np.array([[3,10,5],
    # #   [5,2,8],
    # #   [8,10,3]
    # # ])
    # # b=np.array([120,6,105])
    # # unrestricted=np.array([]) 
    
    c = np.array([3,2])
    A = np.array([
       [2,1],
      [1,2]
    ])
    b = np.array([9,9])
    unrestricted = np.array([1]) 

    print("ana zh2ttt")
    solver = LinearProgrammingSolver(c, A, b ,unrestricted_vars=unrestricted,method="simplex", objective="max")
    optimal_value, solution, tableau_steps = solver.solve()
    print("\nOptimal Solution:", solution)
    print("Optimal Value:", optimal_value)
    solver.print_tableau_steps()

if __name__ == "__main__":
    main()


