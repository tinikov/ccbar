#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

plt.rcParams["font.family"] = "Charter"
plt.rcParams["mathtext.fontset"] = "stix"

a = 0.090713


def all_plot(
    data,
    title,
    filename,
    trange,
    log_on=False,
    xrange=None,
    yrange=None,
    loca=0,
    ylable="need a label!",
):
    fig, ax = plt.subplots()

    style = {
        "markersize": 0.5,
        "fmt": "o",
        "linewidth": 0.3,
        "capsize": 0.2,
        "capthick": 0.3,
    }

    legend_style = {
        "loc": loca,
        "handletextpad": 0.05,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }
    for i in trange:
        ax.errorbar(
            data[i][:, 0] * a,
            data[i][:, 1],
            data[i][:, 2],
            label=r"$n_t=$" + str(i).rjust(2, "0"),
            **style
        )

    ax.set_xlabel(r"$r\ [{\rm fm}]$")
    ax.minorticks_on()
    ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)
    ax.legend(**legend_style)
    ax.set_title(title)
    ax.set_ylabel(ylable)
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))
    if log_on:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))

    fig.tight_layout()
    fig.savefig("{}.pdf".format(filename))
    plt.close()


def vs_plot(
    dataC,
    dataL,
    title,
    filename,
    rLUnit=False,
    log_on=False,
    xrange=None,
    yrange=None,
    cutoff=1.0,
    loca=0,
    ylable="need a label!",
):
    fig, ax = plt.subplots()

    style = {
        # 'markersize': 0.5,
        # 'linewidth': 0.3,
        # 'capthick': 0.3,
        "markersize": 1.6,
        "linewidth": 0.5,
        "capthick": 0.5,
        "fmt": "o",
        "capsize": 0.2,
    }

    legend_style = {
        "loc": loca,
        "handletextpad": 0.05,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }

    mcC = 1.878949898325150025
    mcL = 1.463468832360292460

    if rLUnit:
        ax.errorbar(
            dataC[:, 0], dataC[:, 1] / mcC, dataC[:, 2] / mcC, label=r"Coulomb", **style
        )
        ax.errorbar(
            dataL[:, 0], dataL[:, 1] / mcL, dataL[:, 2] / mcL, label=r"Landau", **style
        )
        # ax.errorbar(dataC[:, 0], -dataC[:, 1], dataC[:, 2], label='Coulomb', **style)
        # ax.errorbar(dataL[:, 0], -dataL[:, 1], dataL[:, 2], label='Landau', **style)
        ax.set_xlabel(r"$n_r$")
    else:
        ax.errorbar(
            dataC[:, 0] * a,
            dataC[:, 1] * cutoff,
            dataC[:, 2] * cutoff,
            label=r"Coulomb ($n_t=19$)",
            **style
        )
        ax.errorbar(
            dataL[:, 0] * a,
            dataL[:, 1] * cutoff,
            dataL[:, 2] * cutoff,
            label=r"Landau ($n_t=28$)",
            **style
        )
        ax.set_xlabel(r"$r\ [{\rm fm}]$")

    ax.minorticks_on()
    ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)
    ax.legend(**style)
    ax.set_title(title)
    ax.set_ylabel(ylable)

    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))
    if log_on:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))

    fig.tight_layout()
    fig.savefig(
        "/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename)
    )


# make data:
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, "0"))

psrawC, psnrC, psl2C, vrawC, vnrC, vl2C = [[] for _ in range(6)]
psrawL, psnrL, psl2L, vrawL, vnrL, vl2L = [[] for _ in range(6)]

for i in range(32):
    psrawC.append(
        np.loadtxt("../result/c4pt/corr/ps/raw/txt.{number}".format(number=timelist[i]))
    )
    vrawC.append(
        np.loadtxt("../result/c4pt/corr/v/raw/txt.{number}".format(number=timelist[i]))
    )

    # psnrC.append(np.loadtxt("4ptC.result/c0.v.{number}".format(number=timelist[i])))
    # vnrC.append(np.loadtxt("4ptC.result/v0.{number}".format(number=timelist[i])))

    # psl2C.append(np.loadtxt("4ptC.result/lap.ps.{number}".format(number=timelist[i])))
    # vl2C.append(np.loadtxt("4ptC.result/vs.{number}".format(number=timelist[i])))

    psrawL.append(
        np.loadtxt("../result/l4pt/corr/ps/raw/txt.{number}".format(number=timelist[i]))
    )
    vrawL.append(
        np.loadtxt("../result/l4pt/corr/ps/raw/txt.{number}".format(number=timelist[i]))
    )

    # psnrL.append(np.loadtxt("4ptL.result/c0.v.{number}".format(number=timelist[i])))
    # vnrL.append(np.loadtxt("4ptL.result/v0.{number}".format(number=timelist[i])))

    # psl2L.append(np.loadtxt("4ptL.result/lap.ps.{number}".format(number=timelist[i])))
    # vl2L.append(np.loadtxt("4ptL.result/vs.{number}".format(number=timelist[i])))


cpath = "../fig/corr/c4pt"
lpath = "../fig/corr/l4pt"

if not os.path.exists("../fig"):
    os.mkdir("../fig")
if not os.path.exists("../fig/corr"):
    os.mkdir("../fig/corr")
if not os.path.exists(cpath):
    os.mkdir(cpath)
if not os.path.exists(lpath):
    os.mkdir(lpath)

# RAW
all_plot(
    data=psrawC,
    title=r"$C(r)$ (Coulomb) (PS channel)",
    filename="{}/ps-raw".format(cpath),
    trange=np.arange(1, 29, 3),
    xrange=[0, 1.4],
    log_on=True,
    ylable=r"$C(r)$",
    loca=3,
)

all_plot(
    data=psrawL,
    title=r"$C(r)$ (Landau) (PS channel)",
    filename="{}/ps-raw".format(lpath),
    trange=np.arange(1, 29, 3),
    xrange=[0, 1.4],
    log_on=True,
    ylable=r"$C(r)$",
    loca=3,
)

all_plot(
    data=vrawC,
    title=r"$C(r)$ (Coulomb) (V channel)",
    filename="{}/v-raw".format(cpath),
    trange=np.arange(1, 29, 3),
    xrange=[0, 1.4],
    log_on=True,
    ylable=r"$C(r)$",
    loca=3,
)

all_plot(
    data=vrawC,
    title=r"$C(r)$ (Landau) (V channel)",
    filename="{}/v-raw".format(lpath),
    trange=np.arange(1, 29, 3),
    xrange=[0, 1.4],
    log_on=True,
    ylable=r"$C(r)$",
    loca=3,
)

####### Coulomb 4pt V ########
# all_plot(
#     vC,
#     r"Saturation of $\phi(r)/\phi(0)$ (Coulomb) (V channel)",
#     "corr_V_4ptC_conv",
#     trange=np.arange(22, 29, 1),
#     xrange=[0, 1.4],
#     yrange=[1e-4, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
# )

######## Landau 4pt V ########
# all_plot(
#     psL,
#     r"$\phi(r)/\phi(0)$ (Landau) (PS channel)",
#     "corr_PS_4ptL",
#     trange=np.arange(1, 29, 3),
#     xrange=[0, 1.4],
#     yrange=[1e-3, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
#     loca=3,
# )
# all_plot(
#     psL,
#     r"Saturation of $\phi(r)/\phi(0)$ (Landau) (PS channel)",
#     "corr_PS_4ptL_conv",
#     trange=np.arange(22, 29, 1),
#     xrange=[0, 1.4],
#     yrange=[1e-3, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
# )

# ######## Landau 4pt V ########
# all_plot(
#     vL,
#     r"$\phi(r)/\phi(0)$ (Landau) (V channel)",
#     "corr_V_4ptL",
#     trange=np.arange(1, 29, 3),
#     xrange=[0, 1.4],
#     yrange=[1e-3, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
#     loca=3,
# )
# all_plot(
#     vL,
#     r"Saturation of $\phi(r)/\phi(0)$ (Landau) (V channel)",
#     "corr_V_4ptL_conv",
#     trange=np.arange(22, 29, 1),
#     xrange=[0, 1.4],
#     yrange=[1e-3, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
# )

# ############### Comparison between gauges #################
# ####### 4pt corr ########
# vs_plot(
#     psC[19],
#     psL[28],
#     r"$\phi(r)/\phi(0)$ (PS channel) (Coulomb vs Landau)",
#     "corr4pt_PS_gaugevs_19C28L",
#     xrange=[0, 1.4],
#     yrange=[1e-4, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
#     loca=3,
# )
# vs_plot(
#     l2psC[19],
#     l2psL[28],
#     r"$\phi(r)$ (normalized) (PS channel) (Coulomb vs Landau)",
#     "l24pt_PS_gaugevs_19C28L",
#     xrange=[0, 1.4],
#     yrange=[1e-7, 1e-2],
#     log_on=True,
#     ylable=r"$\phi(r)$ (normalized)",
#     loca=3,
# )
# vs_plot(
#     l2psC[19],
#     l2psL[28],
#     r"$\phi(r)$ (normalized) (PS channel) (Coulomb vs Landau)",
#     "l24pt_PS_gaugevs_gauss_19C28L",
#     xrange=[0, 1.4],
#     ylable=r"$\phi(r)$ (normalized)",
#     loca=3,
# )
# vs_plot(
#     vC[28],
#     vL[28],
#     r"$\phi(r)/\phi(0)$ (V channel) (Coulomb vs Landau) ($n_t=28$)",
#     "corr4pt_V_typevs_nt28",
#     xrange=[0, 1.4],
#     yrange=[1e-4, 1.0],
#     log_on=True,
#     ylable=r"$\phi(r)/\phi(0)$",
#     loca=3,
# )
