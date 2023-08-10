#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

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


def gaussian(x, A, B, C):
    return A * np.exp(-(x**2) / B) + C


def gaussian2(x, A1, B1, A2, B2, C):
    return gaussian(x, A1, B1, 0) + gaussian(x, A2, B2, 0) + C


gaussian2_model = Model(gaussian2)

params2 = gaussian2_model.make_params(
    A1=-1,
    B1=10,
    A2=-10,
    B2=1,
    C=1,
)

if N_df == 1:
    print("\n#################################################")
    print("[[TEST FIT]] (to test the fit range)")
    print("    Fit range: ({}, {}) [fm]".format(rmin, rmax))

    rawdata = np.loadtxt(args.ifname[0], dtype=np.float64)[0:array_length]

    mask = (rawdata[:, 0] > rmin / a) & (rawdata[:, 0] < rmax / a)
    subdata = rawdata[mask]
    sorted_indices = np.argsort(subdata[:, 0])

    fitdata = subdata[sorted_indices]
    fitsites = fitdata[:, 0]
    fitfks = fitdata[:, 1]
    fiterr = fitdata[:, 2]

    result = gaussian2_model.fit(fitfks, params2, x=fitsites, weights=1 / fiterr)
    print(result.fit_report())
    print("[[!!!]]")
    print("    mc     = {} [MeV]".format(result.best_values["C"] * cutoff))
    print("    χ^2/df = {} ".format(result.redchi))

    # style = {
    # "fmt": "x",
    # "markersize": 5,
    # "markeredgewidth": 0.5,
    # "linewidth": 0.5,
    # }
    # plt.errorbar(
    #     rawdata[:, 0] * a,
    #     rawdata[:, 1] * cutoff / 1000,
    #     rawdata[:, 2] * cutoff / 1000,
    #     **style,
    #     label="raw",
    # )
    # x_plot = np.arange(0, 28, 0.01)
    # plt.plot(x_plot * a, gaussian2(x_plot, **result.best_values) * cutoff / 1000, label="fit2")
    # plt.plot(x_plot * a, np.full(x_plot.shape, result.best_values["C"]) * cutoff / 1000, label="mc")
    # plt.xlim(0, 1.2)
    # plt.ylim(-12, 4)
    # plt.legend()
    # plt.show()
else:
    print("\n#################################################")
    print("##  CHARM QUARK MASS")
    print("##  Total of data files:  {}".format(N_df))
    print("##  Fit range:            ({}, {}) [fm]".format(rmin, rmax))
    print("##  Fit func:             2 Gaussians")

    mc_arr = []
    file_index = 0

    for ifname in args.ifname:
        file_index += 1

        rawdata = np.loadtxt(ifname, dtype=np.float64)[0:array_length]

        mask = (rawdata[:, 0] > rmin / a) & (rawdata[:, 0] < rmax / a)
        subdata = rawdata[mask]
        sorted_indices = np.argsort(subdata[:, 0])

        fitdata = subdata[sorted_indices]
        fitsites = fitdata[:, 0]
        fitfks = fitdata[:, 1]
        fiterr = fitdata[:, 2]

        print("##  Progress: ({}/{})".format(file_index, N_df), end="\r")
        result = gaussian2_model.fit(fitfks, params2, x=fitsites, weights=1 / fiterr)

        mc_arr.append(result.params["C"].value)

    print("##  Progress: ({}/{})\n".format(N_df, N_df))

    mc_arr = np.array(mc_arr)
    mc_mean = np.mean(mc_arr)
    mc_var = np.sqrt(np.var(mc_arr) * (N_df - 1) / N_df)

    print("##  mc = {} ± {}".format(mc_mean * cutoff, mc_var * cutoff))
