#!/usr/bin/env python3

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

data_ps = np.loadtxt("{}/result/c4pt/corr/ps/txt.l2.28".format(codeRoot), np.float64)
data_t = np.loadtxt("{}/result/c4pt/t_wavef.txt".format(codeRoot), np.float64)

fig, ax = plt.subplots(figsize=(3.375, 2.53125), dpi=50)  # picture size

ax.errorbar(
    data_ps[:, 0] * a,
    data_ps[:, 1] * 2 * np.pi**0.5,
    data_ps[:, 2],
    label="PS channel",
    **style
)

rinit = 1e-10
r = np.linspace(rinit, 32, int(1e6))
ax.plot(r * a, data_t, label="T channel", linewidth=0.3)


ax.minorticks_on()
legend_default_style = {
    "frameon": False,
    "fontsize": 7,
    "labelspacing": 0.1,
}

ax.set_xlabel(r"$r\ [{\rm fm}]$", labelpad=-1)
ax.set(xlim=(0, 1.5))
# ax.set(xlim=(0, 1.0))
ax.set(ylim=(0, 0.6))
# ax.set(ylim=(0, 0.7))

ax.set_ylabel(r"$\psi(r)$")

fig.subplots_adjust(left=0.16, right=0.97, bottom=0.13, top=0.96)
ax.legend(loc="best", **legend_default_style)

fig.savefig("{}/fig/wavef_ps+t.png".format(codeRoot), dpi=600)
plt.close()
