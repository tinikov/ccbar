#!/usr/bin/env python3
##
# @file
# @brief  Single Exponential(cosh) Fit by iMinuit
#         for two point temporal correlation functions
# @author Noriyoshi Ishii
# @since  Mon Aug  3 17:03:19 JST 2020
#
# usage：
# ./fit.py -Tsites 32 -type cosh -range 5 10 -ifname pion.txt
#
# required options：
#   -Tsites
#   -range
#   -ifname
#

import argparse
import numpy as np
from iminuit import Minuit

parser = argparse.ArgumentParser(description="potential generator")

parser.add_argument(
    "--Tsites",
    "-Tsites",
    type=int,
    required=True,
    help="Number of sites along the temporal direction",
)
parser.add_argument(
    "--ifname", "-ifname", type=str, required=True, help="input file name"
)
parser.add_argument(
    "--range", "-range", type=int, nargs=2, required=True, help="fit range: t0, t1"
)
parser.add_argument(
    "--initial_values",
    "-initial_values",
    type=float,
    nargs=2,
    default=[1.0, 1.0],
    help="initial values [a, m]",
)
parser.add_argument(
    "--type",
    "-type",
    type=str,
    choices=["exp", "cosh"],
    default="exp",
    help="single exponential fit or single cosh fit",
)

args = parser.parse_args()

##
# chi^2 function for the single exponential fit
#
class ChiSquareSingleExp:
    def __init__(self, ifname, t0, t1):
        self.corr = np.loadtxt(ifname, dtype=np.float64)
        self.Tsites = len(self.corr)
        self.t0 = t0
        self.t1 = t1
        self.corr = self.corr[t0:t1].transpose()

    def __call__(self, a, m):
        Ndf = 2
        f = a * np.exp(-m * self.corr[0])
        chisq = np.sum(np.square((self.corr[1] - f) / self.corr[2]))

        return chisq


##
# chi^2 function for the single cosh fit
#
class ChiSquareSingleCosh:
    def __init__(self, ifname, t0, t1):
        self.corr = np.loadtxt(ifname)
        self.Tsites = len(self.corr)
        self.t0 = t0
        self.t1 = t1
        self.corr = self.corr[t0:t1].transpose()

    def __call__(self, a, m):
        Ndf = 2
        f = a * np.cosh(-m * (self.corr[0] - args.Tsites / 2.0))
        chisq = np.sum(np.square((self.corr[1] - f) / self.corr[2]))

        return chisq


#
# main part
#

if args.type == "exp":
    chiSquare = ChiSquareSingleExp(args.ifname, args.range[0], args.range[1])
else:
    chiSquare = ChiSquareSingleCosh(args.ifname, args.range[0], args.range[1])

print("fit.py attempts to fit '{}'".format(args.ifname))

m = Minuit(
    chiSquare,
    a=args.initial_values[0],
    error_a=0.1,
    m=args.initial_values[1],
    error_m=0.1,
    errordef=1,
)

m.migrad()

#
# Ndf: (Number of data) - (Number of parameters) - 1
#
#
Ndf = args.range[1] - args.range[0] - 2 - 1

print("chi^2/Ndf = {}".format(m.fval / Ndf))
print("a         = {}".format(m.values["a"]))
print("m         = {}".format(m.values["m"]))
print("")
# print("# ncalls  = {}".format(m.ncalls))
print("# range   = {} {}".format(args.range[0], args.range[1]))
