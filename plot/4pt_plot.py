#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

plt.rcParams['font.family'] = 'Charter'
plt.rcParams['mathtext.fontset'] = 'stix'

a = 0.090713

def setup(ax, title, loca, style):
    ax.minorticks_on()
    ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    ax.legend(**style)
    ax.set_title(title)


def gaussian(x, height, width, offset): return height*np.exp(-x**2/(2*width**2)) + offset
def gaussian2(x, h1, w1, h2, w2, offset): return gaussian(x, h1, w1, 0) + gaussian(x, h2, w2, 0) + offset


def all_plot(data, title, filename, trange, rLUnit=False, log_on=False, xrange=None, yrange=None, cutoff=1.0, loca=0, ylable='need a label!'):
    fig, ax = plt.subplots()

    style = {
        'markersize': 0.5,
        'fmt': 'o',
        'linewidth': 0.3,
        'capsize': 0.2,
        'capthick': 0.3
    }

    legend_style = {
        'loc': loca,
        'handletextpad': 0.05,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }

    if rLUnit:
        for i in trange:
            ax.errorbar(data[i][:, 0], data[i][:, 1], data[i][:, 2], label=r'$n_t=$'+str(i).rjust(2, '0'), **style)
        ax.set_xlabel(r'$n_r$')
    else:
        for i in trange:
            ax.errorbar(data[i][:, 0]*a, data[i][:, 1]*cutoff, data[i][:, 2]*cutoff, label=r'$n_t=$'+str(i).rjust(2, '0'), **style)
        ax.set_xlabel(r'$r\ [{\rm fm}]$')

    setup(ax, title, loca, legend_style)
    ax.set_ylabel(ylable)
    
    if (not xrange is None):
        ax.set(xlim=(xrange[0], xrange[1]))

    if (not yrange is None):
        ax.set(ylim=(yrange[0], yrange[1]))
    if log_on:
        ax.set_yscale('log')
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))

    fig.tight_layout()
    fig.savefig(
        "/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))


def all_plot_FKS(data, title, filename, trange, deltaE, xrange=None, yrange=None, loca=0, ylable='need a label!'):
    fig, ax = plt.subplots()

    style = {
        'markersize': 0.5,
        'fmt': 'o',
        'linewidth': 0.3,
        'capsize': 0.2,
        'capthick': 0.3
    }

    legend_style = {
        'loc': loca,
        'handletextpad': 0.05,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }

    for i in trange:
        ax.errorbar(data[i][:, 0]*a, data[i][:, 1]*2.1753/deltaE, data[i][:, 2]*2.1753/deltaE, label=r'$n_t=$'+str(i).rjust(2, '0'), **style)

    ax.set_xlabel(r'$r\ [{\rm fm}]$')

    setup(ax, title, loca, legend_style)
    ax.set_ylabel(ylable)
    
    if (not xrange is None):
        ax.set(xlim=(xrange[0], xrange[1]))

    if (not yrange is None):
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.tight_layout()
    # fig.savefig("/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))
    plt.show()


def all_plot_FKS_fit(data, fitpara, title, filename, trange, deltaE, xrange=None, yrange=None, loca=0, ylable='need a label!'):
    fig, ax = plt.subplots()

    style = {
        'markersize': 1.5,
        # 'markersize': 0.5,
        'fmt': 'o',
        'linewidth': 0.6,
        # 'linewidth': 0.3,
        'capsize': 0.2,
        # 'capthick': 0.3,
        'capthick': 0.6
    }

    stylefit = {
        'linewidth': 0.6
    }

    legend_style = {
        'loc': loca,
        'handletextpad': 0.2,
        'ncol': 2,
        'columnspacing': 0.5,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }
    axx = plt.gca()
    t_0 = trange[0]
    for i in trange:
        color = next(axx._get_lines.prop_cycler)['color']
        ax.errorbar(data[i][:, 0]*a+0.001/2*(i-t_0), -data[i][:, 1]*2.1753**2/deltaE, data[i][:, 2]*2.1753**2/deltaE, label=r'$n_t=$'+str(i).rjust(2, '0'), **style, color = color)
        ax.plot(np.arange(0, 23, 0.01)*a+0.001/2*(i-t_0), -gaussian2(np.arange(0, 23, 0.01), *fitpara[i])*2.1753**2/deltaE, label=r'$n_t=$'+str(i).rjust(2, '0')+' (fitted)', **stylefit, color = color)

    ax.set_xlabel(r'$r\ [{\rm fm}]$')

    setup(ax, title, loca, legend_style)
    ax.set_ylabel(ylable)
    
    if (not xrange is None):
        ax.set(xlim=(xrange[0], xrange[1]))

    if (not yrange is None):
        ax.set(ylim=(yrange[0], yrange[1]))

    ax.legend(**legend_style)

    fig.tight_layout()
    fig.savefig("/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))
    # plt.show()


def c_vs_l_plot(dataC, dataL, title, filename, rLUnit=False, log_on=False, xrange=None, yrange=None, cutoff=1.0, loca=0, ylable='need a label!'):
    fig, ax = plt.subplots()

    style = {
        # 'markersize': 0.5,
        # 'linewidth': 0.3,
        # 'capthick': 0.3,
        'markersize': 1.6,
        'linewidth': 0.5,
        'capthick': 0.5,

        'fmt': 'o',
        'capsize': 0.2,
    }

    legend_style = {
        'loc': loca,
        'handletextpad': 0.05,
        # 'labelspacing': 0.22,
        # 'prop': {'size': 8}
    }

    mcC = 1.878949898325150025
    mcL = 1.463468832360292460

    if rLUnit:
        ax.errorbar(dataC[:, 0], dataC[:, 1]/mcC, dataC[:, 2]/mcC, label=r'Coulomb', **style)
        ax.errorbar(dataL[:, 0], dataL[:, 1]/mcL, dataL[:, 2]/mcL, label=r'Landau', **style)
        # ax.errorbar(dataC[:, 0], -dataC[:, 1], dataC[:, 2], label='Coulomb', **style)
        # ax.errorbar(dataL[:, 0], -dataL[:, 1], dataL[:, 2], label='Landau', **style)
        ax.set_xlabel(r'$n_r$')
    else:
        ax.errorbar(dataC[:, 0]*a, dataC[:, 1]*cutoff, dataC[:, 2]*cutoff, label=r'Coulomb ($n_t=19$)', **style)
        ax.errorbar(dataL[:, 0]*a, dataL[:, 1]*cutoff, dataL[:, 2]*cutoff, label=r'Landau ($n_t=28$)', **style)
        ax.set_xlabel(r'$r\ [{\rm fm}]$')

    setup(ax, title, loca, legend_style)
    ax.set_ylabel(ylable)
    
    if (not xrange is None):
        ax.set(xlim=(xrange[0], xrange[1]))

    if (not yrange is None):
        ax.set(ylim=(yrange[0], yrange[1]))
    if log_on:
        ax.set_yscale('log')
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=15))

    fig.tight_layout()
    fig.savefig(
        "/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))


# make data:
timelist = []
for i in range(32):
    timelist.append(str(i).rjust(2, '0'))
timelist_fkstd = []
for i in range(1, 31):
    timelist_fkstd.append(str(i).rjust(2, '0'))

psC, vC, pspreC, vpreC, v0C, vsC = [[] for _ in range(6)]
psL, vL, pspreL, vpreL, v0L, vsL = [[] for _ in range(6)]
l2psC = []
l2psL = []

fkstdC = []
fkstdL = []
for i in range(1, 31):
    fkstdC.append(np.loadtxt("../result/c4pt/FKS-TD/txt.{T}".format(T=timelist_fkstd[i-1])))
    fkstdL.append(np.loadtxt("../result/l4pt/FKS-TD/txt.{T}".format(T=timelist_fkstd[i-1])))

# for i in range(32):
#     psC.append(np.loadtxt(
#         "4ptC.result/c0.ps.{number}".format(number=timelist[i])))
#     vC.append(np.loadtxt(
#         "4ptC.result/c0.v.{number}".format(number=timelist[i])))
#     pspreC.append(np.loadtxt(
#         "4ptC.result/lap.ps.{number}".format(number=timelist[i])))
#     vpreC.append(np.loadtxt(
#         "4ptC.result/lap.v.{number}".format(number=timelist[i])))
#     v0C.append(np.loadtxt(
#         "4ptC.result/v0.{number}".format(number=timelist[i])))
#     vsC.append(np.loadtxt(
#         "4ptC.result/vs.{number}".format(number=timelist[i])))
#     l2psC.append(np.loadtxt(
#         "4ptC.result/l2.ps.{number}".format(number=timelist[i])))

#     psL.append(np.loadtxt(
#         "4ptL.result/c0.ps.{number}".format(number=timelist[i])))
#     vL.append(np.loadtxt(
#         "4ptL.result/c0.v.{number}".format(number=timelist[i])))
#     pspreL.append(np.loadtxt(
#         "4ptL.result/lap.ps.{number}".format(number=timelist[i])))
#     vpreL.append(np.loadtxt(
#         "4ptL.result/lap.v.{number}".format(number=timelist[i])))
#     v0L.append(np.loadtxt(
#         "4ptL.result/v0.{number}".format(number=timelist[i])))
#     vsL.append(np.loadtxt(
#         "4ptL.result/vs.{number}".format(number=timelist[i])))
#     l2psL.append(np.loadtxt(
#         "4ptL.result/l2.ps.{number}".format(number=timelist[i])))
# mcC = np.loadtxt("4ptC.result/allmassC.txt")
# mcL = np.loadtxt("4ptL.result/allmassL.txt")
# fitparaC = np.loadtxt("4ptC.result/allparaC.txt")
# fitparaL = np.loadtxt("4ptL.result/allparaL.txt")

##################################################################################################

###################### 4pt corr #######################
# ####### Coulomb 4pt PS ########
# all_plot(psC, r'$\phi(r)/\phi(0)$ (Coulomb) (PS channel)', "corr_PS_4ptC", trange=np.arange(1, 29, 3), xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)
# all_plot(psC, r'Saturation of $\phi(r)/\phi(0)$ (Coulomb) (PS channel)', "corr_PS_4ptC_conv_1120", trange=np.arange(11, 20, 1), xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$')

# ####### Coulomb 4pt V ########
# all_plot(vC, r'$\phi(r)/\phi(0)$ (Coulomb) (V channel)', "corr_V_4ptC", trange=np.arange(1, 29, 3), xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)
# all_plot(vC, r'Saturation of $\phi(r)/\phi(0)$ (Coulomb) (V channel)', "corr_V_4ptC_conv", trange=np.arange(22, 29, 1), xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$')

# ######## Landau 4pt V ########
# all_plot(psL, r'$\phi(r)/\phi(0)$ (Landau) (PS channel)', "corr_PS_4ptL", trange=np.arange(1, 29, 3), xrange=[0, 1.4], yrange=[1e-3, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)
# all_plot(psL, r'Saturation of $\phi(r)/\phi(0)$ (Landau) (PS channel)', "corr_PS_4ptL_conv", trange=np.arange(22, 29, 1), xrange=[0, 1.4], yrange=[1e-3, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$')

# ######## Landau 4pt V ########
# all_plot(vL, r'$\phi(r)/\phi(0)$ (Landau) (V channel)', "corr_V_4ptL", trange=np.arange(1, 29, 3), xrange=[0, 1.4], yrange=[1e-3, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)
# all_plot(vL, r'Saturation of $\phi(r)/\phi(0)$ (Landau) (V channel)', "corr_V_4ptL_conv", trange=np.arange(22, 29, 1), xrange=[0, 1.4], yrange=[1e-3, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$')

###################### Veff ######################
# ####### Coulomb Veff PS ########
# all_plot(pspreC, r'$V_{\rm eff}$ (PS) (Coulomb)', "lap_PS_C", rLUnit=True, xrange=[0, 15.5], yrange=[-1.5, 0.5], trange=np.arange(1, 29, 3), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)
# all_plot(pspreC, r'Saturation of $V_{\rm eff}$ (PS) (Coulomb)', "lap_PS_C_conv", rLUnit=True, xrange=[0, 15.5], yrange=[-1.5, 0.5], trange=np.arange(24, 29, 1), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)

# ####### Coulomb Veff V ########
# all_plot(vpreC, r'$V_{\rm eff}$ (V) (Coulomb)', "lap_V_C", rLUnit=True, xrange=[0, 15.5], yrange=[-1, 0.4], trange=np.arange(1, 29, 3), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)
# all_plot(vpreC, r'Saturation of $V_{\rm eff}$ (V) (Coulomb)', "lap_V_C_conv", rLUnit=True, xrange=[0, 15.5], yrange=[-1, 0.4], trange=np.arange(22, 29, 1), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)

# ######## Landau Veff PS ########
# all_plot(pspreL, r'$V_{\rm eff}$ (PS) (Landau)', "lap_PS_L", rLUnit=True, xrange=[0, 15.5], yrange=[-1.4, 0.2], trange=np.arange(1, 29, 3), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)
# all_plot(pspreL, r'Saturation of $V_{\rm eff}$ (PS) (Landau)', "lap_PS_L_conv", rLUnit=True, xrange=[0, 15.5], yrange=[-1.4, 0.2], trange=np.arange(22, 29, 1), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)

# ######## Landau Veff V ########
# all_plot(vpreL, r'$V_{\rm eff}$ (V) (Landau)', "lap_V_L", rLUnit=True, xrange=[0, 15.5], yrange=[-0.8, 0.1], trange=np.arange(1, 29, 3), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)
# all_plot(vpreL, r'Saturation of $V_{\rm eff}$ (V) (Landau)', "lap_V_L_conv", rLUnit=True, xrange=[0, 15.5], yrange=[-0.8, 0.1], trange=np.arange(22, 29, 1), ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=4)

########### Coulomb lap_V - lap_PS ############
# all_plot_FKS(vsC, r'Kawanai-Sasaki function (to estimate $m_c$) (Coulomb)', "F_KS_C", np.arange(1, 29, 3), 0.10805, xrange=[0, 1.4], yrange=[-12, 4], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)
# for i in range(10, 32):
#     all_plot_FKS_fit(vsC, fitparaC, r'Saturation of Kawanai-Sasaki function (to estimate $m_c$) (Coulomb)', "F_KS_C_conv_{}".format(str(i).rjust(2, '0')), [i], 0.10805, xrange=[0, 1], yrange=[-12, 4], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)
# all_plot_FKS_fit(vsC, fitparaC, r'Saturation of Kawanai-Sasaki function (to estimate $m_c$) (Coulomb)', "F_KS_C_conv_{}".format("16-22"), np.arange(16, 22), 0.10805, xrange=[0.6, 0.7], yrange=[1.8, 1.95], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)


########### Landau lap_V - lap_PS ############
# all_plot_FKS(vsL, r'Kawanai-Sasaki function (to estimate $m_c$) (Landau)', "F_KS_L", np.arange(1, 29, 3), 0.10805, xrange=[0, 1.4], yrange=[-12, 4], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)
# for i in range(10, 32):
#     all_plot_FKS_fit(vsL, fitparaL, r'Saturation of Kawanai-Sasaki function (to estimate $m_c$) (Landau)', "F_KS_L_conv_{}".format(str(i).rjust(2, '0')), [i], 0.10805, xrange=[0, 1], yrange=[-12, 4], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)
# all_plot_FKS_fit(vsL, fitparaL, r'Saturation of Kawanai-Sasaki function (to estimate $m_c$) (Landau)', "F_KS_L_conv", np.arange(25, 29, 1), 0.10805, xrange=[0.6, 0.8], yrange=[1.42, 1.52], ylable=r'$-F_{\rm KS}(\rightarrow m_c\ {\rm when}\ r \rightarrow \infty)\ [{\rm GeV}]$', loca=4)
all_plot_FKS(fkstdC, 'test', 'test', np.arange(1, 29, 3), 1, xrange=[0, 1.4], yrange=[-10, 7], ylable='test', loca=4)
all_plot_FKS(fkstdL, 'test', 'test', np.arange(1, 29, 3), 1, xrange=[0, 1.4], yrange=[-10, 7], ylable='test', loca=4)


################ Comparison between gauges #################
# ####### 4pt corr ########
# c_vs_l_plot(psC[19], psL[28], r'$\phi(r)/\phi(0)$ (PS channel) (Coulomb vs Landau)', "corr4pt_PS_gaugevs_19C28L", xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)
# c_vs_l_plot(l2psC[19], l2psL[28], r'$\phi(r)$ (normalized) (PS channel) (Coulomb vs Landau)', "l24pt_PS_gaugevs_19C28L", xrange=[0, 1.4], yrange=[1e-7, 1e-2], log_on=True, ylable=r'$\phi(r)$ (normalized)', loca=3)
# c_vs_l_plot(l2psC[19], l2psL[28], r'$\phi(r)$ (normalized) (PS channel) (Coulomb vs Landau)', "l24pt_PS_gaugevs_gauss_19C28L", xrange=[0, 1.4], ylable=r'$\phi(r)$ (normalized)', loca=3)
# c_vs_l_plot(vC[28], vL[28], r'$\phi(r)/\phi(0)$ (V channel) (Coulomb vs Landau) ($n_t=28$)', "corr4pt_V_typevs_nt28", xrange=[0, 1.4], yrange=[1e-4, 1.0], log_on=True, ylable=r'$\phi(r)/\phi(0)$', loca=3)

# ######### Veff ##########
# c_vs_l_plot(pspreC[19], pspreL[28], r'$V_{\rm eff}$ (PS channel) (Coulomb vs Landau) ($n_t=28$)', "lap_PS_typevs_C19L28_withmc", xrange=[0, 15.5], yrange=[-1, 0.4], rLUnit=True, ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=3)
# c_vs_l_plot(vpreC[28], vpreL[28], r'$V_{\rm eff}$ (V channel) (Coulomb vs Landau) ($n_t=28$)', "lap_V_typevs_nt28", xrange=[0, 15.5], yrange=[-1, 0.4], rLUnit=True, ylable=r'$\frac{\nabla^2\phi(r)}{\phi(r)}\cdot a^2$', loca=3)

########## lap_V - lap_PS ##########
# c_vs_l_plot(vsC[24], vsL[28], r'$\frac{\nabla^2\phi(r)_{PS}}{\phi(r)_{PS}} - \frac{\nabla^2\phi(r)_{V}}{\phi(r)_{V}}$ (Coulomb ($n_t=24$) vs Landau ($n_t=28$)) ', "lapV-PS_typevs_nt28", xrange=[-0.5, 12.5], rLUnit=True, yrange=[-0.65, 0.15], ylable=r'$(\frac{\nabla^2\phi(r)_{PS}}{\phi(r)_{PS}} - \frac{\nabla^2\phi(r)_{V}}{\phi(r)_{V}})\cdot a^2$')

# V0

# all_plot(v0C, r'Spin-independent potential (Coulomb)', "v0C", trange=np.arange(24, 29, 1), xrange=[0, 1.0], yrange=[-2.6, 0.8], ylable=r'$V_0(r)\ /\ {\rm Gev}$', cutoff=2.19410, loca=2)
# all_plot(v0L, r'Spin-independent potential (Landau)', "v0L", trange=np.arange(24, 29, 1), xrange=[0, 1.0], yrange=[-2, 0.6], ylable=r'$V_0(r)\ /\ {\rm Gev}$', cutoff=2.19410, loca=2)

########## Vs ##########
def vplot(dataC, dataL, title, filename, mcC, mcL, offsetC, offsetL, xrange=None, yrange=None, loca=0, ylable='need a label!'):
    fig, ax = plt.subplots()

    style = {
        'markersize': 1.8,
        'fmt': 'o',
        'linewidth': 0.7,
        'capsize': 0.2,
        'capthick': 0.7
    }

    legend_style = {
        'loc': loca,
        'handletextpad': 0.05,
    }

    ax.errorbar(dataC[:, 0]*a, offsetC+dataC[:, 1]*2.1753**2/mcC, dataC[:, 2]*2.1753**2/mcC, label='Coulomb', **style)
    ax.errorbar(dataL[:, 0]*a, offsetL+dataL[:, 1]*2.1753**2/mcL, dataL[:, 2]*2.1753**2/mcL, label='Landau', **style)
    ax.set_xlabel(r'$r\ [{\rm fm}]$')

    setup(ax, title, loca, legend_style)
    ax.set_ylabel(ylable)
    
    if (not xrange is None):
        ax.set(xlim=(xrange[0], xrange[1]))

    if (not yrange is None):
        ax.set(ylim=(yrange[0], yrange[1]))

    fig.tight_layout()
    fig.savefig("/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))
    # plt.show()

# mcC = 1
mcC = 1.878949898325150025
# mcL = 1
mcL = 1.463468832360292460
# offset = 0
offset = 0.10805

# vplot(vsC[19], vsL[28], r'Spin-dependent potential $V_s$ (Coulomb vs Landau)', "vs_typevs_19C28L", mcC, mcL, offset, offset, xrange=[0, 1], yrange=[-0.1, 2.2], ylable=r'$V_s(r)\ [{\rm Gev}]$')

# vplot(v0C[19], v0L[28], r'Spin-independent potential $V_0$ (Coulomb vs Landau)', "v0_typevs_19C28L", mcC, mcL, 3.054109-2*mcC, 3.054109-2*mcL, xrange=[0, 1], yrange=[-3.5, 1], ylable=r'$V_0(r)\ [{\rm Gev}]$')

# vplot(v0C[19], v0L[28], r'Spin-independent potential $V_0$ (Coulomb vs Landau) (shifted)', "v0off_typevs_19C28L", mcC, mcL, 3.054109-2*mcC, 3.114109-2*mcC, xrange=[0, 1], yrange=[-4, 0], ylable=r'$V_0(r)\ [{\rm Gev}]$')

# print(fitparaC[16])


# def all_plot_v0(data, title, filename, trange, mc=1, Ediff=1, xrange=None, yrange=None, loca=0, ylable='need a label!'):
#     fig, ax = plt.subplots()

#     style = {
#         'markersize': 0.5,
#         'fmt': 'o',
#         'linewidth': 0.3,
#         'capsize': 0.2,
#         'capthick': 0.3
#     }

#     legend_style = {
#         'loc': loca,
#         'handletextpad': 0.05,
#         # 'labelspacing': 0.22,
#         # 'prop': {'size': 8}
#     }

#     t_0 = trange[0]
#     for i in trange:
#         ax.errorbar(data[i][:, 0]*a+0.001/2*(i-t_0), Ediff+data[i][:, 1]*2.1753**2/mc, data[i][:, 2]*2.1753**2/mc, label=r'$n_t=$'+str(i).rjust(2, '0'), **style)
#     ax.set_xlabel(r'$r\ [{\rm fm}]$')

#     setup(ax, title, loca, legend_style)
#     ax.set_ylabel(ylable)
    
#     if (not xrange is None):
#         ax.set(xlim=(xrange[0], xrange[1]))

#     if (not yrange is None):
#         ax.set(ylim=(yrange[0], yrange[1]))

#     fig.tight_layout()
#     fig.savefig(
#         "/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format(filename))
    
# all_plot_v0(v0C, r'Spin-independent potential (Coulomb)', "v0C", mc=mcC[20], Ediff=3.054109-2*mcC[20], trange=np.arange(14, 29, 2), xrange=[0, 1.0], yrange=[-2.5, 0.5], ylable=r'$V_0(r)\ /\ {\rm Gev}$', loca=4)
# all_plot_v0(v0C, r'Saturation of spin-independent potential (Coulomb)', "v0C_conv", mc=mcC[20], Ediff=3.054109-2*mcC[20], trange=np.arange(16, 22, 1), xrange=[0.5, 0.8], yrange=[-0.8, -0.2], ylable=r'$V_0(r)\ /\ {\rm Gev}$', loca=4)
# all_plot_v0(v0L, r'Spin-independent potential (Landau)', "v0L", mc=mcL[28], Ediff=3.054109-2*mcL[28], trange=np.arange(14, 29, 2), xrange=[0, 1.0], yrange=[-2.5, 0.5], ylable=r'$V_0(r)\ /\ {\rm Gev}$', loca=4)
# all_plot_v0(v0L, r'Spin-independent potential (Landau)', "v0L_conv", mc=mcL[28], Ediff=3.054109-2*mcL[28], trange=np.arange(24, 29, 1), xrange=[0.6, 0.8], yrange=[0.1, 0.4], ylable=r'$V_0(r)\ /\ {\rm Gev}$', loca=4)



# fig, ax = plt.subplots()

# style = {
#     'markersize': 1.5,
#     'fmt': 'o',
#     'linewidth': 0.6,
#     'capsize': 0.2,
#     'capthick': 0.6
# }

# stylefit = {
#     'linewidth': 0.6
# }

# legend_style = {
#     'loc': 1,
#     'handletextpad': 0.2,
#     'ncol': 2,
#     'columnspacing': 0.5,
# }
# axx = plt.gca()

# deltaE = 0.10805
# ic = 19
# il = 28
# color = next(axx._get_lines.prop_cycler)['color']

# ax.errorbar(vsC[ic][:, 0]*a, vsC[ic][:, 1]*2.1753**2/deltaE, vsC[ic][:, 2]*2.1753**2/deltaE, label=r'$m_c^{\rm (C)}\ (n_t=19)$', **style, color = color)
# ax.plot(np.arange(0, 23, 0.01)*a, gaussian2(np.arange(0, 23, 0.01), *fitparaC[ic])*2.1753**2/deltaE, label=r'$m_c^{\rm (C)}\ (n_t=19)$'+' (fitted)', **stylefit, color = color)

# color = next(axx._get_lines.prop_cycler)['color']

# ax.errorbar(vsL[il][:, 0]*a, vsL[il][:, 1]*2.1753**2/deltaE, vsL[il][:, 2]*2.1753**2/deltaE, label=r'$m_c^{\rm (L)}\ (n_t=28)$', **style, color = color)
# ax.plot(np.arange(0, 23, 0.01)*a, gaussian2(np.arange(0, 23, 0.01), *fitparaL[il])*2.1753**2/deltaE, label=r'$m_c^{\rm (L)}\ (n_t=28)$'+' (fitted)', **stylefit, color = color)


# ax.set_xlabel(r'$r\ [{\rm fm}]$')

# setup(ax, 'Kawanai-Sasaki function (to estimate $m_c$) (Coulomb vs Landau)', 4, legend_style)
# ax.set_ylabel(r'$F_{\rm KS}\ [{\rm GeV}]$')

# ax.set(xlim=(0, 1))
# ax.set(ylim=(-4, 4))

# ax.legend(**legend_style)

# fig.tight_layout()
# fig.savefig("/Users/chen/LQCD/results/ccbar_KS_32x64/4pt_fig/{}.pdf".format('fFKS_gaugevs_C19L28'))
