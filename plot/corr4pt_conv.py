#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

a = 0.090713
tsize = 64

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
    "fmt": "x",
    "markersize": 1.6,
    "markeredgewidth": 0.2,
    "linewidth": 0.2,
}


def all_plot(data, filename, trange, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    for i in trange:
        ax.errorbar(
            data[i][:, 0] * a,
            data[i][:, 1],
            data[i][:, 2],
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **style
        )

    ax.minorticks_on()
    legend_default_style = {
        "handletextpad": 0,
        "frameon": False,
        "fontsize": 7,
        "labelspacing": 0.3,
    }
    ax.legend(loc=3, **legend_default_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$C(r)$", labelpad=-0.1)
    ax.set_yscale("log")
    # ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=7))
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.155, right=0.97, bottom=0.13, top=0.96)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = ["../fig/corr/c4pt", "../fig/corr/l4pt"]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = ["../result/c4pt/corr", "../result/l4pt/corr"]

# Time
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

# Channel
channel = ["ps", "v"]

# Read data
nn_ps_c, nn_v_c, nn_ps_l, nn_v_l = [[] for _ in range(4)]

data = [[nn_ps_c, nn_v_c], [nn_ps_l, nn_v_l]]

for igauge in range(2):
    for ichan in range(2):
        for i in range(32):
            data[igauge][ichan].append(
                np.loadtxt(
                    "{}/{}/txt.nn.{}".format(
                        datapath[igauge],
                        channel[ichan],
                        timelist[i],
                    )
                )
            )

# PLOT
yrange_all = [[[8e-4, 0.07], [1e-3, 0.12]], [[4e-3, 0.1], [1e-2, 0.2]]]
trange_all = [np.arange(22, 28, 1), np.arange(22, 28, 1)]
shift_all = [[True, True], [False, False]]

for igauge in range(2):
    for ichan in range(2):
        for itype in range(3):
            all_plot(
                data=data[igauge][ichan],
                filename="{}/{}_conv".format(path[igauge], channel[ichan]),
                trange=trange_all[igauge],
                xrange=[0.6, 1.2],
                yrange=yrange_all[igauge][ichan],
            )
