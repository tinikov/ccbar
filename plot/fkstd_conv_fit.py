#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

a = 0.090713
a_invrs = 2.1753
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
            data[i][:, 0] * a,
            data[i][:, 1] * a_invrs,
            data[i][:, 2] * a_invrs,
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
    ax.legend(loc=3, bbox_to_anchor=(0.08, 0), **legend_default_style)

    ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$F_{\rm KS}(r)$", labelpad=-0.1)
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.96)
    fig.savefig("{}.png".format(filename), dpi=600)
    plt.close()


# Gauge
path = ["../fig/FKS/coulomb-TD", "../fig/FKS/landau-TD"]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)

datapath = ["../result/c4pt/FKS-TD", "../result/l4pt/FKS-TD"]

# Time
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

# Read data
fks_c, fks_l = [[] for _ in range(2)]

fks_c.append(np.loadtxt("../result/c4pt/FKS-TD/txt.01"))
fks_l.append(np.loadtxt("../result/l4pt/FKS-TD/txt.01"))
for i in range(1, 32):
    fks_c.append(np.loadtxt("../result/c4pt/FKS-TD/txt.{}".format(timelist[i])))
    fks_l.append(np.loadtxt("../result/l4pt/FKS-TD/txt.{}".format(timelist[i])))

all_plot(
    data=fks_c,
    filename="{}/conv".format(path[0]),
    trange=np.arange(21, 28, 1),
    xrange=[0.6, 0.8],
    yrange=[1.5, 2.0],
)

# all_plot(
#     data=fks_l,
#     filename="{}/all".format(path[1]),
#     trange=np.arange(3, 28, 3),
#     xrange=[0, 1.2],
#     yrange=[-12, 4],
# )
