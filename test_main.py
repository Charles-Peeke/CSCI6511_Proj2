import main


def runTests():
    print("Begin Unit Testing")
    print("... --- ... --- ...")
    block1()
    print("... --- ... --- ...")
    block2()
    print("... --- ... --- ...")
    block3()
    print("... --- ... --- ...")
    print("End Unit Testing")


def block1():
    print("Testing Block 1")

    results = [
        block1_unittest_1(),
        block1_unittest_2(),
        block1_unittest_3(),
        block1_unittest_4(),
        block1_unittest_5(),
        block1_unittest_6(),
        block1_unittest_7(),
        block1_unittest_8(),
        block1_unittest_9(),
        block1_unittest_10()]

    if False not in results:
        print("All Unit Tests Passed")
    else:
        print("At Least one Unit Test Failed")
        print(results)
    print("Finished Block 1")


def block1_unittest_1():
    print('Test 1')
    assignment = [-1, -1, -1]
    res = main.isAssignmentComplete(assignment)
    return res is False


def block1_unittest_2():
    print('Test 2')
    assignment = [-1, 1, 1]
    res = main.isAssignmentComplete(assignment)
    return res is False


def block1_unittest_3():
    print('Test 3')
    assignment = [1, 1, 1]
    res = main.isAssignmentComplete(assignment)
    return res is True


def block1_unittest_4():
    print('Test 4')
    assignment = [-1, -1, -1]
    res = main.isLegal(0, 2, assignment, [[0, 1], [1, 2]])
    return res is True


def block1_unittest_5():
    print('Test 5')
    assignment = [-1, 1, 1]
    res = main.isLegal(0, 2, assignment, [[0, 1], [1, 2]])
    return res is True


def block1_unittest_6():
    print('Test 6')
    assignment = [1, -1, 1]
    res = main.isLegal(1, 2, assignment, [[0, 1], [1, 2]])
    return res is True


def block1_unittest_7():
    print('Test 7')
    assignment = [-1, -1, -1]
    constraints = [[0, 1], [1, 2]]
    successors = main.generateSuccessors(constraints, assignment, 0)
    res = len(successors) > 0
    return res is True


def block1_unittest_8():
    print('Test 8')
    main.NUM_COLORS = 3
    dom = [[], []]
    main.create_domain_values(dom, 0)
    return (len(dom[0]) == 3 and
            len(dom[1]) == 0)


def block1_unittest_9():
    print('Test 9')
    main.NUM_COLORS = 4
    dom = [[1, 2, 3, 4], []]
    main.create_domain_values(dom, 1)
    return (len(dom[0]) == 4 and
            len(dom[1]) == 4)


def block1_unittest_10():
    print('Test 10')
    main.DOMAIN_SIZE = 3
    constraints = []
    main.initConstraintList(constraints)
    return (len(constraints) == 3 and
            len(constraints[0]) == 0)


def block2():
    print("Testing Block 2")

    results = [
        block2_unittest_1(),
        block2_unittest_2(),
        block2_unittest_3(),
        block2_unittest_4(),
        block2_unittest_5()]

    if False not in results:
        print("All Unit Tests Passed")
    else:
        print("At Least one Unit Test Failed")
        print(results)
    print("Finished Block 2")


def block2_unittest_1():
    print('Test 1')
    main.DOMAIN_SIZE = 4
    main.NUM_COLORS = 4
    dom_vars = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dom_vals = [-1, -1, -1, -1]
    res = main.findMRV(dom_vars, dom_vals)
    return res == 0


def block2_unittest_2():
    print('Test 2')
    main.DOMAIN_SIZE = 4
    main.NUM_COLORS = 4
    dom_vars = [[1, 3], [3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dom_vals = [-1, -1, -1, -1]
    res = main.findMRV(dom_vars, dom_vals)
    return res == 1


def block2_unittest_3():
    print('Test 3')
    vertex = 0
    constraints = [
        [1, 2],
        [1, 2],
        []
    ]
    possible_vals = [
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3]
    ]
    res = main.calculateLCV(vertex, constraints, possible_vals)
    return res == [0, 1, 2, 3]


def block2_unittest_4():
    print('Test 4')
    vertex = 0
    constraints = [
        [1, 2],
        [1, 2],
        []
    ]
    possible_vals = [
        [0, 1, 2, 3],
        [2, 3],
        [0, 3]
    ]
    res = main.calculateLCV(vertex, constraints, possible_vals)
    return res == [1, 0, 2, 3]


def block2_unittest_5():
    print('Test 5')
    vertex = 0
    constraints = [
        [1, 2],
        [1, 2],
        []
    ]
    possible_vals = [
        [0, 1, 2, 3],
        [2, 3],
        [0]
    ]
    res = main.calculateLCV(vertex, constraints, possible_vals)
    return res == [1, 2, 3, 0]


def block3():
    print("Testing Block 3")

    results = [
        block3_unittest_1(),
        block3_unittest_2()]

    if False not in results:
        print("All Unit Tests Passed")
    else:
        print("At Least one Unit Test Failed")
        print(results)
    print("Finished Block 3")


def block3_unittest_1():
    print('Test 1')
    variable = [11, 8]
    domain_vals = [[1], [2], [2], [3], [3], [4], [1], [4], [2, 3, 4], [2], [2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4],
                   [1, 2, 3, 4],
                   [1, 2, 3, 4], [1, 3], [1, 4]]

    removed, res = main.RemoveInconsistentValues(variable, domain_vals)
    return removed is False


def block3_unittest_2():
    print('Test 2')
    variable = [1, 2]
    domain_vals = [[1], [2], [2], [3], [3], [4], [1], [4], [2, 3, 4], [2], [2, 3, 4], [1, 2, 3, 4]]

    removed, res = main.RemoveInconsistentValues(variable, domain_vals)
    return removed is True


"""
Main Function
"""
if __name__ == "__main__":
    runTests()
