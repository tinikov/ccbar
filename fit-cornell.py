#!/usr/bin/env python3

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from iminuit import Minuit
from iminuit.cost import LeastSquares

# Parsers
parser = argparse.ArgumentParser(
    prog="fit-cornell", description="Fit the Cornell potential"
)
parser.add_argument(
    "-s", "--ssize", type=int, required=True, help="spacial size of lattice"
)
parser.add_argument(
    "-r",
    "--range",
    type=np.float64,
    nargs=2,
    required=True,
    metavar=("MIN", "MAX"),
    help="fit range: [n_min, n_max]",
)
parser.add_argument("-t", "--tsite", type=int, required=True, help="time slice for fit")
args = parser.parse_args()

# Initialize
n = args.ssize
array_length = n**3
codeRoot = "/Volumes/X6/work/ccbar"
t = args.tsite
t = str(t).rjust(2, "0")
ifname = "{}/result/c4pt/preV/ps/txt.{}".format(codeRoot, t)

rmin = args.range[0]
rmax = args.range[1]
if rmin >= rmax or rmin < 0 or rmax > 3**0.5 * n:
    print("Please check the range for fit! ")
    exit(1)


# Define Cornell potential
def cornell(r, A, sigma, V0):
    return -A / r + sigma * r + V0


para = {
    "A": 1,
    "sigma": 0.1,
    "V0": 0.01,
}

print("\n#################################################")
print("Fit range: ({}, {})".format(rmin, rmax))

# Make data
rawdata = np.loadtxt(ifname, dtype=np.float64)[0:array_length]

mask = (rawdata[:, 0] > rmin) & (rawdata[:, 0] < rmax)
subdata = rawdata[mask]
sorted_indices = np.argsort(subdata[:, 0])

fitdata = subdata[sorted_indices]

fitsites = fitdata[:, 0]
fitprev = fitdata[:, 1]
fiterr = fitdata[:, 2]

# Fit
least_squares = LeastSquares(fitsites, fitprev, fiterr, cornell)  # type: ignore
m = Minuit(least_squares, **para)
m.migrad()

# Print result
df = np.shape(fitdata)[0] - 3 - 1
chi = m.fval
print(
    "Vpre(r) = -{}/r + {}r + {}".format(
        m.values["A"], m.values["sigma"], m.values["V0"]
    )
)
print("χ^2/df = {} ".format(chi / df))  # type: ignore

# Draw
plt.style.use(["science", "nature"])
fig, ax = plt.subplots()

errbar_plot_style = {
    "fmt": ".",
    "markersize": 4,
    "markeredgewidth": 0.25,
    "linewidth": 0.25,
    "color": "tab:blue",
    # "markerfacecolor": "white",
    "fillstyle": "none",
}

plot_style = {
    "linewidth": 1,
    "color": "red",
}

legend_style = {
    "loc": 4,
    "handletextpad": 0,
    "labelspacing": 0.3,
}

ax.errorbar(
    rawdata[:, 0], rawdata[:, 1], rawdata[:, 2], label="data", **errbar_plot_style
)
x_fit = np.arange(0.01, 28, 0.01)
ax.plot(x_fit, cornell(x_fit, *m.values), label="fit", **plot_style)

ax.legend(**legend_style)

ax.set_xlabel(r"$n_r$")
ax.set_xlim(0, 15)

ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$")
ax.set_ylim(-1, 0.6)

# Gauge
path = "{}/fig/preV/coulomb".format(codeRoot)
if not os.path.exists(path):
    os.makedirs(path)

fig.savefig("{}/ps_fit{}.png".format(path, t), dpi=600)
plt.close()
