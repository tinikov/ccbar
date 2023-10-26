#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

tsize = 64
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
    "markersize": 3.5,
    "markeredgewidth": 0.55,
    "linewidth": 0.3,
    # "capsize": 1,
    # "capthick": 0.2,
}


def all_plot(
    data,
    channel,
    filename,
    tsize,
    xrange=None,
    yrange=None,
):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size
    all_markers = ["*", "3", ".", "x", "4", "+", "1", "2"]

    index = np.arange(0, tsize, 1)
    for i in range(len(channel)):
        marker = all_markers[0 : len(channel)]
        ax.errorbar(
            index,
            data[i][:, 1],
            data[i][:, 2],
            label=channel[i].upper(),
            **style,
            fmt=marker[i]
        )

    # Set grid (reserved)
    # ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    # ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)

    ax.minorticks_on()
    ax.legend(loc=0, handletextpad=0.1, frameon=False)

    ax.set_xlabel(r"$n_t$", labelpad=-1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$C(n_t)$", labelpad=-1)
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=7))
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.15, right=0.98, bottom=0.13, top=0.97)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Channel
channel = ["ps", "v", "s", "av", "t"]

corr_c, corr_l = [[] for _ in range(2)]  # Read data files
for i in range(5):
    corr_c.append(np.loadtxt("{}/result/c2pt/corr/txt.{}".format(codeRoot, channel[i])))
    corr_l.append(np.loadtxt("{}/result/l2pt/corr/txt.{}".format(codeRoot, channel[i])))

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
