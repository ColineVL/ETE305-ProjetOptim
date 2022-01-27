import pulp
import matplotlib.pyplot as plt
import numpy as np

# a solution :
# minimisation problem
tprob = pulp.LpProblem("Test", pulp.LpMinimize)

# constants
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
]
capamax = 200  # max capacity of the battery
p1min, p1max = 0, 100  # production range
c1 = 50  # cost per unit

p2min, p2max = 10, 400
c2 = 100


# variables
## production
p1 = [pulp.LpVariable(f"p1_{t}", 0, p1max) for t in range(0, 24)]
p2 = [pulp.LpVariable(f"p2_{t}", 0, p2max) for t in range(0, 24)]

## on/off
on1 = [pulp.LpVariable(f"on1_{t}", cat=pulp.LpBinary) for t in range(0, 24)]
on2 = [pulp.LpVariable(f"on2_{t}", cat=pulp.LpBinary) for t in range(0, 24)]

## battery load
p1load = [pulp.LpVariable(f"p1load_{t}", 0, capamax) for t in range(0, 24)]


# constraints
p1load[0] = 0  # let's start empty
# p1load[0]=capamax # let's start full

for t in range(0, 24):
    tprob += p1[t] >= p1min * on1[t]
    tprob += p1[t] <= p1max * on1[t]
    tprob += p2[t] >= p2min * on2[t]
    tprob += p2[t] <= p2max * on2[t]

    tprob += p1[t] <= p1load[t]  # can not provide more than available
    tprob += p1[t] + p2[t] >= demand[t]  # must satify demand

for t in range(1, 24):  # load level beginning a step is based on the previous one
    tprob += p1load[t] == p1load[t - 1] - p1[t - 1] + (
        p1[t - 1] + p2[t - 1] - demand[t - 1]
    )


# objective
tprob += sum([p1[t] * c1 + p2[t] * c2 for t in range(0, 24)])


# display
from matplotlib import gridspec

assert pulp.LpStatus[tprob.solve()] == "Optimal"
p1res = [pulp.value(p1[t]) for t in range(0, 24)]
p2res = [pulp.value(p2[t]) for t in range(0, 24)]
ptot = [p1res[t] + p2res[t] for t in range(0, 24)]
p1al = [pulp.value(p1load[t]) for t in range(0, 24)]

# display results
fig = plt.figure(figsize=(15, 9))
spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[2, 1])

# display demand and production rates
fig.add_subplot(spec[0, 0])
plt.plot(demand, "k", linewidth=2.0, drawstyle="steps", label="demand")

plt.plot(p1res, "g", linewidth=1.0, drawstyle="steps", label="battery production")
plt.plot(p2res, "r", linewidth=1.0, drawstyle="steps", label="dispatchable production")

plt.plot(
    ptot,
    linewidth=1.0,
    drawstyle="steps",
    c="b",
    linestyle="--",
    zorder=2,
    label="total production",
)
plt.fill_between(
    range(0, 24),
    demand,
    ptot,
    step="pre",
    alpha=0.2,
    label="in excess production/charging",
)
plt.legend()


# display battery load
fig.add_subplot(spec[1, 0])
plt.bar(range(0, 24), p1al, label="battery load level")
plt.legend()

plt.waitforbuttonpress()

print(f"Total cost is {pulp.value(tprob.objective)}")
