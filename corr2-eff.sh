#!/bin/zsh
# version: 1.0

if [ $# != 2 ]; then
  echo "\033[1mUSAGE:\033[0m $(basename $0) [TSIZE] [X2PT]"
  exit 1
fi

ulimit -n 1024
TSIZE=$1
XXPT=$2

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
SAMPLE_DIR=$DATA_DIR/$XXPT/jsample

echo -e "Effective mass and finalization for \033[1;35m$XXPTDIR\033[0m"
echo " "

O_DIR=result/$XXPT
EFF_DIR=$DATA_DIR/$XXPT/effmass
rm -rf $O_DIR $EFF_DIR

# 2-pt Correlator
for type in $(ls $SAMPLE_DIR); do
  echo "Jackknife averaging \"$SAMPLE_DIR/$type\""

  mkdir -p $O_DIR/corr/binary
  $BIN_DIR/mean -l $TSIZE -o $O_DIR/corr/$type -j -t $SAMPLE_DIR/$type/2pt.*
  mv $O_DIR/corr/$type $O_DIR/corr/binary

  echo " "
done

# Effective mass
for type in $(ls $SAMPLE_DIR); do
  echo "Effective mass of \"$SAMPLE_DIR/$type\""

  mkdir -p $EFF_DIR/$type
  $BIN_DIR/effmass -n $TSIZE -d $EFF_DIR/$type $SAMPLE_DIR/$type/2pt.*

  mkdir -p $O_DIR/effmass/binary
  $BIN_DIR/mean -l $TSIZE -o $O_DIR/effmass/exp.$type -j -t $EFF_DIR/$type/exp.*
  $BIN_DIR/mean -l $TSIZE -o $O_DIR/effmass/csh.$type -j -t $EFF_DIR/$type/csh.*
  mv $O_DIR/effmass/exp.$type $O_DIR/effmass/csh.$type $O_DIR/effmass/binary

  echo " "
done