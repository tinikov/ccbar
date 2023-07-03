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
    if rLUnit:
        for i in trange:
            ax.errorbar(
                data[i][:, 0],
                data[i][:, 1],
                data[i][:, 2],
                label=r"$n_t=$" + str(i).rjust(2, "0"),
                **style
            )
        ax.set_xlabel(r"$n_r$")
    else:
        for i in trange:
            ax.errorbar(
                data[i][:, 0] * a,
                data[i][:, 1] * cutoff,
                data[i][:, 2] * cutoff,
                label=r"$n_t=$" + str(i).rjust(2, "0"),
                **style
            )
        ax.set_xlabel(r"$r\ [{\rm fm}]$")

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

prepsC, prevC, v0tiC, vstiC, v0tdC, vstiC = [[] for _ in range(6)]
prepsL, prevL, v0tiL, vstiL, v0tdL, vstiL = [[] for _ in range(6)]

for i in range(32):
    prepsC.append(
        np.loadtxt("../result/c4pt/prepot/ps/txt.{number}".format(number=timelist[i]))
    )
    prevC.append(
        np.loadtxt("../result/c4pt/prepot/v/txt.{number}".format(number=timelist[i]))
    )

    prepsL.append(
        np.loadtxt("../result/l4pt/prepot/ps/txt.{number}".format(number=timelist[i]))
    )
    prevL.append(
        np.loadtxt("../result/l4pt/prepot/ps/txt.{number}".format(number=timelist[i]))
    )


cpath = "../fig/pot/coulomb"
lpath = "../fig/pot/landau"

if not os.path.exists("../fig"):
    os.mkdir("../fig")
if not os.path.exists("../fig/pot"):
    os.mkdir("../fig/pot")
if not os.path.exists(cpath):
    os.mkdir(cpath)
if not os.path.exists(lpath):
    os.mkdir(lpath)

# Pre-potential
# all_plot(pspreC, r'$V_{\rm eff}$ (PS) (Coulomb)', "lap_PS_C", rLUnit=True, xrange=[0, 15.5], yrange=[-1.5, 0.5], trange=np.arange(1, 29, 3), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)

all_plot(
    data=prepsC,
    title=r"$V_{\rm eff}$ (Coulomb) (PS channel)",
    filename="{}/pre-ps".format(cpath),
    trange=np.arange(1, 29, 3),
    rLUnit=True,
    xrange=[0, 15.5],
    yrange=[-1.5, 0.5],
    ylable=r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$",
    loca=4,
)

all_plot(
    data=prepsL,
    title=r"$V_{\rm eff}$ (Landau) (PS channel)",
    filename="{}/pre-ps".format(lpath),
    trange=np.arange(1, 29, 3),
    rLUnit=True,
    xrange=[0, 15.5],
    yrange=[-1.5, 0.5],
    ylable=r"$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$",
    loca=4,
)

# all_plot(
#     data=vrawC,
#     title=r"$C(r)$ (Coulomb) (V channel)",
#     filename="{}/v-raw".format(cpath),
#     trange=np.arange(1, 29, 3),
#     xrange=[0, 1.4],
#     log_on=True,
#     ylable=r"$C(r)$",
#     loca=3,
# )

# all_plot(
#     data=vrawC,
#     title=r"$C(r)$ (Landau) (V channel)",
#     filename="{}/v-raw".format(lpath),
#     trange=np.arange(1, 29, 3),
#     xrange=[0, 1.4],
#     log_on=True,
#     ylable=r"$C(r)$",
#     loca=3,
# )

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
