#!/bin/bash
# version: 1.1

gauges=(c2pt l2pt)
channels=(av ps s t v)

for igau in {0..1}; do
    GAU=${gauges[$igau]}
    if [[ -d result/$GAU ]]; then
        rm -rf result/$GAU
    fi
    for ich in {0..4}; do
        CH=${channels[$ich]}
        # [C(n_t) + C(N_t - n_t)]/2
        ./2pt-trev.sh 64 bin data/$GAU/trev/$CH data/$GAU/raw/$CH
        # Jackknife resampling
        ./2pt-jre.sh 64 bin data/$GAU/jre/$CH data/$GAU/trev/$CH
        # Effective masses
        ./2pt-eff.sh 64 bin data/$GAU/effmass/$CH data/$GAU/jre/$CH
        # Averaging (2ptcorr and effmass)
        ./2pt-jave.sh 64 bin result/$GAU/corr/2pt.$CH.bin data/$GAU/jre/$CH
        ./2pt-jave.sh 64 bin result/$GAU/effmass/exp.$CH.bin data/$GAU/effmass/$CH exp
        ./2pt-jave.sh 64 bin result/$GAU/effmass/csh.$CH.bin data/$GAU/effmass/$CH csh
        echo " "
    done
    echo " "
done
