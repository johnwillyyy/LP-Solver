from BasicSimplex import simplex_solver
#from bigM import big_m_solver

class LinearProgrammingSolver:
    def __init__(self, c, A, b, unrestricted_vars=None, constraint_types=None, method="simplex", objective="min"):
        """
        c: Coefficients of the objective function
        A: Coefficients of constraints
        b: Right-hand side values of constraints
        unrestricted_vars: List of indices of unrestricted variables
        constraint_types: List of constraint types ('<=', '=', '>=')
        method: 'simplex' or 'bigm' (Big-M method)
        objective: 'min' or 'max'
        """
        self.c = c
        self.A = A
        self.b = b
        self.unrestricted_vars = unrestricted_vars if unrestricted_vars else []
        self.constraint_types = constraint_types if constraint_types else ["<="] * len(b)
        self.method = method.lower()
        self.maximize = objective.lower() == "max"
        self.tableau_steps = []

        self.transform_unrestricted_vars()
        #self.standardize_constraints()

    def transform_unrestricted_vars(self):
        for index in sorted(self.unrestricted_vars, reverse=True):
            index = int(index) 
            for row in self.A:
                row[index] = float(row[index]) 
                row.insert(index + 1, -row[index]) 
            self.c[index] = float(self.c[index]) 
            self.c.insert(index + 1, -self.c[index])


    def solve(self):
        if self.method == "simplex":
            optimal_value, x_values, tableau_steps = simplex_solver(self.c, self.A, self.b, self.maximize)
            self.tableau_steps = tableau_steps  
            return optimal_value, x_values, tableau_steps
        #elif self.method == "bigm":
        #   optimal_value, x_values, tableau_steps = big_m_solver(self.c, self.A, self.b, self.constraint_types, self.maximize)
        #  self.tableau_steps = tableau_steps  
        # return optimal_value, x_values, tableau_steps
        #elif self.method == "two-phase":
        #   optimal_value, x_values, tableau_steps = self.two_phase_simplex()
        #   self.tableau_steps = tableau_steps
        #   return optimal_value, x_values, tableau_steps
        else:
            raise ValueError(f"Unknown method: {self.method}")
       

    def print_tableau_steps(self):
        print("\n=== Tableau Steps ===")
        for i, step in enumerate(self.tableau_steps):          
            print(f"\nTableau at Step {i}:")
            for row in step:
               print("  ".join(f"{val:.5f}" for val in row))  
