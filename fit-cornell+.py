#!/usr/bin/env python3

import argparse
import numpy as np

from iminuit import Minuit
from iminuit.cost import LeastSquares

from matplotlib import pyplot as plt
import scienceplots  # type: ignore

# Parsers
parser = argparse.ArgumentParser(
    prog="fit-cornell+", description="Fit the deviated Cornell potential"
)
parser.add_argument(
    "-s", "--ssize", type=int, required=True, help="spacial size of lattice"
)
parser.add_argument("ifname", type=str, help="data file for fit")
parser.add_argument(
    "-r",
    "--range",
    type=np.float64,
    nargs=2,
    required=True,
    metavar=("MIN", "MAX"),
    help="fit range: [n_min, n_max]",
)
args = parser.parse_args()

# Initialize
n = args.ssize
array_length = n**3

rmin = args.range[0]
rmax = args.range[1]
if rmin >= rmax or rmin < 0 or rmax > 3**0.5 * n:
    print("Please check the range for fit! ")
    exit(1)


# Define Cornell potential
def cornell_var(r, A, sigma, B, C, V0):
    return -A / r + r * sigma * np.exp(-B * r - C * r**2) + V0


para = {
    "A": 1,
    "sigma": 0.1,
    "B": 0.1,
    # "sigma2": 10,
    "C": 1,
    "V0": 0.01,
}

# print("\n#################################################")
print("Fit range: ({}, {})".format(rmin, rmax))

# Make data
rawdata = np.loadtxt(args.ifname, dtype=np.float64)[0:array_length]

mask = (rawdata[:, 0] > rmin) & (rawdata[:, 0] < rmax)
subdata = rawdata[mask]
sorted_indices = np.argsort(subdata[:, 0])

fitdata = subdata[sorted_indices]

fitsites = fitdata[:, 0]
fitprev = fitdata[:, 1]
fiterr = fitdata[:, 2]

# Fit
least_squares = LeastSquares(fitsites, fitprev, fiterr, cornell_var)  # type: ignore
m = Minuit(least_squares, **para)
m.migrad()

# Print result
# df = np.shape(fitdata)[0] - 3 - 1
# chi = np.float64(m.fval)
# print(
#     "Vpre(r) = -{}/r + {}r·exp(-{}r) + {}".format(
#         m.values["A"], m.values["sigma"], m.values["B"], m.values["V0"]
#     )
# )
# print("χ^2/df = {} ".format(chi / df))

# sns.set_theme()
plt.style.use("science")

style = {
    "fmt": "o",
    "markersize": 2,
    "markeredgewidth": 0.2,
    "linewidth": 0.2,
    "fillstyle": "none",
}


fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)

print(m.values)

x = np.linspace(0.1, 16, 1000)
y = cornell_var(x, *m.values)

ax.errorbar(
    rawdata[:, 0], rawdata[:, 1], rawdata[:, 2], color="tab:blue", label="raw", **style
)
ax.plot(x, y, linewidth=0.6, label="fit", color="r")

ax.minorticks_on()

ax.set(xlim=(0, 16))
ax.set_xlabel(r"$n_r$", labelpad=-1)
ax.set(ylim=(-0.7, 0.2))
ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$", labelpad=0.2)

legend_default_style = {
    "fontsize": 7,
    "labelspacing": 0.1,
}
ax.legend(loc=4, **legend_default_style)

fig.subplots_adjust(left=0.17, right=0.97, bottom=0.13, top=0.96)
fig.savefig("./test.png", dpi=600)
