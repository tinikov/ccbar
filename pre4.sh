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
RAW_DIR=$DATA_DIR/raw/$XXPT

ARRAY_LENGTH=$(($SPACESITES * $SPACESITES * $SPACESITES))
T_HALF=$(($TIMESITES / 2))

echo -e "Pre-processing for \033[1;35m$RAW_DIR\033[0m"
echo " "

TR_DIR=$DATA_DIR/$XXPT/trev
A1_DIR=$DATA_DIR/$XXPT/a1plus
JR_DIR=$DATA_DIR/$XXPT/jsample
rm -rf $TR_DIR $A1_DIR $JR_DIR

for type in $(ls $RAW_DIR); do
  echo -e "Processing \033[1;35m$RAW_DIR/$type\033[0m"
  echo " "

  # Time reversal
  echo "##  Time reversal! "
  echo "##  Time sites total:    $TIMESITES"
  echo "##  Array length:        $ARRAY_LENGTH"
  echo "#######################################"
  for T in {00..$T_HALF}; do
    t1=$T
    t2=$(printf "%02d" $((($TIMESITES - $t1) % $TIMESITES)))
    echo -e "Averaging \033[1;35m$t1\033[0m and \033[1;35m$t2\033[0m to generate \033[1;35m$T\033[0m now..."
    mkdir -p $TR_DIR/$type/$t1
    for gauge in $(ls $RAW_DIR/$type/$t1); do
      gt1=$gauge
      gt2=${gauge/+$t1/+$t2}
      # $BIN_DIR/mean -l $ARRAY_LENGTH -o $TR_DIR/$type/$T/TR.$gauge $RAW_DIR/$type/$t1/$gt1 $RAW_DIR/$type/$t2/$gt2 >/dev/null 2>&1
      $BIN_DIR/mean -l $ARRAY_LENGTH -o $TR_DIR/$type/$T/$gauge $RAW_DIR/$type/$t1/$gt1 $RAW_DIR/$type/$t2/$gt2 >/dev/null 2>&1
    done
  done
  echo " "

  # A1+ Projection
  for T in {00..$T_HALF}; do
    echo -e "For \033[1;35m$T\033[0m ..."
    mkdir -p $A1_DIR/$type/$T
    # $BIN_DIR/a1plus -s $SPACESITES -d $A1_DIR/$type/$T -p A1 $TR_DIR/$type/$T/TR.*
    $BIN_DIR/a1plus -s $SPACESITES -d $A1_DIR/$type/$T $TR_DIR/$type/$T/4pt.*
  done
  echo " "

  # Jackknife resampling
  for T in {00..$T_HALF}; do
    echo -e "For \033[1;35m$T\033[0m ..."
    mkdir -p $JR_DIR/$type/$T
    # $BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR/$type/$T -p JR $A1_DIR/$type/$T/A1.*
    $BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR/$type/$T $A1_DIR/$type/$T/4pt.*
  done
  echo " "
done
