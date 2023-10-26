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
    "markersize": 3.5,
    "markeredgewidth": 0.4,
    "linewidth": 0.4,
}


def gauge_plot(cdata, ct, ldata, lt, filename, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    ax.errorbar(
        cdata[ct][:, 0] * a,
        cdata[ct][:, 1],
        cdata[ct][:, 2],
        label=r"Coulomb ($n_t=$" + str(ct).rjust(2, "0") + ")",
        fmt="+",
        **style
    )

    ax.errorbar(
        ldata[lt][:, 0] * a,
        ldata[lt][:, 1],
        ldata[lt][:, 2],
        label=r"Landau ($n_t=$" + str(lt).rjust(2, "0") + ")",
        fmt="3",
        **style
    )

    ax.minorticks_on()
    legend_default_style = {
        "handletextpad": 0,
        "frameon": False,
        "fontsize": 7,
        "labelspacing": 0.1,
    }
    ax.legend(loc=3, **legend_default_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
    if xrange is not None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$C(r)$", labelpad=-0.1)
    ax.set_yscale("log")
    if yrange is not None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.96)

    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = "{}/fig/corr/".format(codeRoot)
if not os.path.exists(path):
    os.makedirs(path)

# Time
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

# Channel
channel = ["ps", "v"]

# Read data
nn_ps_c, nn_v_c, nn_ps_l, nn_v_l = [[] for _ in range(4)]
for it in range(32):
    nn_ps_c.append(
        np.loadtxt("{}/result/c4pt/corr/ps/txt.nn.{}".format(codeRoot, timelist[it]))
    )
    nn_ps_l.append(
        np.loadtxt("{}/result/l4pt/corr/ps/txt.nn.{}".format(codeRoot, timelist[it]))
    )
    nn_v_c.append(
        np.loadtxt("{}/result/c4pt/corr/v/txt.nn.{}".format(codeRoot, timelist[it]))
    )
    nn_v_l.append(
        np.loadtxt("{}/result/l4pt/corr/v/txt.nn.{}".format(codeRoot, timelist[it]))
    )

# PLOT
gauge_plot(
    nn_ps_c,
    28,
    nn_ps_l,
    28,
    filename="{}/4pt_gauge_ps".format(path),
    xrange=[0, 1.2],
    yrange=[5e-4, 1],
)

gauge_plot(
    nn_v_c,
    28,
    nn_v_l,
    28,
    filename="{}/4pt_gauge_v".format(path),
    xrange=[0, 1.2],
    yrange=[5e-4, 1],
)
