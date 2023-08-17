#!/bin/zsh
# version: 1.0

if [ $# != 4 ]; then
    echo "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [X4PT] [TSITE]"
    exit 1
fi

ulimit -n 1024
XYZSIZE=$1
TSIZE=$2
X4PT=$3
T=$(printf "%02d" $4)

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
REC_DIR=$DATA_DIR/$X4PT/recursive

ARRAY_LENGTH=$(($XYZSIZE * $XYZSIZE * $XYZSIZE))
T_HALF=$(($TSIZE / 2))

echo -e "Recursive jackknife for T = \033[1;35m$T\033[0m"
echo " "

O_DIR=result/$X4PT/mc-err
rm -rf $O_DIR
mkdir -p $O_DIR/$T

for iconf in $(ls $REC_DIR); do
  SAMPLE_DIR=$REC_DIR/$iconf/jsample
  LAP_DIR=$REC_DIR/$iconf/lap

  FKS_DIR=$REC_DIR/$iconf/fks-td
  rm -rf $FKS_DIR

  # F_{KS} (time-dependent)
  echo -e "##  FKS: \033[1;35m$T-$iconf\033[0m..."
  echo "#######################################"
  
  tm=$(printf "%02d" $(($T - 1)))
  tp=$(printf "%02d" $(($T + 1)))
  mkdir -p $FKS_DIR/$T
  for psgauge in $(ls $SAMPLE_DIR/ps/$T); do
    ogauge=${psgauge/.ps./.}
    vgauge=${psgauge/.ps./.v.}
    vm=${vgauge/+$T/+$tm}
    vp=${vgauge/+$T/+$tp}
    psm=${psgauge/+$T/+$tm}
    psp=${psgauge/+$T/+$tp}

    $BIN_DIR/fks-td -l $ARRAY_LENGTH -o $FKS_DIR/$T/$ogauge $SAMPLE_DIR/v/$tm/$vm $SAMPLE_DIR/v/$tp/$vp $SAMPLE_DIR/ps/$tm/$psm $SAMPLE_DIR/ps/$tp/$psp $LAP_DIR/v/$T/$vgauge $LAP_DIR/ps/$T/$psgauge >/dev/null 2>&1
  done
  echo " "

  # Jackknife and finalize part
  mkdir -p $O_DIR/binary/$T

  echo -e "Jackknife average \033[1;35m$FKS_DIR/$T\033[0m ..."
  $BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/binary/$T/$iconf $FKS_DIR/$T/4pt.*
  echo " "
done

$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR/$T -p "txt" $O_DIR/binary/$T/*
