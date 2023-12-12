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

ARRAY_LENGTH=$((XYZSIZE * XYZSIZE * XYZSIZE))
T_HALF=$((TSIZE / 2))

O_DIR=result/$X4PT/preV
LAP_DIR=$DATA_DIR/$X4PT/lap
rm -rf $O_DIR $LAP_DIR

# Pre-potential
for type in $(ls $SAMPLE_DIR); do
	echo -e "Pre-potential for \033[1;35m$SAMPLE_DIR/$type\033[0m"
	echo " "

	for ((it = 0; it <= T_HALF; it = it + 1)); do
		T=$(printf "%02d" $it)
		echo -e "For \033[1;35m$T\033[0m..."
		mkdir -p $LAP_DIR/$type/$T
		$BIN_DIR/prev -n $XYZSIZE -d $LAP_DIR/$type/$T $SAMPLE_DIR/$type/$T/*
		echo " "
	done
done

# Jackknife and finalize part
for type in $(ls $LAP_DIR); do
	mkdir -p $O_DIR/$type/binary
	for T in $(ls $LAP_DIR/$type); do
		echo -e "Jackknife average \033[1;35m$LAP_DIR/$type/$T\033[0m..."
		$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/$type/binary/$T $LAP_DIR/$type/$T/4pt.*
		echo " "
	done
	$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR/$type -p "txt" $O_DIR/$type/binary/*
	echo " "
done

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
