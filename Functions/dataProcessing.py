import numpy as np

def process_lp_data(data):
    # Extract basic parameters
    problem_type = data.get("problemType", "")
    objective_type = data.get("objectiveType", "")
    technique = data.get("technique", "")
    objective_coefficients = np.array([float(x) for x in data.get("objectiveCoefficients", [])])
    
    # Extract constraints
    constraints = data.get("constraints", [])
    constraint_coefficients = np.array([[float(x) for x in c["coefficients"]] for c in constraints])
    constraint_operators = [c["operator"] for c in constraints]
    constraint_rhs = np.array([float(c["rhs"]) for c in constraints])
    
    # Extract goals
    goals = data.get("goals", [])
    goal_coefficients = np.array([[float(x) for x in g["coefficients"]] for g in goals]) if goals else np.array([])
    goal_operators = [g["operator"] for g in goals] if goals else []
    goal_rhs = np.array([float(g["rhs"]) for g in goals]) if goals else np.array([])
    
    # Extract goal properties
    goal_priorities = np.array([float(x) for x in data.get("goalPriorities", [])])
    goal_weights = np.array([float(x) for x in data.get("goalWeights", [])])

    goal_type = data.get("goalType","")
    # Extract unrestricted variables
    unrestricted_variables = np.array([int(x) for x in data.get("unrestrictedVariables", [])])
    
    return problem_type, objective_type, technique, objective_coefficients, constraint_coefficients, constraint_operators, constraint_rhs, goal_coefficients, goal_operators, goal_rhs, goal_type,goal_priorities,goal_weights, unrestricted_variables

# # Example usage
# data = {
#     "problemType": "normal",
#     "objectiveCoefficients": ["1", "2", "2"],
#     "objectiveType": "maximize",
#     "technique": "bigM",
#     "constraints": [
#         {"coefficients": ["1", "1", "1"], "operator": "<=", "rhs": "2"},
#         {"coefficients": ["5", "5", "5"], "operator": ">=", "rhs": "2"},
#         {"coefficients": ["27", "7", "7"], "operator": "=", "rhs": "3"}
#     ],
#     "goals": [],
#     "unrestrictedVariables": ["x2"],
#     "goalPriorityType": "weights",
#     "goalPriorities": [],
#     "goalWeights": []
# }

# problem_type, objective_type, technique, objective_coefficients, constraint_coefficients, constraint_operators, constraint_rhs, goal_coefficients, goal_operators, goal_rhs, goal_priority_type, goal_weights, goal_priorities, unrestricted_variables = process_lp_data(data)

# print(problem_type)
# print(objective_coefficients)
# print(objective_type)
# print(technique)
# print(constraint_coefficients)
# print(constraint_operators)
# print(constraint_rhs)
# print(goal_coefficients)
# print(goal_operators)
# print(goal_rhs)
# print(goal_priority_type)
# print(goal_weights)
# print(goal_priorities)
# print(unrestricted_variables)
