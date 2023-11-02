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


def gauge_plot(coulomb, landau, filename, cutoff=1.0, xrange=None, yrange=None, loc=8):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    index = np.arange(0, tsize, 1)
    ax.errorbar(
        index,
        coulomb[:, 1] * cutoff,
        coulomb[:, 2] * cutoff,
        label="Coulomb",
        **style,
        fmt="x"
    )
    ax.errorbar(
        index + 0.12,
        landau[:, 1] * cutoff,
        landau[:, 2] * cutoff,
        label="Landau",
        **style,
        fmt="+"
    )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.minorticks_on()
    ax.legend(loc=loc, handletextpad=0.1, frameon=False)

    ax.set_xlabel(r"$n_t$", labelpad=-1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    # ax.xaxis.set_minor_locator(ticker.NullLocator())
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]", labelpad=1)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.14, right=0.98, bottom=0.13, top=0.97)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Channel
channel = ["ps", "v", "s", "av", "t"]

emass_c, emass_l = [[] for _ in range(2)]  # Read data files
for i in range(5):
    emass_c.append(
        np.loadtxt("{}/result/c2pt/effmass/txt.exp.{}".format(codeRoot, channel[i]))
    )
    emass_l.append(
        np.loadtxt("{}/result/l2pt/effmass/txt.exp.{}".format(codeRoot, channel[i]))
    )

xrange_all = [[4, 28], [4, 28], [0, 28], [0, 28], [0, 28]]
yrange_all = [[2.7, 3], [2.8, 3.1], [3.2, 3.6], [3.3, 3.6], [3.3, 3.6]]
loc = [8, 8, 2, 2, 2]

# Destination
path = "{}/fig/effmass".format(codeRoot)
if not os.path.exists(path):
    os.makedirs(path)

# PLOT
for i in range(5):
    gauge_plot(
        emass_c[i],
        emass_l[i],
        "{}/gauge_{}".format(path, channel[i]),
        cutoff=cutoff,
        xrange=xrange_all[i],
        yrange=yrange_all[i],
        loc=loc[i],
    )
