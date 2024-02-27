#!/bin/bash
# version: 1.2

gtypes=(c2pt l2pt)
channels=(av ps s t v)

for ifix in {0..1}; do
    GFIX=${gtypes[$ifix]}
    for ich in {0..4}; do
        CH=${channels[$ich]}
        # Prep
        ## [C(t) + C(T - t)]/2
        ./2pt-trev.sh 64 bin data/$GFIX/trev/$CH data/bin_ave/$GFIX/$CH
        ## Jackknife resampling
        ./2pt-jre.sh 64 bin data/$GFIX/jksamp/$CH data/$GFIX/trev/$CH

        # 2-point correlator
        ./2pt-jave.sh 64 bin result/$GFIX/corr "2pt.$CH" "bin" data/$GFIX/jksamp/$CH "2pt"

        # Effective masses
        ./2pt-eff.sh 64 bin data/$GFIX/effmass/$CH data/$GFIX/jksamp/$CH
        ./2pt-jave.sh 64 bin result/$GFIX/effmass "exp.$CH" "bin" data/$GFIX/effmass/$CH "exp"
        ./2pt-jave.sh 64 bin result/$GFIX/effmass "csh.$CH" "bin" data/$GFIX/effmass/$CH "csh"
        echo " "
    done
    echo " "
done
