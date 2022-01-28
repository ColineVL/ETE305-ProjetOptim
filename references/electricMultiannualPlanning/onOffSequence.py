import pulp
import matplotlib.pyplot as plt
import numpy as np

demand = np.loadtxt("./references/electricMultiannualPlanning/demand.txt")

costs = np.array([20, 40])
power_max = np.array([400, 200])
power_min = np.array([50, 20])

# %load solutions/weekplan.py
# %load solutions/weekplan.py
# minimisation problem
tprob = pulp.LpProblem("Week", pulp.LpMinimize)

# constants
p1min, p2min = power_min
p1max, p2max = power_max
c1, c2 = costs
nbsteps = len(demand)

# variables

## production
p1 = [pulp.LpVariable(f"p1_{t}", 0, p1max) for t in range(0, nbsteps)]
p2 = [pulp.LpVariable(f"p2_{t}", 0, p2max) for t in range(0, nbsteps)]

## on/off
on1 = [pulp.LpVariable(f"on1_{t}", cat=pulp.LpBinary) for t in range(0, nbsteps)]
on2 = [pulp.LpVariable(f"on2_{t}", cat=pulp.LpBinary) for t in range(0, nbsteps)]


# constraints
for t in range(0, nbsteps):
    tprob += p1[t] >= p1min * on1[t]  # if 'on' produce at least min
    tprob += p1[t] <= p1max * on1[t]  # if 'on' produce at most max, if 'off' produce 0
    tprob += p2[t] >= p2min * on2[t]
    tprob += p2[t] <= p2max * on2[t]

    tprob += p1[t] + p2[t] >= demand[t]

for t in range(1, nbsteps - 1):
    tprob += on1[t] <= on1[t - 1] + on1[t + 1]
    tprob += on2[t] <= on2[t - 1] + on2[t + 1]

# objective
tprob += sum([p1[t] * c1 + p2[t] * c2 for t in range(0, nbsteps)])


# display
assert pulp.LpStatus[tprob.solve()] == "Optimal"
p1res = [pulp.value(p1[t]) for t in range(0, nbsteps)]
p2res = [pulp.value(p2[t]) for t in range(0, nbsteps)]

plt.plot(demand, "b")
plt.plot(p1res, "g")
plt.plot(p2res, "r")
plt.waitforbuttonpress()
