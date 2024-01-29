#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use(["science", "nature"])

a = 0.090713
a_invrs = 2.1753
tsize = 64
codeRoot = "/Volumes/X6/work/ccbar"


def all_plot(data, filename, trange, xrange=None, yrange=None):
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
        "loc": 2,
        "bbox_to_anchor": (0.95, 1.02),
        "handletextpad": 0,
        "labelspacing": 0.3,
    }

    for i in trange:
        re_i = i - trange[0]
        t_all = trange[-1] - trange[0]
        ax.errorbar(
            data[i][:, 0] * a + 0.00035 * (re_i - np.ceil(t_all / 2)),
            -data[i][:, 1] * a_invrs,
            data[i][:, 2] * a_invrs,
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **errbar_plot_style
        )

    ax.legend(**legend_style)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.02))
    ax.set_xlabel(r"$r\ [{\rm fm}]$")
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1])

    ax.set_ylabel(r"$F_{\rm KS}(r)$")
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])

    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = [
    "{}/fig/FKS/coulomb-TD/conv".format(codeRoot),
    "{}/fig/FKS/landau-TD/conv".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = [
    "{}/result/c4pt/FKS-TD".format(codeRoot),
    "{}/result/l4pt/FKS-TD".format(codeRoot),
]

# Time
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

# Read data
fks_c, fks_l = [[] for _ in range(2)]

fks_c.append(np.loadtxt("{}/txt.01".format(datapath[0])))
fks_l.append(np.loadtxt("{}/txt.01".format(datapath[1])))
for i in range(1, 31):
    fks_c.append(np.loadtxt("{}/txt.{}".format(datapath[0], timelist[i])))
    fks_l.append(np.loadtxt("{}/txt.{}".format(datapath[1], timelist[i])))

for irc in range(0, 10):
    all_plot(
        data=fks_c,
        filename="{}/{}".format(path[0], str(irc + 1).rjust(2, "0")),
        trange=np.arange(23, 29, 1),
        xrange=[0.4 + irc * 0.04, 0.4 + (irc + 1) * 0.04],
        yrange=[-2.4, -1.6],
    )

for irl in range(0, 20):
    all_plot(
        data=fks_l,
        filename="{}/{}".format(path[1], str(irl + 1).rjust(2, "0")),
        trange=np.arange(23, 29, 1),
        xrange=[0.4 + irl * 0.04, 0.4 + (irl + 1) * 0.04],
        yrange=[-1.7, -1.1],
    )