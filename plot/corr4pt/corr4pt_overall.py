#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

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
    "markersize": 1.7,
    "markeredgewidth": 0.3,
    "linewidth": 0.3,
}


def all_plot(data, filename, trange, ntype, xrange=None, yrange=None):
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
        "labelspacing": 0.1,
    }

    ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$C(r)$", labelpad=-0.1)
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=7))
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    if ntype == "plain":
        fig.subplots_adjust(left=0.155, right=0.85, bottom=0.13, top=0.96)
        ax.legend(loc=2, bbox_to_anchor=(0.95, 1.02), **legend_default_style)
    elif ntype == "nn":
        fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.96)
        ax.legend(loc=3, bbox_to_anchor=(-0.03, -0.02), **legend_default_style)
    elif ntype == "l2":
        fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.96)
        if filename == "{}/fig/corr/l4pt/l2_ps".format(
            codeRoot
        ) or filename == "{}/fig/corr/l4pt/l2_v".format(codeRoot):
            ax.legend(loc=1, bbox_to_anchor=(1.01, 1.02), **legend_default_style)
        else:
            ax.legend(loc=3, bbox_to_anchor=(-0.03, -0.02), **legend_default_style)

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

# Type
type_all = ["plain", "nn", "l2"]

# Read data
plain_ps_c, nn_ps_c, l2_ps_c, plain_v_c, nn_v_c, l2_v_c = [[] for _ in range(6)]
plain_ps_l, nn_ps_l, l2_ps_l, plain_v_l, nn_v_l, l2_v_l = [[] for _ in range(6)]

data = [
    [[plain_ps_c, nn_ps_c, l2_ps_c], [plain_v_c, nn_v_c, l2_v_c]],
    [[plain_ps_l, nn_ps_l, l2_ps_l], [plain_v_l, nn_v_l, l2_v_l]],
]

for igauge in range(2):
    for ichan in range(2):
        for itype in range(3):
            for i in range(32):
                data[igauge][ichan][itype].append(
                    np.loadtxt(
                        "{}/{}/txt.{}.{}".format(
                            datapath[igauge],
                            channel[ichan],
                            type_all[itype],
                            timelist[i],
                        )
                    )
                )

# PLOT
yrange_all = [
    [
        [[1e-27, 1e-6], [8e-4, 1], [1e-4, 0.2]],
        [[1e-27, 1e-6], [1e-3, 1], [1e-4, 0.2]],
    ],
    [
        [[1e-27, 1e-6], [5e-3, 1], [3e-4, 0.2]],
        [[1e-27, 1e-6], [1e-2, 1], [1e-3, 0.1]],
    ],
]

for igauge in range(2):
    for ichan in range(2):
        for itype in range(3):
            all_plot(
                data=data[igauge][ichan][itype],
                filename="{}/{}_{}".format(
                    path[igauge], type_all[itype], channel[ichan]
                ),
                trange=np.arange(1, 29, 3),
                ntype="{}".format(type_all[itype]),
                xrange=[0, 1.2],
                yrange=yrange_all[igauge][ichan][itype],
            )
