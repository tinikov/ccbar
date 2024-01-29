#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use(["science", "nature"])

a = 0.090713
tsize = 64
codeRoot = "/Volumes/X6/work/ccbar"
int_c = 2.0 * np.sqrt(np.pi)


def all_plot(data, filename, trange, xrange=None, yrange=None, tick_locator=None):
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
        "loc": 1,
        "handletextpad": 0,
        "labelspacing": 0.3,
    }

    for i in trange:
        re_i = i - trange[0]
        t_all = trange[-1] - trange[0]
        ax.errorbar(
            data[i][:, 0] * a + 0.00025 * (re_i - np.ceil(t_all / 2)),
            data[i][:, 1] * int_c,
            data[i][:, 2] * int_c,
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **errbar_plot_style
        )

    ax.legend(**legend_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$")
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1])

    ax.set_ylabel(r"$C(r)$")
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])
    if tick_locator is not None:
        ax.yaxis.set_major_locator(tick_locator)

    ax.ticklabel_format(style="sci", scilimits=(-1, 2), axis="y")

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
l2_ps_c, l2_v_c, l2_ps_l, l2_v_l = [[] for _ in range(4)]

data = [[l2_ps_c, l2_v_c], [l2_ps_l, l2_v_l]]

for igauge in range(2):
    for ichan in range(2):
        for i in range(32):
            data[igauge][ichan].append(
                np.loadtxt(
                    "{}/{}/txt.l2.{}".format(
                        datapath[igauge],
                        channel[ichan],
                        timelist[i],
                    )
                )
            )

# PLOT
xrange_all = [[[1.024, 1.052], [1.024, 1.052]], [[1.024, 1.052], [1.024, 1.052]]]
yrange_all = [
    [[0.00125, 0.0024], [0.0019, 0.004]],
    [[0.004, 0.007], [0.0066, 0.013]],
]
tick_locator = [None, ticker.MultipleLocator(0.0004), None, None]

for igauge in range(2):
    for ichan in range(2):
        all_plot(
            data=data[igauge][ichan],
            filename="{}/{}_conv".format(path[igauge], channel[ichan]),
            trange=np.arange(24, 30, 1),
            xrange=xrange_all[igauge][ichan],
            yrange=yrange_all[igauge][ichan],
            tick_locator=tick_locator[igauge + ichan],
        )
