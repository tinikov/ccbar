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

case $REPLY in
0)
    echo "Program terminated."
    exit
    ;;
1)
    gtypes=(c2pt l2pt)
    channels=(av ps s t v)

    for ifix in {0..1}; do
        GFIX=${gtypes[$ifix]}
        for ich in {0..4}; do
            CH=${channels[$ich]}
            # [C(n_t) + C(N_t - n_t)]/2
            ./2pt-trev.sh 64 bin data/$GFIX/trev/$CH data/bin_ave/$GFIX/$CH
            # Jackknife resampling
            ./2pt-jre.sh 64 bin data/$GFIX/jksamp/$CH data/$GFIX/trev/$CH
            # Effective masses
            ./2pt-eff.sh 64 bin data/$GFIX/effmass/$CH data/$GFIX/jksamp/$CH
            # Averaging (2ptcorr and effmass)
            ./2pt-jave.sh 64 bin result/$GFIX/corr/2pt.$CH.bin data/$GFIX/jksamp/$CH "2pt"
            ./2pt-jave.sh 64 bin result/$GFIX/effmass/exp.$CH.bin data/$GFIX/effmass/$CH "exp"
            ./2pt-jave.sh 64 bin result/$GFIX/effmass/csh.$CH.bin data/$GFIX/effmass/$CH "csh"
            echo " "
        done
        echo " "
    done
    ;;
2)
    echo "Under construction..."
    ;;
*)
    echo "Invalid entry" >&2
    exit 1
    ;;
esac
