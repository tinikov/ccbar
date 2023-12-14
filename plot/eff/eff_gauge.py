#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use("science")

tsize = 64
cutoff = 2.1753
codeRoot = "/Users/chen/LQCD/code/ccbar"


def gauge_plot(coulomb, landau, filename, cutoff=1.0, xrange=None, yrange=None, loc=8):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    errbar_plot_style1 = {
        "fmt": "D",
        "color": "xkcd:primary blue",
        "markersize": 2.8,
        "markeredgewidth": 0.35,
        "linewidth": 0.25,
        "fillstyle": "none",
    }

    errbar_plot_style2 = {
        "fmt": "s",
        "color": "xkcd:bright red",
        "markersize": 2.8,
        "markeredgewidth": 0.35,
        "linewidth": 0.25,
        "fillstyle": "none",
    }

    legend_default_style = {
        "handletextpad": 0,
        "fontsize": 7,
        "labelspacing": 0.4,
    }

    index = np.arange(0, tsize, 1)
    ax.errorbar(
        index + 0.5,
        coulomb[:, 1] * cutoff,
        coulomb[:, 2] * cutoff,
        label="Coulomb",
        **errbar_plot_style1,
    )
    ax.errorbar(
        index + 0.5,
        landau[:, 1] * cutoff,
        landau[:, 2] * cutoff,
        label="Landau",
        **errbar_plot_style2,
    )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.legend(loc=loc, **legend_default_style)

    ax.set_xlabel(r"$n_t$")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]", labelpad=3)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

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

xrange_all = [[4, 29], [4, 29], [0, 29], [0, 29], [0, 29]]
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
