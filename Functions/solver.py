from simplex import *
from BigM import *
from twophase import *
from goal import *
import numpy as np
from tabulate import tabulate
from goal import *

import numpy as np

def transform_unrestricted_vars(A, c, unrestricted_vars):
    num_vars = len(A[0])
    var_names = [f"x{i+1}" for i in range(num_vars)] 
    for index in sorted(unrestricted_vars, reverse=True):
        index = int(index) 
        A = A.tolist()
        c = c.tolist()
        for i in range(len(A)):
            A[i].insert(index + 1, -A[i][index])
        c.insert(index + 1, -c[index])
        var_names.insert(index + 1, f"{var_names[index]}'")  
        A = np.array(A)
        c = np.array(c)
    return A, c, var_names


class LinearProgrammingSolver:
    def __init__(self, c, A, b, unrestricted_vars=None, constraint_types=None, method="simplex", objective="min", is_goal=False,
                 goal_coeffs=[], goal_rhs=[], goal_signs=[], priorities=[]):
        self.c = c
        self.A = A
        self.b = b
        self.unrestricted_vars = unrestricted_vars if unrestricted_vars.size >0 else []
        self.constraint_types = constraint_types if constraint_types else ["<="] * len(b)
        self.method = method.lower()
        self.maximize = objective.lower() == "max"
        self.tableau_steps = []
        self.is_goal=is_goal
        self.goal_coeffs = goal_coeffs
        self.goal_rhs=goal_rhs
        self.goal_signs=goal_signs
        self.goal_priorities = priorities
        self.A,self.c, self.var_names = transform_unrestricted_vars(self.A,self.c,self.unrestricted_vars)


    def solve(self):
        if self.is_goal==True:
            print('ANA FELGOAAAALLLLLL')

            goal_status, solution, tableaux = goal_programming(self.A, self.b, self.constraint_types,self.var_names ,self.goal_coeffs, self.goal_rhs, self.goal_signs, self.goal_priorities)
            self.tableau_steps = tableaux

            return goal_status, solution, tableaux  

        count = self.constraint_types.count(">=") + self.constraint_types.count("=")
        if count == 0:
            print("ana felsimplex")
            status,optimal_value, x_values, tableau_steps = simplex_method(self.c, self.A, self.b,self.constraint_types, self.maximize, self.var_names)
            self.tableau_steps = tableau_steps  
            return status,optimal_value, x_values, tableau_steps
        elif self.method == "bigm":
            print("ana fel BIG M")
            status,optimal_value, x_values, tableau_steps = big_m_method(self.c, self.A, self.b, self.constraint_types,  self.maximize,self.var_names)
            self.tableau_steps = tableau_steps  
            return status,optimal_value, x_values, tableau_steps
        elif self.method == "twophase":
            print("ana fel 2PHASE")
            status,optimal_value, x_values, tableau_steps = two_phase_simplex(self.c, self.A, self.b, self.constraint_types,  self.maximize,self.var_names)
            self.tableau_steps = tableau_steps  
            return status,optimal_value, x_values, tableau_steps    
        else:
            raise ValueError(f"Unknown method: {self.method}")
        



    def print_tableau_steps(self):
        """Prints all tableaux in a well-formatted manner for readability."""
        for i, step in enumerate(self.tableau_steps):
            print(f"\n{'='*20} Tableau {i+1} {'='*20}\n")
            tableau = step["tableau"]
            columns = step["columns"]
            rows = step["rows"]
            note = step.get("note", "")  ####### ahe ya John

            # Create a table with row names
            table_with_rows = [[rows[j]] + tableau[j] for j in range(len(rows))]

            # Print in table format
            print(note)                  ##### w dy kaman
            print(tabulate(table_with_rows, headers=[""] + columns, tablefmt="grid"))
            
        print("\n" + "="*50)