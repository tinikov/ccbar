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

O_DIR=$ROOT/result/$X4PT/corr
NORM_DIR=$DATA_DIR/$X4PT/norm
rm -rf $O_DIR $NORM_DIR

for type in $(ls $SAMPLE_DIR); do
	# Normalization, Jackknife and Finalization
	mkdir -p $O_DIR/$type/binary
	for ((it = 0; it <= T_HALF; it = it + 1)); do
		T=$(printf "%02d" $it)
		echo -e "Normalizing \033[1;35m$type/$T\033[0m ..."
		mkdir -p $NORM_DIR/$type/$T
		$BIN_DIR/norm -n $XYZSIZE -d $NORM_DIR/$type/$T $SAMPLE_DIR/$type/$T/4pt.*
		echo " "
		echo -e "Jackknife average \033[1;35m$type/$T\033[0m ..."
		$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/$type/binary/plain.$T $SAMPLE_DIR/$type/$T/4pt.*
		$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/$type/binary/nn.$T $NORM_DIR/$type/$T/nn.*
		$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/$type/binary/l2.$T $NORM_DIR/$type/$T/l2.*
		echo " "
	done
	$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR/$type -p "txt" $O_DIR/$type/binary/plain.*
	$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR/$type -p "txt" $O_DIR/$type/binary/nn.*
	$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR/$type -p "txt" $O_DIR/$type/binary/l2.*
	echo " "
done

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
