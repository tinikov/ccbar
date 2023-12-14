#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use("science")

a = 0.090713
tsize = 64
codeRoot = "/Users/chen/LQCD/code/ccbar"


def gauge_plot(cdata, ct, ldata, lt, filename, xrange=None, yrange=None):
    fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

    errbar_plot_style1 = {
        "fmt": "o",
        "color": "xkcd:primary blue",
        "markersize": 2.5,
        "markeredgewidth": 0.35,
        "linewidth": 0.25,
        "fillstyle": "none",
    }

    errbar_plot_style2 = {
        "fmt": "s",
        "color": "xkcd:bright red",
        "markersize": 2.2,
        "markeredgewidth": 0.35,
        "linewidth": 0.25,
        "fillstyle": "none",
    }

    legend_default_style = {
        "loc": 1,
        "handletextpad": 0,
        "frameon": False,
        "fontsize": 7,
        "labelspacing": 0.3,
    }

    ax.errorbar(
        cdata[ct][:, 0] * a,
        cdata[ct][:, 1] * 2 * np.sqrt(np.pi),
        cdata[ct][:, 2] * 2 * np.sqrt(np.pi),
        label=r"Coulomb ($n_t=$" + str(ct).rjust(2, "0") + ")",
        **errbar_plot_style1
    )

    ax.errorbar(
        ldata[lt][:, 0] * a,
        ldata[lt][:, 1] * 2 * np.sqrt(np.pi),
        ldata[lt][:, 2] * 2 * np.sqrt(np.pi),
        label=r"Landau ($n_t=$" + str(lt).rjust(2, "0") + ")",
        **errbar_plot_style2
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
    xrange=[0, 2.5],
    yrange=[-0.05, 0.6],
)

gauge_plot(
    l2_v_c,
    29,
    l2_v_l,
    29,
    filename="{}/4pt_gauge_v".format(path),
    xrange=[0, 2.5],
    yrange=[-0.04, 0.4],
)
