#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

a = 0.090713
a_invrs = 2.1753

tmin = 10
tmax = 27

rmin = 0.01
rmax = [1.34, 1.34]

path = ["../fig/FKS/coulomb-TD/each", "../fig/FKS/landau-TD/each"]
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = ["../result/c4pt/FKS-TD", "../result/l4pt/FKS-TD"]


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

# Font setting
font = {
    "family": "Charter",
    "size": 8,
    "mathfamily": "stix",
}

plt.rcParams["font.family"] = font["family"]
plt.rcParams["font.size"] = font["size"]
plt.rcParams["mathtext.fontset"] = font["mathfamily"]

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

        result = gaussian2_model.fit(fitfks, params2, x=fitsites, weights=1 / fiterr)

        # Draw
        style = {
            "fmt": ".",
            "markersize": 1,
            "markeredgewidth": 0.35,
            "linewidth": 0.3,
        }

        fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

        ax.errorbar(
            rawdata[:, 0] * a,
            rawdata[:, 1] * a_invrs,
            rawdata[:, 2] * a_invrs,
            label="data",
            **style
        )
        x_fit = np.arange(0, 28, 0.01)
        ax.plot(
            x_fit * a,
            gaussian2(x_fit, **result.best_values) * a_invrs,
            linewidth=0.75,
            label="fit",
        )
        ax.plot(
            x_fit * a,
            np.full(x_fit.shape, result.best_values["C"]) * a_invrs,
            linewidth=0.75,
            label=r"$m_c$",
        )

        # Set grid (reserved)
        ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
        ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)

        ax.minorticks_on()
        legend_default_style = {
            "frameon": False,
            "fontsize": 7,
            "labelspacing": 0.1,
        }
        ax.legend(loc=4, bbox_to_anchor=(0.88, 0.04), **legend_default_style)

        ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
        ax.set(xlim=(0, 1.2))

        ax.set_ylabel(r"$F_{\rm KS}(r)$", labelpad=-0.1)
        ax.set(ylim=(-2, 4))

        fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.96)
        fig.savefig("{}/{}.png".format(path[igauge], str(i).rjust(2, "0")), dpi=600)
        plt.close()