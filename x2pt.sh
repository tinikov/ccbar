#!/bin/bash
# version: 1.0

# Time reversal
./2pttre.sh 64 bin data/raw/c2pt data/c2pt/trev Y
./2pttre.sh 64 bin data/raw/l2pt data/l2pt/trev Y

# Jackknife resampling
./2ptjre.sh 64 bin data/c2pt/trev data/c2pt/jsample Y
./2ptjre.sh 64 bin data/l2pt/trev data/l2pt/jsample Y

# Effective masses
./2pteffmass.sh 64 bin data/c2pt/jsample data/c2pt/effmass Y
./2pteffmass.sh 64 bin data/l2pt/jsample data/l2pt/effmass Y

# Jackknife averaging (2pt correlators and effective masses)
./2ptjave.sh 64 bin data/c2pt/jsample result/c2pt/corr 2pt Y
./2ptjave.sh 64 bin data/l2pt/jsample result/l2pt/corr 2pt Y

./2ptjave.sh 64 bin data/c2pt/effmass result/c2pt/effmass exp Y
./2ptjave.sh 64 bin data/l2pt/effmass result/l2pt/effmass exp Y

./2ptjave.sh 64 bin data/c2pt/effmass result/c2pt/effmass csh n
./2ptjave.sh 64 bin data/l2pt/effmass result/l2pt/effmass csh n