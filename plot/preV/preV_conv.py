#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use(["science", "nature"])

codeRoot = "/Volumes/X6/work/ccbar"


def all_plot(data, filename, trange, xrange=None, yrange=None):
    fig, ax = plt.subplots()

    errbar_plot_style = {
        "fmt": ".",
        "markersize": 4,
        "markeredgewidth": 0.4,
        "linewidth": 0.25,
        "markerfacecolor": "white",
        # "fillstyle": "none",
    }

    legend_style = {
        "loc": 4,
        "handletextpad": 0,
        "labelspacing": 0.3,
    }

    for i in trange:
        re_i = i - trange[0]
        t_all = trange[-1] - trange[0]
        ax.errorbar(
            data[i][:, 0] + 0.005 * (re_i - np.ceil(t_all / 2)),
            data[i][:, 1],
            data[i][:, 2],
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **errbar_plot_style
        )

    ax.legend(**legend_style)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_xlabel(r"$n_r$")
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1])

    ax.set_ylabel(r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$")
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])

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

yrange_gauge = [[[0.16, 0.26], [0.11, 0.21]], [[0.04 , 0.14], [0.00, 0.10]]]

for igauge in range(2):
    for ichan in range(2):
        all_plot(
            data=data[igauge][ichan],
            filename="{}/{}_conv".format(path[igauge], channel[ichan]),
            trange=np.arange(24, 30, 1),
            xrange=[9.76, 10.14],
            yrange=yrange_gauge[igauge][ichan],
        )
