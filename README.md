# CSCI6511 : AI : Project 2

## Constraint Satisfaction Problem

### GWU - Spring 2022
* Author: Charles Peeke

The Idea behind any CSP is to search through the possible states of the CSP and determine at each step, what steps are valid (i.e. fit all constraints), and either continue towards a solution, or backtrack when there is no valid position to move to.

## The Problem:
#### ```Input: <filename>.txt```
```
# Information
# Labels
Colors = <int>
# Constraints
Vertex1, Vertex2
Vertex1, Vertex2
Vertex1, Vertex2
...
```

### Example Result:
```
========== Output ==========
Solution Found!
There are 17 vertices (domain size) and 45 edges (constraints) with 4 colors (domain values).
Result: 17 
	Labels: [1, 2, 2, 3, 3, 4, 1, 4, 2, 2, 3, 1, 3, 2, 4, 3, 1]

------ Extra Statistics: ------
- TIME TAKEN: 	 0.00068212 seconds!
- AC3 Inconsistencies: 	  39
------ ----- ----------- ------
========== ------ ==========
```

## Breakdown:

Within the CSP solver, the process is:
* Check if the CSP state is complete (all variables assigned)
* Select the variable with the minimum remaining values
* Select the least constraining value for the variable 
* Make the assignment and verify that the new state is valid
* Find all successors to the CSP state & eliminate any inconsistencies within the assignments

#### MRV (Minimum Remaining Variable):
The goal of MRV is to find the variable that contains the least options. This will ensure that variables that are very constrained will be assigned first to eliminate the need to explore more branches to discover an invalid assignment later on. 

If one variable is constrained to one value, it is very clear whether or not that value assignment will invalidate the CSP state.

#### LCV (Least Constraining Value):
The goal of LCV is to find the value which constrains the least amount of neighboring variables out of the possible values of a variable. In this implementation, instead of calculating the LCV once every time a new value was to be tested, we could use the constraints to find an ordering for the values. Since we only checked one variable at a time, the constraints would not change for the variable, and thus, we could use the same ordering for each possible assignment and resulting CSP state.

#### AC3:
Arc Consistency enables CSP solvers to more efficiently explore possible assignments before continually backtracking. Within each CSP state, the initial assignment is valid within the singular set of constraints for a single variable, but does not imply that all other constraints are met as the change "ripples" through the list of variables.

## Discussion: 

It was very interesting to add in the simple counter for the function that removes inconsistent values. After discussion of the algorithm in lecture, I was curious if there would be any real time save with these. Although it is tough to see since most of the examples run within miliseconds, comparing some examples with the examples from in class were really cool! AC3 Saves a lot of time as you scale up because it eliminates the inconsistent values that would "distract" the algirithm away from the optimal solution.