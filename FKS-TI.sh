#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

if [ $# != 4 ]; then
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [X4PT] [MDIFF]"
	exit 1
fi

ulimit -n 1024

XYZSIZE=$1
TSIZE=$2
X4PT=$3
MDIFF=$4

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
LAP_DIR=$DATA_DIR/$X4PT/lap

ARRAY_LENGTH=$((XYZSIZE * XYZSIZE * XYZSIZE))
T_HALF=$((TSIZE / 2))

echo -e "Conducting KS(TI)-method for \033[1;35m$DATA_DIR/$X4PT\033[0m"
echo " "

O_DIR=$ROOT/result/$X4PT/FKS-TI
FKS_DIR=$DATA_DIR/$X4PT/fks-ti
rm -rf $O_DIR $FKS_DIR

for ((it = 0; it < T_HALF; it = it + 1)); do
	T=$(printf "%02d" $it)
	echo -e "\033[1;35m$T\033[0m now..."
	mkdir -p $FKS_DIR/$T
	for psgauge in $(ls $LAP_DIR/ps/$T); do
		ogauge=${psgauge/.ps./.}
		vgauge=${psgauge/.ps./.v.}

		$BIN_DIR/fks-ti -l $ARRAY_LENGTH -m $MDIFF -o $FKS_DIR/$T/$ogauge $LAP_DIR/v/$T/$vgauge $LAP_DIR/ps/$T/$psgauge >/dev/null 2>&1
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
