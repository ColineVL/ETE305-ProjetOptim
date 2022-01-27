import matplotlib.pyplot as plt
import numpy as np


def graphical_interpretation():
    ax = plt.axes(frameon=False, aspect=1)
    plt.xlim(-0.2, 8), plt.ylim(-0.2, 8)
    x = np.arange(10)
    plt.plot((8 - x) / 2)
    plt.plot((8 - 2 * x), "g")
    plt.fill_between(x, (8 - x) / 2, 8 + 0 * x, alpha=0.2)
    plt.fill_between(x, (8 - 2 * x), 8 + 0 * x, color="g", alpha=0.2)
