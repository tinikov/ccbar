#!/usr/bin/env python3

import argparse
import numpy as np
from iminuit import Minuit
from iminuit.cost import LeastSquares

# Parsers
parser = argparse.ArgumentParser(prog="mc-fit", description="Fit charm quark masses")
parser.add_argument(
    "-s", "--ssize", type=int, required=True, help="spacial size of lattice"
)
parser.add_argument(
    "-a", "--a", type=np.float64, required=True, help="interval between lattices"
)
parser.add_argument(
    "-c", "--cutoff", type=np.float64, required=True, help="lattice cutoff"
)
parser.add_argument("ifname", nargs="+", type=str, help="file list for fit")
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

a = args.a
cutoff = args.cutoff * 1000

rmin = args.range[0]
rmax = args.range[1]
if rmin >= rmax or rmin < 0 or rmax > 3**0.5 * n * a:
    print("Please check the range for fit! ")
    exit(1)

N_df = len(args.ifname)


# Define Gaussian functions
def gaussian(x, A, B, C):
    return A * np.exp(-(x**2) / B) + C


def gaussian2(x, A1, B1, A2, B2, C):
    return gaussian(x, A1, B1, 0) + gaussian(x, A2, B2, 0) + C


para = {
    "A1": -1,
    "B1": 10,
    "A2": -10,
    "B2": 1,
    "C": 1,
}

if N_df == 1:
    print("\n#################################################")
    print("[[TEST FIT]] (to test the fit range)")
    print("    Fit range: ({}, {}) [fm]".format(rmin, rmax))

    # Make data
    rawdata = np.loadtxt(args.ifname[0], dtype=np.float64)[0:array_length]

    mask = (rawdata[:, 0] > rmin / a) & (rawdata[:, 0] < rmax / a)
    subdata = rawdata[mask]
    sorted_indices = np.argsort(subdata[:, 0])

    fitdata = subdata[sorted_indices]

    fitsites = fitdata[:, 0]
    fitfks = fitdata[:, 1]
    fiterr = fitdata[:, 2]

    # Fit
    least_squares = LeastSquares(fitsites, fitfks, fiterr, gaussian2)
    m = Minuit(least_squares, **para)
    m.migrad()

    # Print result
    df = np.shape(fitdata)[0] - 5 - 1
    print("mc     = {} [MeV]".format(m.values["C"] * cutoff))
    print("χ^2/df = {} ".format(m.fval / df))
else:
    mc_arr = []

    for ifname in args.ifname:
        rawdata = np.loadtxt(ifname, dtype=np.float64)[0:array_length]

        mask = (rawdata[:, 0] > rmin / a) & (rawdata[:, 0] < rmax / a)
        subdata = rawdata[mask]
        sorted_indices = np.argsort(subdata[:, 0])

        fitdata = subdata[sorted_indices]
        fitsites = fitdata[:, 0]
        fitfks = fitdata[:, 1]
        fiterr = fitdata[:, 2]

        least_squares = LeastSquares(fitsites, fitfks, fiterr, gaussian2)
        m = Minuit(least_squares, **para)
        m.migrad()

        mc_arr.append(m.values["C"])

    mc_arr = np.array(mc_arr)
    mc_mean = np.mean(mc_arr)
    mc_var = np.sqrt(np.var(mc_arr) * (N_df - 1) / N_df)

    print("{} {}".format(mc_mean * cutoff, mc_var * cutoff))
