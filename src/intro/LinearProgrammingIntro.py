import pulp
from helperFunctions import graphical_interpretation
import matplotlib.pyplot as plt

"""
Linear programming introduction
"""

# First we create a new problem main variable
prob = pulp.LpProblem(
    "example", pulp.LpMaximize
)  # problem name, problem nature maximisation or minimisation

# We declare and name the variables
# **WARNING** All variables must have a different name
x = pulp.LpVariable(
    "x", 0, None
)  # name, lower bound, upper bound (None means unbounded)
y = pulp.LpVariable("y", 0, None)

# Add constraints to the problem (boolean expressions added to the main problem variable)
prob += x + 2 * y <= 8
prob += 2 * x + y <= 8

# If a numerical expression is added, it is interpreted as the objective function (must be unique, in case not, last one wins)
prob += x + y

# Then we solve it!
status = prob.solve()

# Check the status of the resolution
print(pulp.LpStatus[status])

graphical_interpretation()

# Now we get the optimal value
plt.plot([x.value()], [y.value()], "ro")
plt.waitforbuttonpress()

# By the way
print(f"x : {x.value()}, y : {y.value()}")
