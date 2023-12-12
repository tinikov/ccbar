#!/usr/bin/env python3

import argparse
import numpy as np
from iminuit import Minuit
from iminuit.cost import LeastSquares

# Parsers
parser = argparse.ArgumentParser(prog="fit-cornell", description="Fit the Cornell potential")
parser.add_argument("-s", "--ssize", type=int, required=True, help="spacial size of lattice")
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
rawdata = np.loadtxt(args.ifname, dtype=np.float64)[0:array_length]

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
chi = np.float64(m.fval)
print("Vpre(r) = -{}/r + {}r + {}".format(m.values["A"], m.values["sigma"], m.values["V0"]))
print("χ^2/df = {} ".format(chi / df))
