#!/usr/bin/env python3

import argparse
import numpy as np
from scipy.optimize import curve_fit

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
parser.add_argument(
    "--init_val",
    type=np.float64,
    nargs=2,
    metavar=("A", "M"),
    default=(1.0, 1.0),
    help="initial values (A, M); (1.0, 1.0) by default",
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


def single_exp(n, A, M):
    return A * np.exp(-M * n)


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

    popt, pcov, infodict, errmsg, ier = curve_fit(
        single_exp, fitsites, fitcorr, sigma=fiterr, full_output=True
    )

    df = tmax - tmin - 2 - 1  # degree of freedom: (# of data) - (# of parameters) - 1
    chisq = np.sum(np.square(infodict["fvec"]))

    print("##  A      = {}".format(popt[0]))
    print("##  M      = {} (lattice unit)".format(popt[1]))
    print("##  χ^2/df = {}".format(chisq / df))
else:
    print("\n#################################################")
    print("##  FITTING HADRON MASS (lattice unit)")
    print("##  Total of data files:  {}".format(N_df))
    print("##  Fit range:            [{}, {}]".format(tmin, tmax))
    print("##  Fit func:             exp")

    A_arr, M_arr, chisq_arr = [], [], []
    file_index = 0

    for ifname in args.ifname:
        file_index += 1

        rawdata = np.loadtxt(ifname, dtype=np.float64)[0:n_t]
        corr = rawdata[:, 1]
        err = rawdata[:, 2]

        fitdata = rawdata[tmin:tmax]
        fitcorr = fitdata[:, 1]
        fiterr = fitdata[:, 2]

        print("##  Progress: ({}/{})".format(file_index, N_df), end="\r")
        popt, pcov, infodict, errmsg, ier = curve_fit(
            single_exp, fitsites, fitcorr, sigma=fiterr, full_output=True
        )

        A_arr.append(popt[0])
        M_arr.append(popt[1])
        chisq_arr.append(np.sum(np.square(infodict["fvec"])))

    print("##  Progress: ({}/{})\n".format(N_df, N_df))

    df = tmax - tmin - 2 - 1  # degree of freedom: (# of data) - (# of parameters) - 1

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
