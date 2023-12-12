#!/bin/bash
# version: 1.0

if [ $# != 3 ]; then
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [X4PT]"
	exit 1
fi

ulimit -n 1024

XYZSIZE=$1
TSIZE=$2
X4PT=$3

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
SAMPLE_DIR=$DATA_DIR/$X4PT/jsample
LAP_DIR=$DATA_DIR/$X4PT/lap

ARRAY_LENGTH=$((XYZSIZE * XYZSIZE * XYZSIZE))
T_HALF=$((TSIZE / 2))

echo -e "Conducting KS(TD)-method for \033[1;35m$DATA_DIR/$X4PT\033[0m"
echo " "

O_DIR=result/$X4PT/FKS-TD
FKS_DIR=$DATA_DIR/$X4PT/fks-td
rm -rf $O_DIR $FKS_DIR

# F_{KS} (time-dependent)
echo "##  F_{KS} (time-dependent)! "
echo "##  Time sites total: $T_HALF"
echo "##  Array length:     $ARRAY_LENGTH"
echo "#######################################"
for ((it = 1; it < T_HALF; it = it + 1)); do
	T=$(printf "%02d" $it)
	echo -e "\033[1;35m$T\033[0m now..."
	tm=$(printf "%02d" $((it - 1)))
	tp=$(printf "%02d" $((it + 1)))
	mkdir -p $FKS_DIR/$T
	for psgauge in $(ls $SAMPLE_DIR/ps/$T); do
		ogauge=${psgauge/.ps./.}
		vgauge=${psgauge/.ps./.v.}
		vm=${vgauge/+$T/+$tm}
		vp=${vgauge/+$T/+$tp}
		psm=${psgauge/+$T/+$tm}
		psp=${psgauge/+$T/+$tp}

		$BIN_DIR/fks-td \
			-l $ARRAY_LENGTH \
			-o $FKS_DIR/$T/$ogauge \
			$SAMPLE_DIR/v/$tm/$vm \
			$SAMPLE_DIR/v/$tp/$vp \
			$SAMPLE_DIR/ps/$tm/$psm \
			$SAMPLE_DIR/ps/$tp/$psp \
			$LAP_DIR/v/$T/$vgauge \
			$LAP_DIR/ps/$T/$psgauge \
			>/dev/null 2>&1
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

$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR -p "txt" $O_DIR/binary/*
echo " "

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
