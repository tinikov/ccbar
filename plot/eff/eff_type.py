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
    "markersize": 4.5,
    "markeredgewidth": 0.7,
    "linewidth": 0.4,
    # "capsize": 1,
    # "capthick": 0.2,
}


def type_plot(exp, cosh, filename, cutoff=1.0, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    index = np.arange(0, tsize, 1)
    ax.errorbar(
        index, exp[:, 1] * cutoff, exp[:, 2] * cutoff, label="exp", **style, fmt="x"
    )
    ax.errorbar(
        index, cosh[:, 1] * cutoff, cosh[:, 2] * cutoff, label="cosh", **style, fmt="+"
    )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.minorticks_on()
    ax.legend(loc=8, handletextpad=0.1, frameon=False)

    ax.set_xlabel(r"$n_t$", labelpad=-1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    # ax.xaxis.set_minor_locator(ticker.NullLocator())
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]", labelpad=1)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.13, top=0.97)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Channel
channel = ["ps", "v", "s", "av", "t"]

emass_c, emass_l, hmass_c, hmass_l = [[] for _ in range(4)]  # Read data files
for i in range(5):
    emass_c.append(
        np.loadtxt("{}/result/c2pt/effmass/txt.exp.{}".format(codeRoot, channel[i]))
    )
    emass_l.append(
        np.loadtxt("{}/result/l2pt/effmass/txt.exp.{}".format(codeRoot, channel[i]))
    )
    hmass_c.append(
        np.loadtxt("{}/result/c2pt/effmass/txt.csh.{}".format(codeRoot, channel[i]))
    )
    hmass_l.append(
        np.loadtxt("{}/result/l2pt/effmass/txt.csh.{}".format(codeRoot, channel[i]))
    )

yrange_all = [[1.5, 3.1], [1.6, 3.2], [2.2, 3.6], [2.4, 3.8], [2.4, 3.8]]

# Gauge
path = [
    "{}/fig/effmass/coulomb".format(codeRoot),
    "{}/fig/effmass/landau".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)
edata = [emass_c, emass_l]  # C, L
hdata = [hmass_c, hmass_l]  # C, L

# PLOT
for i in range(2):
    for j in range(5):
        type_plot(
            edata[i][j],
            hdata[i][j],
            "{}/type_{}".format(path[i], channel[j]),
            cutoff=cutoff,
            xrange=[0, 32],
            yrange=yrange_all[j],
        )
