#!/usr/bin/env python3

import argparse
import numpy as np
from iminuit import Minuit
from iminuit.cost import LeastSquares

parser = argparse.ArgumentParser(prog="M-fit", description="Fit hadron masses")
parser.add_argument(
    "-t", "--tsize", type=int, required=True, help="temporal size of lattice"
)
parser.add_argument(
    "-c", "--cutoff", type=np.float64, required=True, help="lattice cutoff"
)
parser.add_argument("ifname", nargs="+", type=str, help="file list for fit")
parser.add_argument(
    "-r",
    "--range",
    type=int,
    nargs=2,
    required=True,
    metavar=("MIN", "MAX"),
    help="fit range: [nt_min, nt_max]",
)
args = parser.parse_args()

tmin = args.range[0]
tmax = args.range[1]
n_t = args.tsize
if tmin >= tmax or tmin < 0 or tmax > n_t:
    print("Please check the range for fit! ")
    exit(1)
tsites = np.arange(0, n_t, 1)
fitsites = np.arange(tmin, tmax, 1)

N_df = len(args.ifname)


# Define functions for fit
def exp(n, A, M):
    return A * np.exp(-M * n)


para = {
    "A": 0.01,
    "M": 1.0,
}

if N_df == 1:
    print("\n#################################################")
    print("##  TEST FIT (to test the fit range) (LU)")
    print("##  Fit range:  [{}, {}]".format(tmin, tmax))
    print("##  Fit func:   exp\n")

    rawdata = np.loadtxt(args.ifname[0], dtype=np.float64)[0:n_t]
    corr = rawdata[:, 1]
    err = rawdata[:, 2]

    fitdata = rawdata[tmin:tmax]

    fitcorr = fitdata[:, 1]
    fiterr = fitdata[:, 2]

    # Fit
    least_squares = LeastSquares(fitsites, fitcorr, fiterr, exp)
    m = Minuit(least_squares, **para)
    m.migrad()

    # degree of freedom: (# of data) - (# of parameters) - 1
    df = tmax - tmin - 2 - 1
    print("##  A      = {}".format(m.values["A"]))
    print("##  M      = {} (lattice unit)".format(m.values["M"]))
    print("##  χ^2/df = {}".format(m.fval / df))
else:
    print("\n#################################################")
    print("##  FITTING HADRON MASS (lattice unit)")
    print("##  Total of data files:  {}".format(N_df))
    print("##  Fit range:            [{}, {}]".format(tmin, tmax))
    print("##  Fit func:             exp")

    A_arr, M_arr, chisq_arr = [], [], []
    file_index = 0

    for ifname in args.ifname:
        rawdata = np.loadtxt(ifname, dtype=np.float64)[0:n_t]
        file_index += 1

        corr = rawdata[:, 1]
        err = rawdata[:, 2]

        fitdata = rawdata[tmin:tmax]
        fitcorr = fitdata[:, 1]
        fiterr = fitdata[:, 2]

        # Fit
        print("##  Progress: ({}/{})".format(file_index, N_df), end="\r")
        least_squares = LeastSquares(fitsites, fitcorr, fiterr, exp)
        m = Minuit(least_squares, **para)
        m.migrad()

        A_arr.append(m.values["A"])
        M_arr.append(m.values["M"])
        chisq_arr.append(m.fval)

    print("##  Progress: ({}/{})\n".format(N_df, N_df))

    # degree of freedom: (# of data) - (# of parameters) - 1
    df = tmax - tmin - 2 - 1

    A_arr = np.array(A_arr)
    M_arr = np.array(M_arr)
    chisq_arr = np.array(chisq_arr) / df

    A_mean = np.mean(A_arr)
    M_mean = np.mean(M_arr)
    chisq_mean = np.mean(chisq_arr)

    A_var = np.sqrt(np.var(A_arr) * (N_df - 1) / N_df)
    M_var = np.sqrt(np.var(M_arr) * (N_df - 1) / N_df)
    chisq_var = np.sqrt(np.var(chisq_arr) * (N_df - 1) / N_df)

    cutoff = args.cutoff * 1000

    print("##  A      = {} ± {}".format(A_mean, A_var))
    print("##  M(LU)  = {} ± {}".format(M_mean, M_var))
    print("##  M      = {} ± {}".format(M_mean * cutoff, M_var * cutoff))
    print("##  χ^2/df = {} ± {}".format(chisq_mean, chisq_var))
