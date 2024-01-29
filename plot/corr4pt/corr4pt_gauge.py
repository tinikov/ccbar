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


def gauge_plot(cdata, ct, ldata, lt, filename, xrange=None, yrange=None):
    fig, ax = plt.subplots()  # picture size

    errbar_plot_style1 = {
        "fmt": ".",
        "color": "xkcd:primary blue",
        "markersize": 3,
        "markeredgewidth": 0.4,
        "linewidth": 0.25,
        "markerfacecolor": "white",
        # "fillstyle": "none",
    }

    errbar_plot_style2 = {
        "fmt": ".",
        "color": "xkcd:bright red",
        "markersize": 3,
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

    ax.errorbar(
        cdata[ct][:, 0] * a,
        cdata[ct][:, 1] * int_c,
        cdata[ct][:, 2] * int_c,
        label=r"Coulomb ($n_t=$" + str(ct).rjust(2, "0") + ")",
        **errbar_plot_style1
    )

    ax.errorbar(
        ldata[lt][:, 0] * a,
        ldata[lt][:, 1] * int_c,
        ldata[lt][:, 2] * int_c,
        label=r"Landau ($n_t=$" + str(lt).rjust(2, "0") + ")",
        **errbar_plot_style2
    )

    ax.legend(**legend_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$")
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1])

    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_ylabel(r"$C(r)$")
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])

    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


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
l2_ps_c, l2_v_c, l2_ps_l, l2_v_l = [[] for _ in range(4)]
for it in range(32):
    l2_ps_c.append(
        np.loadtxt("{}/result/c4pt/corr/ps/txt.l2.{}".format(codeRoot, timelist[it]))
    )
    l2_ps_l.append(
        np.loadtxt("{}/result/l4pt/corr/ps/txt.l2.{}".format(codeRoot, timelist[it]))
    )
    l2_v_c.append(
        np.loadtxt("{}/result/c4pt/corr/v/txt.l2.{}".format(codeRoot, timelist[it]))
    )
    l2_v_l.append(
        np.loadtxt("{}/result/l4pt/corr/v/txt.l2.{}".format(codeRoot, timelist[it]))
    )

# PLOT
gauge_plot(
    l2_ps_c,
    29,
    l2_ps_l,
    29,
    filename="{}/4pt_gauge_ps".format(path),
    xrange=[0.05, 2.5],
    yrange=[-0.02, 0.4],
)

gauge_plot(
    l2_v_c,
    29,
    l2_v_l,
    29,
    filename="{}/4pt_gauge_v".format(path),
    xrange=[0.05, 2.5],
    yrange=[-0.02, 0.4],
)
