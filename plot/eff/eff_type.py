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


def type_plot(exp, cosh, filename, cutoff=1.0, xrange=None, yrange=None):
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
        "loc": 8,
        "handletextpad": 0,
        "fontsize": 8,
        "labelspacing": 0.4,
    }

    index = np.arange(0, tsize, 1)
    ax.errorbar(
        index, exp[:, 1] * cutoff, exp[:, 2] * cutoff, label="exp", **errbar_plot_style1
    )
    ax.errorbar(
        index, cosh[:, 1] * cutoff, cosh[:, 2] * cutoff, label="cosh", **errbar_plot_style2
    )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.legend(**legend_default_style)

    ax.set_xlabel(r"$n_t$")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]")
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

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
