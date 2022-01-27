import pulp
import matplotlib.pyplot as plt
from helperFunctions import graphical_interpretation

"""
Mixed linear programming
"""

prob = pulp.LpProblem("example", pulp.LpMaximize)

x = pulp.LpVariable(
    "x", 0, None, cat=pulp.LpInteger
)  # cat continuous is the default, override it with integer
y = pulp.LpVariable(
    "y", 0, None, cat=pulp.LpInteger
)  # this is the only change to go from LP to MILP

prob += x + 2 * y <= 8
prob += 2 * x + y <= 8

prob += x + y

assert pulp.LpStatus[prob.solve()] == "Optimal"
print((pulp.value(x), pulp.value(y)))

graphical_interpretation()

# Admissible solutions
plt.plot(
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4],
    [0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 0],
    "go",
    alpha=0.5,
)

# Now we get the optimal value
plt.plot([x.value()], [y.value()], "ro")
plt.waitforbuttonpress()
