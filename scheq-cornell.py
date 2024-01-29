#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.integrate import odeint


# Initialize
n = 32
array_length = int(n**3)
rmin = 3
rmax = 14
codeRoot = "/Volumes/X6/work/ccbar"


# Define Cornell potential
def cornell_fit(r, A, sigma, V0):
    return -A / r + sigma * r + V0


para = {
    "A": 1,
    "sigma": 0.1,
    "V0": 0.01,
}

# Make data
rawdata = np.loadtxt(
    "{}/result/c4pt/preV/ps/txt.29".format(codeRoot), dtype=np.float64
)[0:array_length]

mask = (rawdata[:, 0] > rmin) & (rawdata[:, 0] < rmax)
subdata = rawdata[mask]
sorted_indices = np.argsort(subdata[:, 0])

fitdata = subdata[sorted_indices]

fitsites = fitdata[:, 0]
fitprev = fitdata[:, 1]
fiterr = fitdata[:, 2]

# Fit
least_squares = LeastSquares(fitsites, fitprev, fiterr, cornell_fit)  # type: ignore
m = Minuit(least_squares, **para)
m.migrad()

A = np.float64(m.values["A"])
sigma = np.float64(m.values["sigma"])
V0 = np.float64(m.values["V0"])
print(sigma)


def cornell(y, r, E, A, sigma, V0):
    u, uprime = y
    dydt = [
        uprime,
        # (- A / r + sigma * r + V0) * u,  # PS channel
        (-E - A / r + sigma * r + V0 + 2 / r**2) * u,  # T channel
    ]
    return dydt


E = 0.20336045  # T channel (3, 12)
print(E / 0.2364 * 2.1753)
rinit = 1e-10
y0 = [rinit * 2, rinit**2]
r = np.linspace(rinit, 32, int(1e6))

sol = odeint(cornell, y0, r, args=(E, A, sigma, V0))

C = np.sqrt(np.sum(sol[:, 0] * sol[:, 0] * (32 - rinit) / 1e6))
plt.plot(r * 0.090713, sol[:, 0] / r / C, label="u(r)")
plt.legend(loc="best")
plt.xlabel("r")
plt.grid()
plt.show()

np.savetxt("{}/result/c4pt/t_wavef.txt".format(codeRoot), sol[:, 0] / r / C)
