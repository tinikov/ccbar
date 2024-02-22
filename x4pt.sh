#!/bin/bash
# version: 1.2

clear
echo "
Please select: 
1. Standard analysis (2pt)
2. Variational analysis (2pt)
0. Quit
"
read -p "Enter selection [0-2] > "

gtypes=(c4pt l4pt)
channels=(ps v)

for ifix in {0..1}; do
    GFIX=${gtypes[$ifix]}
    for ich in {0..1}; do
        CH=${channels[$ich]}
        # [C(n_t) + C(N_t - n_t)]/2
        ./4pt-trev.sh 32 64 bin data/$GFIX/trev/$CH data/bin_ave/$GFIX/$CH
        # A1+
        ./4pt-a1plus.sh 32 64 bin data/$GFIX/a1plus/$CH data/$GFIX/trev/$CH
        # Jackknife resample
        ./4pt-jre.sh 32 64 bin data/$GFIX/jksam/$CH data/$GFIX/a1plus/$CH
        echo " "
    done
    echo " "
done
