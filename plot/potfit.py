#!/usr/bin/env python3

import numpy as np
# import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

for gauge in ['C', 'L']:
    masslist = []
    paralist = []
    for i in range(0, 32):
        dname = '4pt{}.result/vs.{}'.format(gauge, str(i).rjust(2, '0'))
        data=np.genfromtxt(dname)

        min_distance = 1
        max_distance = 9

        mask_max = data[:, 0] > max_distance
        tmp = data[~mask_max]
        mask_min = tmp[:, 0] < min_distance
        newdata = tmp[~mask_min]
        order_indices = newdata[:, 0].argsort()
        order_data = newdata[order_indices]

        #############################################################################
        def gaussian(x, height, width, offset): return height*np.exp(-x**2/(2*width**2)) + offset
        def gaussian2(x, h1, w1, h2, w2, offset): return gaussian(x, h1, w1, 0) + gaussian(x, h2, w2, 0) + offset
        #############################################################################

        guess2 = [0.05, 2, 0.5, 0.8, -0.04]

        popt, pcov = curve_fit(gaussian2, order_data[:, 0], order_data[:, 1], p0=guess2, sigma=order_data[:, 2], maxfev=100000)

        mass = -popt[4]*2.1753**2/0.10805
        masslist.append(mass)
        paralist.append(popt)
        print(np.sqrt(np.diag(pcov)), file=sys.stderr)

    np.savetxt("allmass{}.txt".format(gauge), masslist)
    np.savetxt("allpara{}.txt".format(gauge), paralist)

        # print(popt)
        # print(np.sqrt(np.diag(pcov)))

        # plt.errorbar(order_data[:,0], order_data[:,1], order_data[:,2], lw=1, fmt="o", markersize=0.5, label='measurement')
        # plt.plot(np.arange(1, 23, 0.01), gaussian2(np.arange(1, 23, 0.01), *popt), lw=2, c='r', label='fit of 2 Gaussians')
        # plt.legend(loc='best')
        # plt.show()