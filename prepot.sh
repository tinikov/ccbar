#!/bin/zsh
# version: 1.0

if [ $# != 3 ]; then
  echo "\033[1mUSAGE:\033[0m $(basename $0) [SPACESITES] [TIMESITES] [XXPT]"
  exit 1
fi

ulimit -n 1024
SPACESITES=$1
TIMESITES=$2
XXPT=$3

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
SAMPLE_DIR=$DATA_DIR/$XXPT/jsample

ARRAY_LENGTH=$(($SPACESITES * $SPACESITES * $SPACESITES))
T_HALF=$(($TIMESITES / 2))

O_DIR=result/$XXPT/prepot
LAP_DIR=$DATA_DIR/$XXPT/lap
rm -rf $O_DIR $LAP_DIR

# Pre-potential
for type in $(ls $SAMPLE_DIR); do
  echo -e "Pre-potential for \033[1;35m$SAMPLE_DIR/$type\033[0m"
  echo " "

  for T in {00..$T_HALF}; do
    echo -e "For \033[1;35m$T\033[0m ..."
    mkdir -p $LAP_DIR/$type/$T
    # $BIN_DIR/ppot -s $SPACESITES -d $LAP_DIR/$type/$T -p LAP $SAMPLE_DIR/$type/$T/*
    $BIN_DIR/ppot -s $SPACESITES -d $LAP_DIR/$type/$T $SAMPLE_DIR/$type/$T/*
    echo " "
  done
done

# Jackknife and finalize part
for type in $(ls $LAP_DIR); do
  mkdir -p $O_DIR/$type/binary
  for T in $(ls $LAP_DIR/$type); do
    echo -e "Jackknife average \033[1;35m$LAP_DIR/$type/$T\033[0m ..."
    $BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/$type/binary/$T $LAP_DIR/$type/$T/4pt.*
    echo " "
  done
  $BIN_DIR/cart2sphr -s $SPACESITES -d $O_DIR/$type -p "txt" $O_DIR/$type/binary/*
done
