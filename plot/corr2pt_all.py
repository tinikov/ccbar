#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use(["science", "nature"])

tsize = 64
codeRoot = "/Volumes/X6/work/ccbar"


def all_plot(
    data,
    channel,
    filename,
    tsize,
    xrange=None,
    yrange=None,
):
    fig, ax = plt.subplots()

    errbar_plot_style = {
        "markersize": 3.5,
        "markeredgewidth": 0.4,
        "linewidth": 0.25,
        "fillstyle": "none",
    }

    legend_style = {
        "loc": "best",
        "handletextpad": 0.5,
        "labelspacing": 0.3,
    }

    all_markers = ["o", "h", "v", "H", "p", "s", "^", "<", ">"]

    index = np.arange(0, tsize, 2)
    for i in range(len(channel)):
        ax.errorbar(
            index,
            data[i][:, 1][0::2],
            data[i][:, 2][0::2],
            label=channel[i].upper(),
            **errbar_plot_style,
            fmt=all_markers[i]
        )

    ax.legend(**legend_style)

    ax.set_xlabel(r"$n_t$")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1])

    ax.set_ylabel(r"$C(n_t)$")
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=7))
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])

    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Channel
channel = ["ps", "v", "s", "av", "t"]

corr_c, corr_l = [[] for _ in range(2)]  # Read data files
for i in range(5):
    corr_c.append(np.loadtxt("{}/result/c2pt/corr/2pt.{}.txt".format(codeRoot, channel[i])))
    corr_l.append(np.loadtxt("{}/result/l2pt/corr/2pt.{}.txt".format(codeRoot, channel[i])))

# Gauge
path = [
    "{}/fig/corr/c2pt".format(codeRoot),
    "{}/fig/corr/l2pt".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)
data = [corr_c, corr_l]  # C, L

# PLOT
for i in range(2):
    all_plot(
        data[i],
        channel,
        "{}/all".format(path[i]),
        tsize,
        yrange=[1e-27, 1e-1],
    )
