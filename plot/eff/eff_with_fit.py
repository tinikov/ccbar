#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import scienceplots

plt.style.use(["science", "nature"])

tsize = 64
cutoff = 2.1753
codeRoot = "/Volumes/X6/work/ccbar"

# Read data files
type = ["ps", "v", "s", "av", "t"]
hmass_c, hmass_l = [[] for _ in range(2)]

for i in range(5):
    hmass_c.append(
        np.loadtxt("{}/result/c2pt/effmass/txt.csh.{}".format(codeRoot, type[i]))
    )
    hmass_l.append(
        np.loadtxt("{}/result/l2pt/effmass/txt.csh.{}".format(codeRoot, type[i]))
    )

# Gauge
path = [
    "{}/fig/effmass/coulomb".format(codeRoot),
    "{}/fig/effmass/landau".format(codeRoot),
]  # C, L
for ipath in path:
    if not os.path.exists(ipath):
        os.makedirs(ipath)
data = [hmass_c, hmass_l]  # C, L

fig, ax = plt.subplots()

errbar_plot_style = {
    "markersize": 3.5,
    "markeredgewidth": 0.4,
    "linewidth": 0.25,
    "fillstyle": "none",
}

legend_style = {
    "loc": 2,
    "bbox_to_anchor": (0.95, 1.03),
    "handletextpad": 0.5,
    "labelspacing": 0.3,
}

all_markers = ["o", "h", "v", "H", "p", "s", "^", "<", ">"]

index = np.arange(0, tsize, 1)
ntype = len(type)
for i in range(ntype):
    ax.errorbar(
        index + 0.5 + 0.06 * (i - np.ceil(ntype / 2)),
        data[0][i][:, 1] * cutoff,
        data[0][i][:, 2] * cutoff,
        label=type[i].upper(),
        **errbar_plot_style,
        fmt=all_markers[i]
    )

color_cycler = plt.rcParams['axes.prop_cycle'].by_key()['color']

ax.plot([25, 29], [2.9725, 2.9725], linestyle="-", linewidth="0.7", color=color_cycler[0])
ax.plot([24, 29], [3.0777, 3.0777], linestyle="-", linewidth="0.7", color=color_cycler[1])
ax.plot([13, 23], [3.426, 3.426], linestyle="-", linewidth="0.7", color=color_cycler[2])
ax.plot([10, 16], [3.473, 3.473], linestyle="-", linewidth="0.7", color=color_cycler[3])
ax.plot([9, 17], [3.487, 3.487], linestyle="-", linewidth="0.7", color=color_cycler[4])

# Set grid (reserved)
ax.grid(which="major", color="#DDDDDD", linewidth=0.5)
ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)

ax.legend(**legend_style)

ax.set_xlabel(r"$n_t$")
ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
ax.set_xlim(5, 29)

ax.set_ylabel(r"$m_{\rm eff}\ [{\rm GeV}]$")
ax.set_ylim(2.84, 3.64)

fig.savefig("{}/closer_with_fit.png".format(path[0]), dpi=600)
plt.close()
