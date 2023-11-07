#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt

a = 0.090713
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
    "fmt": "x",
    "markersize": 1.3,
    "markeredgewidth": 0.3,
    "linewidth": 0.3,
}


def all_plot(data, filename, trange, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    for i in trange:
        ax.errorbar(
            data[i][:, 0] + 0.005 * i,
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
        "labelspacing": 0.1,
    }
    ax.legend(loc=4, **legend_default_style)

    ax.set_xlabel(r"$n_r$", labelpad=-1)
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$", labelpad=0.2)
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.17, right=0.97, bottom=0.13, top=0.96)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = [
    "{}/fig/preV/coulomb".format(codeRoot),
    "{}/fig/preV/landau".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = [
    "{}/result/c4pt/preV".format(codeRoot),
    "{}/result/l4pt/preV".format(codeRoot),
]

# Time
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

# Channel
channel = ["ps", "v"]

# Read data
pre_ps_c, pre_v_c, pre_ps_l, pre_v_l = [[] for _ in range(4)]

data = [[pre_ps_c, pre_v_c], [pre_ps_l, pre_v_l]]

for igauge in range(2):
    for ichan in range(2):
        for i in range(32):
            data[igauge][ichan].append(
                np.loadtxt(
                    "{}/{}/txt.{}".format(
                        datapath[igauge],
                        channel[ichan],
                        timelist[i],
                    )
                )
            )

yrange_gauge = [[0.03, 0.28], [-0.04, 0.21]]

for igauge in range(2):
    for ichan in range(2):
        all_plot(
            data=data[igauge][ichan],
            filename="{}/{}_conv".format(path[igauge], channel[ichan]),
            trange=np.arange(23, 29, 1),
            xrange=[8.1, 9.7],
            yrange=yrange_gauge[igauge],
        )
