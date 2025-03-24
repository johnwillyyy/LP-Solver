from basicSimplex import *
from createFirstTableau import *

def simplex_method(c, A, b, constraint_types,is_max=True,vars_names=None):
    if vars_names is None:
        vars_names = [f"X{i+1}" for i in range(len(c))]  
    tableau, column_names, row_names = create_first_tableau(c, A, b,constraint_types,vars_names,is_max,"simplex")
    return simplex_with_visualization(tableau, column_names, row_names, is_max)