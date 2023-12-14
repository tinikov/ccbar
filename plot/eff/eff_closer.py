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

    errbar_plot_style = {
        "markersize": 3.5,
        "markeredgewidth": 0.4,
        "linewidth": 0.3,
        "fillstyle": "none",
    }

    legend_default_style = {
        "handletextpad": 0,
        "fontsize": 7,
        "labelspacing": 0.4,
    }

    all_markers = ["o", "h", "v", "H", "p", "s", "^", "<", ">"]

    index = np.arange(0, tsize, 1)
    for i in range(len(type)):
        ax.errorbar(
            index + 0.5 + 0.06 * (i - 3),
            data[i][:, 1] * cutoff,
            data[i][:, 2] * cutoff,
            label=type[i].upper(),
            **errbar_plot_style,
            fmt=all_markers[i]
        )

    # Set grid (reserved)
    ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

    ax.legend(loc=2, bbox_to_anchor=(0.95, 1.03), **legend_default_style)

    ax.set_xlabel(r"$n_t$")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]", labelpad=3)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

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
        xrange=[4, 29],
        yrange=[2.8, 3.6],
    )
