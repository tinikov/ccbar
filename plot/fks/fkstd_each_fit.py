#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
import scienceplots

plt.style.use(["science", "nature"])

a = 0.090713
a_invrs = 2.1753
codeRoot = "/Volumes/X6/work/ccbar"

tmin = 10
tmax = 28

rmin = 0.01
rmax = [0.82, 0.82]

path = [
    "{}/fig/FKS/coulomb-TD/each".format(codeRoot),
    "{}/fig/FKS/landau-TD/each".format(codeRoot),
]
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = [
    "{}/result/c4pt/FKS-TD".format(codeRoot),
    "{}/result/l4pt/FKS-TD".format(codeRoot),
]


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

# Font setting
font = {
    "family": "Charter",
    "size": 8,
    "mathfamily": "stix",
}

plt.rcParams["font.family"] = font["family"]
plt.rcParams["font.size"] = font["size"]
plt.rcParams["mathtext.fontset"] = font["mathfamily"]

yrange = [[1.5, 2.5], [1.1, 2.1]]
# yrange = [[-2, 3], [-2, 3]]
# text_ysite = [2.43, 2.03]

for igauge in range(2):
    for i in range(tmin, tmax + 1):
        # Fit
        rawdata = np.loadtxt(
            "{}/txt.{}".format(datapath[igauge], str(i).rjust(2, "0")), dtype=np.float64
        )

        mask = (rawdata[:, 0] > rmin / a) & (rawdata[:, 0] < rmax[igauge] / a)
        subdata = rawdata[mask]
        sorted_indices = np.argsort(subdata[:, 0])

        fitdata = subdata[sorted_indices]

        fitsites = fitdata[:, 0]
        fitfks = fitdata[:, 1]
        fiterr = fitdata[:, 2]

        # Fit
        least_squares = LeastSquares(fitsites, fitfks, fiterr, gaussian2)  # type: ignore
        m = Minuit(least_squares, **para)  # type: ignore
        m.migrad()

        # Draw
        fig, ax = plt.subplots()

        errbar_plot_style = {
            "fmt": ".",
            "markersize": 3.8,
            "markeredgewidth": 0.4,
            "linewidth": 0.3,
            "markerfacecolor": "white",
            # "fillstyle": "none",
        }

        legend_style = {
            "loc": 3,
            # "bbox_to_anchor": (0.95, 1.02),
            "handletextpad": 0.3,
            "labelspacing": 0.3,
        }

        ax.errorbar(
            rawdata[:, 0] * a,
            -rawdata[:, 1] * a_invrs,
            rawdata[:, 2] * a_invrs,
            label="data",
            **errbar_plot_style
        )
        x_fit = np.arange(0, 28, 0.01)
        ax.plot(
            x_fit * a,
            -gaussian2(x_fit, *m.values) * a_invrs,
            linewidth=0.75,
            label="fit",
        )
        # ax.plot(
        #     x_fit * a,
        #     np.full(x_fit.shape, m.values["C"]) * a_invrs,
        #     linewidth=0.75,
        #     label=r"$m_c$",
        # )

        # Set grid (reserved)
        # ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
        # ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

        ax.minorticks_on()
        ax.legend(**legend_style)

        ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
        # ax.set(xlim=(0.54, 0.66))
        ax.set(xlim=(0, 1.2))

        ax.set_ylabel(r"$F_{\rm KS}(r)$", labelpad=1.5)
        # ax.set(ylim=(yrange[igauge][0], yrange[igauge][1]))
        ax.set(ylim=(-3, 2))

        # ax.text(0.645, text_ysite[igauge], r"$t = {}$".format(str(i).rjust(2, "0")))
        ax.text(0.7, 1.5, r"$t = {}$".format(str(i).rjust(2, "0")))
        ax.text(
            0.7,
            # text_ysite[igauge] - 0.9,
            1.0,
            r"$m_c =$"
            + r"${}$".format(round(m.values["C"] * a_invrs * 1000))
            + r"$\ [{\rm MeV}]$",
        )

        fig.savefig("{}/{}.png".format(path[igauge], str(i).rjust(2, "0")), dpi=600)
        plt.close()
