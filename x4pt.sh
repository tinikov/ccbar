#!/bin/bash
# version: 1.1

gauges=(c2pt l2pt)
channels=(av ps s t v)

for igau in {0..1}; do
    GAU=${gauges[$igau]}
    for ich in {0..4}; do
        CH=${channels[$ich]}
        DATAPATH=data/$GAU/$CH
        # [C(n_t) + C(N_t - n_t)]/2
        ./2pttre.sh 64 bin $DATAPATH 2pt tr
        # Jackknife resampling
        ./2ptjre.sh 64 bin $DATAPATH tr jre
        # Effective masses
        ./2pteff.sh 64 bin $DATAPATH jre
        # Averaging (2ptcorr and effmass)
        ./2ptjave.sh 64 bin $DATAPATH jre result/$GAU/2pt.$CH.bin
        ./2ptjave.sh 64 bin $DATAPATH exp result/$GAU/exp.$CH.bin
        ./2ptjave.sh 64 bin $DATAPATH csh result/$GAU/csh.$CH.bin
        echo " "
    done
    echo " "
done
