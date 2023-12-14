#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use("science")

a = 0.090713
tsize = 64
codeRoot = "/Users/chen/LQCD/code/ccbar"


def all_plot(data, filename, trange, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    errbar_plot_style = {
        "fmt": ".",
        "markersize": 3,
        "markeredgewidth": 0.2,
        "linewidth": 0.2,
        "fillstyle": "none",
    }

    legend_default_style = {
        "loc": 1,
        "handletextpad": 0,
        "frameon": False,
        "fontsize": 7,
        "labelspacing": 0.3,
    }

    for i in trange:
        ax.errorbar(
            data[i][:, 0] * a + 0.0004 * (i - trange[0]),
            data[i][:, 1],
            data[i][:, 2],
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **errbar_plot_style
        )

    ax.legend(**legend_default_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$")
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$C(r)$", labelpad=3)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = [
    "{}/fig/corr/c4pt".format(codeRoot),
    "{}/fig/corr/l4pt".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = [
    "{}/result/c4pt/corr".format(codeRoot),
    "{}/result/l4pt/corr".format(codeRoot),
]

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
xrange_all = [[[1.0, 1.1], [0.9, 1.0]], [[1.2, 1.3], [1.1, 1.2]]]
yrange_all = [[[0.001, 0.006], [0.006, 0.024]], [[0.002, 0.012], [0.017, 0.045]]]

for igauge in range(2):
    for ichan in range(2):
        for itype in range(3):
            all_plot(
                data=data[igauge][ichan],
                filename="{}/{}_conv".format(path[igauge], channel[ichan]),
                trange=np.arange(24, 30, 1),
                xrange=xrange_all[igauge][ichan],
                yrange=yrange_all[igauge][ichan],
            )
