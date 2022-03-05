"""
CSCI 6511 - Artificial Intelligence - Spring 2022
GWU - Dr. Amrinder
Author: Charles Peeke
"""
import time
import collections

# Global Variables
DOMAIN_SIZE = 0
CONSTRAINT_SIZE = 0
NUM_COLORS = 0
INCONSISTENT_VALS = 0

"""
Helper Functions
"""


def isAssignmentComplete(assignment):
    """
    Simple check to determine if the assignment is complete.
    All domain variables default to value -1 and change when assigned a color
    :param assignment: CSP Assignment State
    :return: Whether the assignment provided is complete or not
    """
    return -1 not in assignment


def generateSuccessors(constraints, assignment, vertex):
    """
    Generates successor states from constraints, the state assignments, and a given vertex
    :param constraints: List of constraints that need to be satisfied
    :param assignment: Current list of assigned variables/values
    :param vertex: Current vertex to assign/meet constraints
    :return: Collection of successors
    """
    possible_vals = []
    for adjacentVert in constraints[vertex]:
        # If the vertex is unassigned, it's a possible assignment
        if assignment[adjacentVert] != 1:
            possible_vals.append([adjacentVert, vertex])
    successors = collections.deque(possible_vals)
    return successors


def isLegal(vertex, assign_color, assignment, constraints):
    """
    Checks if any constraints are broken by the current assignment
    :param vertex: Variable for the assignment
    :param assign_color: Assigned color for the vertex
    :param assignment: Current list of assigned variables/values
    :param constraints: List of constraints that need to be satisfied
    :return: Boolean value if the current assignment is legal for the constraints
    """
    for constraint in constraints[vertex]:
        if assign_color == assignment[constraint]:
            return False
    return True


"""
Heuristics Section
"""


def findMRV(domain_vars, domain_vals):
    """
    Finds the vertex with the Minimum Remaining Values
    :param domain_vars: List of domain variables 
    :param domain_vals: List of domain values
    :return: The vertex with the minimum remaining values
    """
    min_values = NUM_COLORS + 1
    mrv_vertex = -1
    # Search all Nodes to find
    for i in range(DOMAIN_SIZE):
        if len(domain_vars[i]) < min_values and domain_vals[i] != 1:
            min_values = len(domain_vars[i])
            mrv_vertex = i
    return mrv_vertex


def calculateLCV(vertex, constraints, possible_vals):
    """
    Creates a priority list of the Least Constraining Values based on the possible values of the vertex
    :param vertex: Variable for the assignment
    :param constraints: List of constraints that need to be satisfied
    :param possible_vals: List of domain variables (vertices)
    :return: Prioritizes list of least to most constraining values for the given variable
    """
    lcv_list = []
    color_order = None
    # Search through all values of the vertex
    for dom_val in possible_vals[vertex]:
        minimum = 100
        for constraint_val in constraints[vertex]:
            temp = len(possible_vals[constraint_val])
            if dom_val in possible_vals[constraint_val]:
                temp -= 1
            if temp < minimum:
                minimum = temp
        lcv_list.append([dom_val, minimum])
        lcv_ordered = sorted(lcv_list, key=lambda c: c[1], reverse=True)
        color_order = [col[0] for col in lcv_ordered]
    return color_order


"""
Arc Consistency Section
"""


def verifyAC3(arc_list, constraints, domain_vars, domain_vals):
    """
    Verifies the list or arcs for the current state satisfy the constraints, and keep a consistent solution
    :param arc_list: List of arcs to check the consistency
    :param constraints: List of constraints that need to be satisfied
    :param domain_vars: List of domain variables
    :param domain_vals: List of domain values
    :return: Boolean if any arcs had inconsistent values and the domain was changed
    """
    while len(arc_list) != 0:
        popped = arc_list.popleft()
        removed, domain_vars = RemoveInconsistentValues(popped, domain_vars)
        if removed:
            if len(domain_vars[popped[0]]) == 0:
                return False, domain_vars
            constraints2 = [adj for adj in constraints[popped[0]] if adj != popped[1]]
            for j in constraints2:
                added = [j, popped[0]]
                if domain_vals[j] != 1:
                    arc_list.append(added)
    return True, domain_vars


def RemoveInconsistentValues(variable, domain_vals):
    """
    Function responsible for removing any inconsistent values from the variable given the possible values
    * Also, introduces a counter for any values that were inconsistent, to parallel the pruning ideas from lecture
    :param variable: Variable for the assignment
    :param domain_vals: Values for the variable assignment
    :return: Boolean if any inconsistent values were removed, and the new domain values based on this action
    """
    global INCONSISTENT_VALS
    removed = False
    if len(domain_vals[variable[1]]) == 1:
        c = domain_vals[variable[1]][0]
        if c in domain_vals[variable[0]]:
            domain_vals[variable[0]].remove(c)
            INCONSISTENT_VALS += 1
            removed = True
    return removed, domain_vals


"""
Main CSP Section
"""


def solveCSP(state, constraints, domain, assignment):
    """
    Backtracking algorithm for CSP problems
    Recursively assigns values to the domain variables,
    checks constraints, and determines the solution for the CSP
    :param state: CSP state
    :param constraints: List of Constraints for the CSP (edges)
    :param domain: List of domain variables (vertices)
    :param assignment: Assignment for the domain variables
    :return:
    """

    # Check if the current assignment is complete (Base Case)
    if isAssignmentComplete(assignment):
        return state

    # Find the Minimum Remaining Variable for current assignment
    vertex = findMRV(domain, assignment)
    if vertex is None:
        return -1

    # Order the Values in Least Constraining Value order for the variable
    vert_values = calculateLCV(vertex, constraints, domain)
    if vert_values is None:
        return -1

    # Attempt to assign each possible value to the LCV
    for val in vert_values:
        if isLegal(vertex, val, state, constraints):
            # Generate Successors for the CSP state
            successors = generateSuccessors(constraints, assignment, vertex)

            # Computer AC3 for the domain variable and values
            dom_copy = domain
            dom_copy[vertex] = [d for d in domain[vertex] if d == val]
            [removed, domain_list] = verifyAC3(successors, constraints, dom_copy, assignment)

            # Checks if AC3 removed any possible states
            if removed:
                state[vertex] = val
                assignment[vertex] = 1
                dom_copy = domain_list
                result = solveCSP(state, constraints, dom_copy, assignment)
                # If CSP completes, we backtrack
                if result != 0:
                    return result

        # Unassigned values from the AC3 tests
        state[vertex] = -1
        assignment[vertex] = -1
    return -1


def mainCSP(file_name):
    """
    The Main Driver for the CSP Coloring Problem.
    Given the input filename, creates the domain, constraints, domain values, and solves the problem
    * Can display the solution, as well as time, and statistics about the interaction AC3 has on the CSP states
    :param file_name: Location of the test data. Provided are some in the format of gc_"...".txt
    :return: Displays the resulting solution of the CSP
    """
    global DOMAIN_SIZE, CONSTRAINT_SIZE, NUM_COLORS, INCONSISTENT_VALS

    lines = readFile(file_name)
    constraints = getFileData(lines)
    init_domain, init_vals, init_state = create_initial_state()

    # Actual CSP Solving Function
    start_time = time.time()
    solution = solveCSP(init_state, constraints, init_domain, init_vals)
    finish_time = time.time()
    duration = finish_time - start_time

    # Display the resulting solution
    displaySolution(solution, constraints, duration,
                    display_solution=True, display_time=True,
                    display_stats=True, verify_csp=False)


"""
Initialization Section
"""


def create_initial_state():
    """
    Create the domain variables and possible values, and current assigned values
    :return: Initial Domain Variables and Values, and the assigned state of all variables
    """
    global DOMAIN_SIZE
    init_state = []
    init_assignment = []
    domain = []
    for i in range(DOMAIN_SIZE):
        init_assignment.append(-1)
        init_state.append(-1)
        domain.append([])
        create_domain_values(domain, i)
    return domain, init_assignment, init_state


def create_domain_values(domain, vert_ind):
    """
    Given the current domain and the vertex to initialize, create all possible values for the vertex
    :param domain: list of domain variables
    :param vert_ind: Index of the domain variable to initialize
    :return:
    """
    global NUM_COLORS
    for i in range(NUM_COLORS):
        domain[vert_ind].append(i + 1)


def createConstraints(lines, offset):
    """
    Create the constraint list from the lines in the file and the offset of the domain variables
    :param lines: Data from the input file
    :param offset: Indicator if the vertices started at 0 or 1
    :return: The constraint list from the file
    """
    global NUM_COLORS
    constraints = []
    initConstraintList(constraints)

    # Read the File Data
    for line in lines:
        # Checks for extra lines (end of file)
        if len(line) > 1:
            if line[0] == 'c' or line[0] == 'C':  # Num of colors specified on these lines
                c_info = line.strip().split("=")
                NUM_COLORS = int(c_info[1])
            elif line[0] != "#":  # Ignore Commented Lines
                constraintVertices = line.strip().split(",")
                x = int(constraintVertices[0]) - offset
                y = int(constraintVertices[1]) - offset
                constraints[x].append(y)
                constraints[y].append(x)
    return constraints


def initConstraintList(constraints):
    """
    Create the correct size for the constraints given the size of the domain (colors)
    * Similar to creating an adjacency table for the vertices
    :param constraints: List to be initialized
    :return:
    """
    global DOMAIN_SIZE
    for i in range(DOMAIN_SIZE):
        constraints.append([])


def calculateDomainSize(lines):
    """
    Find the size of the domain variables from the file data
    :param lines: File data in the form of read in lines
    :return: Offset from the domain (starting at vertex 0 or 1)
    """
    global CONSTRAINT_SIZE, DOMAIN_SIZE
    zeroStart = 0
    offset = 1
    # Read the File
    for line in lines:
        # Only care about lines with data, not commented, and not the color data
        if len(line) > 1 and line[0] != "#" and line[0] != 'c' and line[0] != 'C':
            CONSTRAINT_SIZE += 1
            constraintVertices = line.strip().split(",")
            start_vert = int(constraintVertices[0])
            end_vert = int(constraintVertices[1])
            if start_vert > DOMAIN_SIZE:
                DOMAIN_SIZE = start_vert
            if end_vert > DOMAIN_SIZE:
                DOMAIN_SIZE = end_vert
            if start_vert == 0 or end_vert == 0:
                zeroStart = 1
                offset = 0
    # Include an extra 1 to domain size if data starts at vertex 0
    DOMAIN_SIZE += zeroStart
    return offset


"""
File Reading Section
"""


def getFileData(lines):
    """
    Gets the Domain size, Domain values, and constraint list from the file
    :param lines: Lines read in from the file
    :return: The constraint list from the file
    """
    offset = calculateDomainSize(lines)  # Offset represents whether we found data starts at vertex 0 or vertex 1
    constraints = createConstraints(lines, offset)
    return constraints


def readFile(input_file):
    """
    Simply open the file, read in all the data, and close the filereader
    :param input_file: Location and name of the file
    :return: Data from the file in form of lines
    """
    file = open(input_file, 'r')
    lines = file.readlines()
    file.close()
    return lines


"""
Display Section
"""


def displaySolution(solution, constraints, duration,
                    display_solution=False, display_time=False,
                    display_stats=False, verify_csp=False):
    """
    Function to display the solution, time taken, and other statistics about the CSP Solver
    :param solution: List of the resulting assignments for the CSP
    :param constraints: List of the constraints for the CSP
    :param duration: Duration of the running time of the function (in MS)
    :param display_solution: Flag to display the solution values
    :param display_stats: Flag to display other stats about the CSP
    :param display_time: Flag to display the time taken for the CSP
    :param verify_csp: Flag to verify the solution assignment against the constraints
    :return:
    """
    print("========== Output ==========")

    if solution == -1:
        print("No Solution Found!")
        print(f"There are {DOMAIN_SIZE} vertices (domain size) "
              f"and {CONSTRAINT_SIZE} edges (constraints) "
              f"with {NUM_COLORS} colors (domain values).")
    else:
        print("Solution Found!")
        print(f"There are {DOMAIN_SIZE} vertices (domain size) "
              f"and {CONSTRAINT_SIZE} edges (constraints) "
              f"with {NUM_COLORS} colors (domain values).")

        if display_solution:
            print(f"Result: {len(solution)} \n\tLabels: {solution}")

        if verify_csp:
            verify_solution(constraints, solution)

    if display_time or display_stats:
        display_extra_stats(display_stats, display_time, duration)

    print("========== ------ ==========")


def verify_solution(constraints, solution):
    """
    Verify that the solution meets all constraints
    :param constraints: Constraints for the CSP
    :param solution: Given solution assignment for the variables
    :return:
    """
    satisfied = True
    for i in range(DOMAIN_SIZE):
        for j in constraints[i]:
            if solution[i] == solution[j]:
                satisfied = False
    print("Solution being checked according to constraints...")
    if satisfied:
        print("All Constraints are Satisfied!")
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Not all Constraints are Satisfied!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def display_extra_stats(display_inconsistencies, display_time, duration):
    """
    Display Extra Statistics about the CSP including run time and AC3 removed values
    :param display_inconsistencies: Flag to display AC3 removed inconsistencies
    :param display_time: Flag to display time taken for the CSP function
    :param duration: Run time for the CSP
    :return:
    """
    print("\n------ Extra Statistics: ------")
    if display_time:
        print(f"- TIME TAKEN: \t {duration:.8f} seconds!")
    if display_inconsistencies:
        print("- AC3 Inconsistencies: \t ", INCONSISTENT_VALS)
    print("------ ----- ----------- ------")


"""
Main Function
"""
if __name__ == "__main__":
    mainCSP("gc_78317100510400.txt")
