from numpy import random

def output(assignments):
    n = len(assignments)
    for queen in assignments:
        for _ in range(queen - 1):
            print('·', end=' ')
        print('♕', end=' ')
        for _ in range(n - queen):
            print('·', end=' ')
        print()

# N-Queens Problem
class CSP:
    def __init__(self, n):
        self.variables = list(range(n))
        self.domains = {var: list(range(1, n+1)) for var in self.variables}

## Backtracking
def recursive_backtracking(csp, assignment={x:None for x in range(8)}):
    if all(each != None for each in assignment.values()):
        return assignment
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = recursive_backtracking(csp, assignment)
            if result is not None:
                return result
            assignment[var] = None
    return None

## Ordering

### Random choice
def select_unassigned_variable(assignment, csp):
    unassigned = [var for var in csp.variables if assignment[var] is None]
    return random.choice(unassigned)

## Filtering

### Forward checking
def is_consistent(var, value, assignment):
    for var2, value2 in assignment.items():
        if value2 is None:
            continue
        if var2 == var:
            continue
        if not node_consistent(var, value, var2, value2):
            return False
    return True

def node_consistent(var1, value1, var2, value2):
    return value1 != value2 and abs(var1 - var2) != abs(value1 - value2)

def order_domain_values(var, assignment, csp):
    return csp.domains[var]


csp = CSP(8)
assignments = recursive_backtracking(csp)
output(list(assignments.values()))