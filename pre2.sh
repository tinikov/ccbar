#!/bin/zsh
# version: 1.0

if [ $# != 2 ]; then
  echo "\033[1mUSAGE:\033[0m $(basename $0) [TIMESITES] [XXPT]"
  exit 1
fi

ulimit -n 1024
TIMESITES=$1
XXPT=$2

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
RAW_DIR=$DATA_DIR/raw/$XXPT

echo -e "Pre-processing for \033[1;35m$RAW_DIR\033[0m"
echo " "

TR_DIR=$DATA_DIR/$XXPT/trev
JR_DIR=$DATA_DIR/$XXPT/jsample
rm -rf $TR_DIR $JR_DIR

for type in $(ls $RAW_DIR); do
  echo -e "Processing \033[1;35m$RAW_DIR/$type\033[0m"

  # Time reversal
  mkdir -p $TR_DIR/$type
  $BIN_DIR/trev2 -l $TIMESITES -d $TR_DIR/$type $RAW_DIR/$type/2pt.*

  # Jackknife resampling
  mkdir -p $JR_DIR/$type
  $BIN_DIR/jre -l $TIMESITES -d $JR_DIR/$type -v -t $TR_DIR/$type/2pt.*

  echo " "
done
