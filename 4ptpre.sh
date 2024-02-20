#!/bin/bash
# version: 1.1

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [RDATADIR] [OFDIR] [IS_REFRESH]=Y/n"
	exit 1
}

if [[ "$#" -ne 3 ]]; then
fi

XYZSIZE=$1
TSIZE=$2
X4PT=$3

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
RAW_DIR=$DATA_DIR/raw/$X4PT

ARRAY_LENGTH=$((XYZSIZE * XYZSIZE * XYZSIZE))
T_HALF=$((TSIZE / 2))

echo -e "Pre-processing for \033[1;35m$RAW_DIR\033[0m"
echo " "

TR_DIR=$DATA_DIR/$X4PT/trev
A1_DIR=$DATA_DIR/$X4PT/a1plus
JR_DIR=$DATA_DIR/$X4PT/jsample
rm -rf $TR_DIR $A1_DIR $JR_DIR

for type in $(ls $RAW_DIR); do
	echo -e "Processing \033[1;35m$RAW_DIR/$type\033[0m"
	echo " "

	# Time reversal
	echo "##  Time reversal! "
	echo -e "##  Time sites total:  \033[1;35m$TSIZE\033[0m"
	echo "##  Array length:      $ARRAY_LENGTH"
	echo "#######################################"
	for ((it = 0; it <= T_HALF; it = it + 1)); do
		T=$(printf "%02d" $it)
		t1=$T
		t2=$(printf "%02d" $(((TSIZE - it) % TSIZE)))
		echo -e "Averaging \033[1;35m$t1\033[0m and \033[1;35m$t2\033[0m to generate \033[1;35m$T\033[0m now..."
		mkdir -p $TR_DIR/$type/$t1
		for gauge in $(ls $RAW_DIR/$type/$t1); do
			gt1=$gauge
			gt2=${gauge/+$t1/+$t2}
			$BIN_DIR/mean -l $ARRAY_LENGTH -o $TR_DIR/$type/$T/$gauge $RAW_DIR/$type/$t1/$gt1 $RAW_DIR/$type/$t2/$gt2 >/dev/null 2>&1
		done
	done
	echo " "

	# A1+ Projection
	for ((it = 0; it <= T_HALF; it = it + 1)); do
		T=$(printf "%02d" $it)
		echo -e "For \033[1;35m$T\033[0m ..."
		mkdir -p $A1_DIR/$type/$T
		$BIN_DIR/a1plus -n $XYZSIZE -d $A1_DIR/$type/$T $TR_DIR/$type/$T/4pt.*
	done
	echo " "

	# Jackknife resampling
	for ((it = 0; it <= T_HALF; it = it + 1)); do
		T=$(printf "%02d" $it)
		echo -e "For \033[1;35m$T\033[0m ..."
		mkdir -p $JR_DIR/$type/$T
		$BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR/$type/$T $A1_DIR/$type/$T/4pt.*
	done
	echo " "
done

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
