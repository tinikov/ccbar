#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

plt.rcParams["font.family"] = "Charter"
plt.rcParams["mathtext.fontset"] = "stix"

style = {
    "markersize": 3.8,
    "fmt": "x",
    "linewidth": 0.5,
    "capsize": 2.8,
    "capthick": 0.5,
}


def setup(ax, title, loca):
    ax.minorticks_on()
    ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)
    ax.legend(loc=loca, handletextpad=0.1)
    ax.set_title(title)


def all_plot(
    data,
    type,
    title,
    filename,
    log_on=False,
    xrange=None,
    yrange=None,
    cutoff=1.0,
    loca=0,
):
    fig, ax = plt.subplots()

    index = np.arange(0, 64, 1)
    for i in range(len(type)):
        ax.errorbar(
            index,
            data[i][:, 1] * cutoff,
            data[i][:, 2] * cutoff,
            label=type[i].upper(),
            **style
        )

    ax.minorticks_on()
    ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)
    ax.legend(loc=loca, handletextpad=0.1)
    ax.set_title(title)
    if not cutoff == 1.0:
        ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]")
    ax.set_xlabel(r"$n_t$")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    if log_on:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))
        ax.set_ylabel(r"$C(n_t)$")

    fig.tight_layout()
    fig.savefig("{}.pdf".format(filename))
    plt.close()


def type_compare_plot(exp, cosh, i, title, filename, xrange=None, yrange=None, loca=0):
    fig, ax = plt.subplots()

    index = np.arange(0, 64, 1)
    ax.errorbar(
        index, exp[i][:, 1] * 2.1753, exp[i][:, 2] * 2.1753, label="exp", **style
    )
    ax.errorbar(
        index, cosh[i][:, 1] * 2.1753, cosh[i][:, 2] * 2.1753, label="cosh", **style
    )

    setup(ax, title, loca)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]")
    ax.set_xlabel(r"$n_t$")
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.tight_layout()
    fig.savefig("{}.pdf".format(filename))
    plt.close()


def gauge_compare_plot(
    coulomb, landau, i, title, filename, xrange=None, yrange=None, cutoff=1.0, loca=0
):
    fig, ax = plt.subplots()

    index = np.arange(0, 64, 1)
    ax.errorbar(
        index,
        coulomb[i][:, 1] * 2.1753,
        coulomb[i][:, 2] * 2.1753,
        label="Coulomb",
        **style
    )
    ax.errorbar(
        index,
        landau[i][:, 1] * 2.1753,
        landau[i][:, 2] * 2.1753,
        label="Landau",
        **style
    )

    ax.minorticks_on()
    ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
    ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.8)
    ax.legend(loc=loca, handletextpad=0.1)
    ax.set_title(title)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    if not xrange is None:
        ax.set(xlim=(xrange[0], xrange[1]))

    ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}$]")
    ax.set_xlabel(r"$n_t$")
    if not yrange is None:
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.tight_layout()
    fig.savefig("{}.pdf".format(filename))
    plt.close()


type = ["ps", "v", "s", "av", "t"]
gauge = ["C", "L"]
corr_c, corr_l, hmass_c, hmass_l, emass_c, emass_l = [[] for _ in range(6)]

for i in range(5):
    corr_c.append(np.loadtxt("../result/c2pt/corr/txt.{}".format(type[i])))
    corr_l.append(np.loadtxt("../result/l2pt/corr/txt.{}".format(type[i])))
    emass_c.append(np.loadtxt("../result/c2pt/effmass/txt.exp.{}".format(type[i])))
    emass_l.append(np.loadtxt("../result/l2pt/effmass/txt.exp.{}".format(type[i])))
    hmass_c.append(np.loadtxt("../result/c2pt/effmass/txt.csh.{}".format(type[i])))
    hmass_l.append(np.loadtxt("../result/l2pt/effmass/txt.csh.{}".format(type[i])))

eeffyrange = [-2 * 2.1753, 2 * 2.1753]
heffyrange = [0, 2 * 2.1753]

##################################################
##
## PLOT
##
##################################################

figpath = "../fig"
corrpath = "../fig/corr"
corrpathc = "../fig/corr/c2pt"
corrpathl = "../fig/corr/l2pt"
effmpath = "../fig/effmass"
effmpathc = "../fig/effmass/coulomb"
effmpathl = "../fig/effmass/landau"

if not os.path.exists(figpath):
    os.mkdir(figpath)
if not os.path.exists(corrpath):
    os.mkdir(corrpath)
if not os.path.exists(effmpath):
    os.mkdir(effmpath)
if not os.path.exists(corrpathc):
    os.mkdir(corrpathc)
if not os.path.exists(corrpathl):
    os.mkdir(corrpathl)
if not os.path.exists(effmpathc):
    os.mkdir(effmpathc)
if not os.path.exists(effmpathl):
    os.mkdir(effmpathl)

# All
all_plot(
    corr_c,
    type,
    r"$c\bar{c}$ 2-point correlators (Coulomb)",
    "{}/all".format(corrpathc),
    log_on=True,
    yrange=[1e-26, 1e-1],
)
all_plot(
    corr_l,
    type,
    r"$c\bar{c}$ 2-point correlators (Landau)",
    "{}/all".format(corrpathl),
    log_on=True,
    yrange=[1e-26, 1e-1],
)
all_plot(
    emass_c,
    type,
    r"$c\bar{c}$ Effective masses (exp type) (Coulomb)",
    "{}/expall".format(effmpathc),
    yrange=eeffyrange,
    cutoff=2.1753,
)
all_plot(
    emass_l,
    type,
    r"$c\bar{c}$ Effective masses (exp type) (Landau)",
    "{}/expall".format(effmpathl),
    yrange=eeffyrange,
    cutoff=2.1753,
)
all_plot(
    hmass_c,
    type,
    r"$c\bar{c}$ Effective masses (cosh type) (Coulomb)",
    "{}/cshall".format(effmpathc),
    yrange=heffyrange,
    cutoff=2.1753,
    loca=4,
)
all_plot(
    hmass_l,
    type,
    r"$c\bar{c}$ Effective masses (cosh type) (Landau)",
    "{}/cshall".format(effmpathl),
    yrange=heffyrange,
    cutoff=2.1753,
    loca=4,
)

# type
type_compare_plot(
    emass_c,
    hmass_c,
    0,
    r"$c\bar{c}$ Effective mass (PS channel) (exp vs cosh) (Coulomb)",
    "{}/tvs_PS".format(effmpathc),
    xrange=[0.5, 31.5],
    yrange=[1.5, 3.1],
    loca=4,
)
type_compare_plot(
    emass_l,
    hmass_l,
    0,
    r"$c\bar{c}$ Effective mass (PS channel) (exp vs cosh) (Landau)",
    "{}/tvs_PS".format(effmpathl),
    xrange=[0.5, 31.5],
    yrange=[1.5, 3.1],
    loca=4,
)
type_compare_plot(
    emass_c,
    hmass_c,
    1,
    r"$c\bar{c}$ Effective mass (V channel) (exp vs cosh) (Coulomb)",
    "{}/tvs_V".format(effmpathc),
    xrange=[0.5, 31.5],
    yrange=[1.6, 3.2],
    loca=4,
)
type_compare_plot(
    emass_l,
    hmass_l,
    1,
    r"$c\bar{c}$ Effective mass (V channel) (exp vs cosh) (Landau)",
    "{}/tvs_V".format(effmpathl),
    xrange=[0.5, 31.5],
    yrange=[1.6, 3.2],
    loca=4,
)
type_compare_plot(
    emass_c,
    hmass_c,
    2,
    r"$c\bar{c}$ Effective mass (S channel) (exp vs cosh) (Coulomb)",
    "{}/tvs_S".format(effmpathc),
    xrange=[0.5, 31.5],
    yrange=[2.2, 3.6],
    loca=4,
)
type_compare_plot(
    emass_l,
    hmass_l,
    2,
    r"$c\bar{c}$ Effective mass (S channel) (exp vs cosh) (Landau)",
    "{}/tvs_S".format(effmpathl),
    xrange=[0.5, 31.5],
    yrange=[2.2, 3.6],
    loca=4,
)
type_compare_plot(
    emass_c,
    hmass_c,
    3,
    r"$c\bar{c}$ Effective mass (AV channel) (exp vs cosh) (Coulomb)",
    "{}/tvs_AV".format(effmpathc),
    xrange=[0.5, 31.5],
    yrange=[2.4, 3.8],
    loca=4,
)
type_compare_plot(
    emass_l,
    hmass_l,
    3,
    r"$c\bar{c}$ Effective mass (AV channel) (exp vs cosh) (Landau)",
    "{}/tvs_AV".format(effmpathl),
    xrange=[0.5, 31.5],
    yrange=[2.4, 3.8],
    loca=4,
)
type_compare_plot(
    emass_c,
    hmass_c,
    4,
    r"$c\bar{c}$ Effective mass (T channel) (exp vs cosh) (Coulomb)",
    "{}/tvs_T".format(effmpathc),
    xrange=[0.5, 31.5],
    yrange=[2.4, 3.8],
    loca=4,
)
type_compare_plot(
    emass_l,
    hmass_l,
    4,
    r"$c\bar{c}$ Effective mass (T channel) (exp vs cosh) (Landau)",
    "{}/tvs_T".format(effmpathl),
    xrange=[0.5, 31.5],
    yrange=[2.4, 3.8],
    loca=4,
)

# Gauge compare
gauge_compare_plot(
    emass_c,
    emass_l,
    0,
    r"$c\bar{c}$ Effective mass (PS channel) (Coulomb vs Landau)",
    "{}/gvs_PS".format(effmpath),
    xrange=[0.5, 28.5],
    yrange=[1.5, 3.1],
    loca=4,
)
gauge_compare_plot(
    emass_c,
    emass_l,
    1,
    r"$c\bar{c}$ Effective mass (V channel) (Coulomb vs Landau)",
    "{}/gvs_V".format(effmpath),
    xrange=[0.5, 28.5],
    yrange=[1.6, 3.2],
    loca=4,
)
gauge_compare_plot(
    emass_c,
    emass_l,
    2,
    r"$c\bar{c}$ Effective mass (S channel) (Coulomb vs Landau)",
    "{}/gvs_S".format(effmpath),
    xrange=[0.5, 28.5],
    yrange=[2.2, 3.6],
    loca=4,
)
gauge_compare_plot(
    emass_c,
    emass_l,
    3,
    r"$c\bar{c}$ Effective mass (AV channel) (Coulomb vs Landau)",
    "{}/gvs_AV".format(effmpath),
    xrange=[0.5, 28.5],
    yrange=[2.4, 3.8],
    loca=4,
)
gauge_compare_plot(
    emass_c,
    emass_l,
    4,
    r"$c\bar{c}$ Effective mass (T channel) (Coulomb vs Landau)",
    "{}/gvs_T".format(effmpath),
    xrange=[0.5, 28.5],
    yrange=[2.4, 3.8],
    loca=4,
)
