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
LAP_DIR=$DATA_DIR/$XXPT/lap

ARRAY_LENGTH=$(($SPACESITES * $SPACESITES * $SPACESITES))
T_HALF=$(($TIMESITES / 2))

echo -e "Conducting KS(TD)-method for \033[1;35m$DATA_DIR/$XXPT\033[0m"
echo " "

O_DIR=result/$XXPT/FKS-TD
LN_DIR=$DATA_DIR/$XXPT/ddtln
FKS_DIR=$DATA_DIR/$XXPT/fks-td
rm -rf $O_DIR $LN_DIR $FKS_DIR

# F_{KS} (time-dependent)
echo "##  F_{KS} (time-dependent)l! "
echo "##  Time sites total (reversed): $T_HALF"
echo "##  Array length:                $ARRAY_LENGTH"
echo "#######################################"
TMAXEFF=$(($T_HALF - 1))
for T in {01..$TMAXEFF}; do
  echo -e "\033[1;35m$T\033[0m now..."
  tm=$(printf "%02d" $(($T - 1)))
  tp=$(printf "%02d" $(($T + 1)))
  mkdir -p $LN_DIR/$T
  mkdir -p $FKS_DIR/$T
  for psgauge in $(ls $SAMPLE_DIR/ps/$T); do
    ogauge=${psgauge/.ps./.}
    vgauge=${psgauge/.ps./.v.}
    vm=${vgauge/+$T/+$tm}
    vp=${vgauge/+$T/+$tp}
    psm=${psgauge/+$T/+$tm}
    psp=${psgauge/+$T/+$tp}

    $BIN_DIR/fks-td -l $ARRAY_LENGTH -of $FKS_DIR/$T/$ogauge -od $LN_DIR/$T/$ogauge $SAMPLE_DIR/v/$tm/$vm $SAMPLE_DIR/v/$tp/$vp $SAMPLE_DIR/ps/$tm/$psm $SAMPLE_DIR/ps/$tp/$psp $LAP_DIR/v/$T/$vgauge $LAP_DIR/ps/$T/$psgauge >/dev/null 2>&1
  done
done
echo " "

# Jackknife and finalize part
mkdir -p $O_DIR/binary

for T in $(ls $FKS_DIR); do
  echo -e "Jackknife average \033[1;35m$FKS_DIR/$T\033[0m ..."
  $BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/binary/$T $FKS_DIR/$T/4pt.*
  echo " "
done

$BIN_DIR/cart2sphr -s $SPACESITES -d $O_DIR -p "txt" $O_DIR/binary/*
