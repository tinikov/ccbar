#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

tsize = 64
cutoff = 2.1753
codeRoot = "/Users/chen/LQCD/code/ccbar"

# Font setting
font = {
    "family": "Charter",
    "size": 8,
    "mathfamily": "stix",
}

plt.rcParams["font.family"] = font["family"]
plt.rcParams["font.size"] = font["size"]
plt.rcParams["mathtext.fontset"] = font["mathfamily"]

style = {
    "markersize": 2.5,
    "markeredgewidth": 0.35,
    "linewidth": 0.35,
    # "capsize": 1,
    # "capthick": 0.2,
}


def all_plot(
    data,
    type,
    filename,
    tsize,
    cutoff=1.0,
    xrange=None,
    yrange=None,
):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size
    all_markers = ["*", "3", ".", "x", "4", "+", "1", "2"]

    index = np.arange(0, tsize, 1)
    for i in range(len(type)):
        marker = all_markers[0 : len(type)]
        ax.errorbar(
            index,
            data[i][:, 1] * cutoff,
            data[i][:, 2] * cutoff,
            label=type[i].upper(),
            **style,
            fmt=marker[i]
        )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.minorticks_on()
    ax.legend(loc=2, bbox_to_anchor=(0.95, 1.02), handletextpad=0.1, frameon=False)

    ax.set_xlabel(r"$n_t$", labelpad=-1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    # ax.xaxis.set_minor_locator(ticker.NullLocator())
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]", labelpad=1)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    # fig.subplots_adjust(left=0.155, right=0.85, bottom=0.13, top=0.96)
    fig.subplots_adjust(left=0.13, right=0.85, bottom=0.13, top=0.97)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Read data files
type = ["ps", "v", "s", "av", "t"]
hmass_c, hmass_l = [[] for _ in range(2)]

for i in range(5):
    hmass_c.append(
        np.loadtxt("{}/result/c2pt/effmass/txt.csh.{}".format(codeRoot, type[i]))
    )
    hmass_l.append(
        np.loadtxt("{}/result/l2pt/effmass/txt.csh.{}".format(codeRoot, type[i]))
    )

# Gauge
path = [
    "{}/fig/effmass/coulomb".format(codeRoot),
    "{}/fig/effmass/landau".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)
data = [hmass_c, hmass_l]  # C, L

# PLOT
for i in range(2):
    all_plot(
        data[i],
        type,
        "{}/closer".format(path[i]),
        tsize,
        cutoff=cutoff,
        xrange=[4, 28],
        yrange=[2.8, 3.6],
    )
