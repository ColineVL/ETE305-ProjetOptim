import pulp
import matplotlib.pyplot as plt

# demand expressed hour by hour
demand = [
    20,
    20,
    20,
    30,
    40,
    40,
    120,
    120,
    150,
    300,
    300,
    300,
    300,
    500,
    500,
    300,
    200,
    200,
    200,
    400,
    400,
    500,
    400,
    100,
]  # change the values so they are relevant to yours

# a solution :
# minimisation problem
tprob = pulp.LpProblem("Test", pulp.LpMinimize)

# constants
p1min = 0
p1max = 100
c1 = 50
p2min = 10
p2max = 400
c2 = 100

# variables
p1 = [pulp.LpVariable(f"p1_{t}", p1min, p1max) for t in range(0, 24)]
p2 = [pulp.LpVariable(f"p2_{t}", p2min, p2max) for t in range(0, 24)]
# capa=[pulp.LpVariable(f"capa_$t") for t in range(0,24)]

# constraints
for t in range(0, 24):
    tprob += p1[t] >= p1min
    tprob += p1[t] <= p1max
    tprob += p2[t] >= p2min
    tprob += p2[t] <= p2max

    tprob += p1[t] + p2[t] >= demand[t]

# objective
tprob += sum([p1[t] * c1 + p2[t] * c2 for t in range(0, 24)])

assert pulp.LpStatus[tprob.solve()] == "Optimal"

# a solution
p1res = [pulp.value(p1[t]) for t in range(0, 24)]
p2res = [pulp.value(p2[t]) for t in range(0, 24)]

plt.plot(demand, "b")
plt.plot(p1res, "g")
plt.plot(p2res, "r")

plt.waitforbuttonpress()
