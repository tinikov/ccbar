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
        ./4pt-jre.sh 32 64 bin data/$GFIX/jksamp/$CH data/$GFIX/a1plus/$CH

        # 4-point correlator
        ./4pt-norm.sh 32 64 bin data/$GFIX/norm/$CH data/$GFIX/jksamp/$CH
        ./4pt-jave+c2s.sh 32 64 bin result/$GFIX/corr "pl.$CH" "bin" data/$GFIX/jksamp/$CH "4pt"
        ./4pt-jave+c2s.sh 32 64 bin result/$GFIX/corr "l2.$CH" "bin" data/$GFIX/norm/$CH "l2"
        ./4pt-jave+c2s.sh 32 64 bin result/$GFIX/corr "nn.$CH" "bin" data/$GFIX/norm/$CH "nn"

        # [▽^2 C(r,t)]/C(r,t)
        ./4pt-prev.sh 32 64 bin data/$GFIX/prev/$CH data/$GFIX/jksamp/$CH
        ./4pt-jave+c2s.sh 32 64 bin result/$GFIX/prev "prev.$CH" "bin" data/$GFIX/prev/$CH "4pt"
        echo " "
    done
    # Kawanai-Sasaki (t-dep.)

    # Kawanai-Sasaki (t-indep.)
    echo " "
done
