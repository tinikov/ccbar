#!/bin/bash
# version: 1.0

# Time reversal
./corr2pt/tre2pt.sh 64 bin data/raw/c2pt data/c2pt/trev Y
./corr2pt/tre2pt.sh 64 bin data/raw/l2pt data/l2pt/trev Y

# Jackknife resampling
./corr2pt/jre2pt.sh 64 bin data/c2pt/trev data/c2pt/jsample Y
./corr2pt/jre2pt.sh 64 bin data/l2pt/trev data/l2pt/jsample Y

# Effective masses
./corr2pt/effmass2pt.sh 64 bin data/c2pt/jsample data/c2pt/effmass Y
./corr2pt/effmass2pt.sh 64 bin data/l2pt/jsample data/l2pt/effmass Y

# Jackknife averaging (2pt correlators and effective masses)
corr2pt/jave2pt.sh 64 bin data/c2pt/jsample result/c2pt/corr 2pt Y
corr2pt/jave2pt.sh 64 bin data/l2pt/jsample result/l2pt/corr 2pt Y

corr2pt/jave2pt.sh 64 bin data/c2pt/effmass result/c2pt/effmass exp Y
corr2pt/jave2pt.sh 64 bin data/l2pt/effmass result/l2pt/effmass exp Y

corr2pt/jave2pt.sh 64 bin data/c2pt/effmass result/c2pt/effmass csh n
corr2pt/jave2pt.sh 64 bin data/l2pt/effmass result/l2pt/effmass csh n