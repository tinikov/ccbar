#!/bin/bash
# version: 1.0

if [ $# != 3 ]; then
  echo -e "\033[1mUSAGE:\033[0m $(basename $0) [MIN] [MAX] [X4PT]"
  exit 1
fi

ulimit -n 1024

MIN=$1
MAX=$2
X4PT=$3

ROOT=.
RESULT_DIR=$ROOT/result
DATA_DIR=$RESULT_DIR/$X4PT/mc-td

RESULT=$RESULT_DIR/$X4PT/mcWerr.txt
rm $RESULT

for ((i = 1; i < 28; i = i + 1)); do
  iT=$(printf "%02d" $i)
  echo "Fitting $iT..."
  ./mc-fit.py -s 32 -a 0.090713 -c 2.1753 -r $MIN $MAX $DATA_DIR/$iT/* >> $RESULT
done
