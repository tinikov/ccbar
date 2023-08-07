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
    "markersize": 1.7,
    "markeredgewidth": 0.3,
    "linewidth": 0.3,
}


def all_plot(data, filename, trange, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    for i in trange:
        ax.errorbar(
            data[i][:, 0],
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
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$", labelpad=-0.1)
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.17, right=0.97, bottom=0.13, top=0.96)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = ["../fig/preV/coulomb", "../fig/preV/landau"]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = ["../result/c4pt/preV", "../result/l4pt/preV"]

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

for igauge in range(2):
    for ichan in range(2):
        all_plot(
            data=data[igauge][ichan],
            filename="{}/{}_all".format(path[igauge], channel[ichan]),
            trange=np.arange(0, 28, 3),
            xrange=[0, 13],
            yrange=[-1, 0.4],
        )
