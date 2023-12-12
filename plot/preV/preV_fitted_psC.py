#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares

codeRoot = "/Users/chen/LQCD/code/ccbar"

rmin = 3
rmax = 12

t = 28
t = str(t).rjust(2, "0")

# Gauge
path = "{}/fig/preV/coulomb".format(codeRoot)
if not os.path.exists(path):
    os.makedirs(path)

datapath = "{}/result/c4pt/preV".format(codeRoot)


# Define Cornell potential
def cornell(r, A, sigma, V0):
    return -A / r + sigma * r + V0


para = {
    "A": 1,
    "sigma": 0.1,
    "V0": 0.01,
}

# Font setting
font = {
    "family": "Charter",
    "size": 8,
    "mathfamily": "stix",
}

plt.rcParams["font.family"] = font["family"]
plt.rcParams["font.size"] = font["size"]
plt.rcParams["mathtext.fontset"] = font["mathfamily"]

# Fit
rawdata = np.loadtxt("{}/ps/txt.{}".format(datapath, t), dtype=np.float64)

mask = (rawdata[:, 0] > rmin) & (rawdata[:, 0] < rmax)
subdata = rawdata[mask]
sorted_indices = np.argsort(subdata[:, 0])

fitdata = subdata[sorted_indices]

fitsites = fitdata[:, 0]
fitprev = fitdata[:, 1]
fiterr = fitdata[:, 2]

# Fit
least_squares = LeastSquares(fitsites, fitprev, fiterr, cornell)  # type: ignore
m = Minuit(least_squares, **para)  # type: ignore
m.migrad()

# Draw
style = {
    "fmt": "x",
    "markersize": 1.7,
    "markeredgewidth": 0.3,
    "linewidth": 0.3,
}

fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

ax.errorbar(rawdata[:, 0], rawdata[:, 1], rawdata[:, 2], label="data", **style)
x_fit = np.arange(0.01, 28, 0.01)
ax.plot(
    x_fit,
    cornell(x_fit, *m.values),
    linewidth=0.75,
    label="fit",
)

ax.minorticks_on()
legend_default_style = {
    # "handletextpad": 0,
    "frameon": False,
    "fontsize": 7,
    "labelspacing": 0.1,
}
ax.legend(loc=4, **legend_default_style)

ax.set_xlabel(r"$n_r$", labelpad=-1)
ax.set(xlim=(0, 13))

ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$", labelpad=-0.1)
ax.set(ylim=(-1, 0.4))

fig.subplots_adjust(left=0.17, right=0.97, bottom=0.13, top=0.96)
fig.savefig("{}/ps_fit{}.png".format(path, t), dpi=600)
plt.close()
