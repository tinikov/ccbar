# #!/bin/bash
# ulimit -n 1024

# cd $1
# DATA_DIR=$(pwd -P)
# DATA_DIR_BASE=$(basename $DATA_DIR)
# LQCD_BASE_DIR=/home/puppy/LQCD
# SPACESITES=32

# cd $DATA_DIR

# # rm -rf mcfit-txt

# # for time in $(ls pot-tmp/vs); do
# #     mkdir -p mcfit-txt/$time

# #     echo "Processing with \"$DATA_DIR_BASE/pot-tmp/vs/$time\""
# #     $LQCD_BASE_DIR/bin/cart2sphr -c 2 pot-tmp/vs/$time/*

# #     mv pot-tmp/vs/$time/txtsphr.* mcfit-txt/$time
# # done

# for time in $(ls mcfit-txt); do
#     cp $LQCD_BASE_DIR/bin/mass_emp ./
#     mv mass_emp mc_$time
#     cp $LQCD_BASE_DIR/bin/para2_emp ./
#     mv para2_emp para_$time
#     $LQCD_BASE_DIR/bin/potfit.py -t $time -i mcfit-txt/$time/*
# done

# $LQCD_BASE_DIR/bin/collect.py
# rm mc_* para_*