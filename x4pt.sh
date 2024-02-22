#!/bin/bash
# version: 1.2

gtypes=(c4pt l4pt)
channels=(ps v)

for ifix in {0..1}; do
    GFIX=${gtypes[$ifix]}
    for ich in {0..1}; do
        CH=${channels[$ich]}
        # Prep
        ## [C(n_t) + C(N_t - n_t)]/2
        ./4pt-trev.sh 32 64 bin data/$GFIX/trev/$CH data/bin_ave/$GFIX/$CH
        ## A1+
        ./4pt-a1plus.sh 32 64 bin data/$GFIX/a1plus/$CH data/$GFIX/trev/$CH
        ## Jackknife resampling
        ./4pt-jre.sh 32 64 bin data/$GFIX/jksam/$CH data/$GFIX/a1plus/$CH

        # 4-point correlator
        # ./4pt-jave+c2s

        # [▽^2 C(r,t)]/C(r,t)
        ./4pt-prev.sh 32 64 bin data/$GFIX/prev/$CH data/$GFIX/jksam/$CH
        echo " "
    done
    # Kawanai-Sasaki (t-dep.)
    
    # Kawanai-Sasaki (t-indep.)
    echo " "
done
