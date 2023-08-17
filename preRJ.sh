#!/bin/zsh
# version: 1.0

if [ $# != 3 ]; then
    echo "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [X4PT]"
    exit 1
fi

ulimit -n 1024
XYZSIZE=$1
TSIZE=$2
X4PT=$3

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
A1_DIR=$DATA_DIR/$X4PT/a1plus

ARRAY_LENGTH=$(($XYZSIZE * $XYZSIZE * $XYZSIZE))
T_HALF=$(($TSIZE / 2))

REC_DIR=$DATA_DIR/$X4PT/recursive
rm -rf $REC_DIR

for T in {00..$T_HALF}; do
  for type in $(ls $A1_DIR); do
    all_config=($(ls $A1_DIR/$type/$T))
    N=${#all_config[@]}
    for i in {1..$N}; do
      all_config[$i]=$A1_DIR/$type/$T/${all_config[$i]}
    done
    for i in {1..$N}; do
      conftmp=${all_config[$i]}
      all_config[$i]=
      confbase=${${conftmp##*.}#*-}

      echo -e "JR: \033[1;35m$type-$T-$confbase\033[0m..."
      JR_DIR=$REC_DIR/$confbase/jsample
      mkdir -p $JR_DIR/$type/$T
      $BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR/$type/$T $all_config

      echo -e "LAP: \033[1;35m$type-$T-$confbase\033[0m..."
      LAP_DIR=$REC_DIR/$confbase/lap
      mkdir -p $LAP_DIR/$type/$T
      $BIN_DIR/prev -n $XYZSIZE -d $LAP_DIR/$type/$T $JR_DIR/$type/$T/*

      all_config[$i]=$conftmp
    done
  done
done