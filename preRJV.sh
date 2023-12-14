#!/bin/bash
# version: 1.0

if [ $# != 4 ]; then
	echo "USAGE: $(basename $0) [XYZSIZE] [TSIZE] [X4PT] [NCONF]"
	exit 1
fi

ulimit -n 1024
XYZSIZE=$1
TSIZE=$2
X4PT=$3
NCONF=$4

ROOT=.
BIN_DIR=$ROOT/bin
DATA_DIR=$ROOT/data
A1_DIR=$DATA_DIR/$X4PT/a1plus

ARRAY_LENGTH=$(($XYZSIZE * $XYZSIZE * $XYZSIZE))
T_HALF=$(($TSIZE / 2))

if [ $X4PT = c4pt ]; then
	GAUGE=C
elif [ $X4PT = l4pt ]; then
	GAUGE=L
fi

REC_DIR=$DATA_DIR/recursive

# Recursive Jackknife resampling & laplacian
for ((iconf = 0; iconf < $NCONF; iconf += 1)); do
	ibin=$(printf '%02d' $((iconf + 1)))
	TYPE=(ps v)
	for itype in ${TYPE[@]}; do
		for ((it = 0; it < $T_HALF + 1; it += 1)); do
			iT=$(printf '%02d' $it)

			# Remove current configuration from list
			THISPATH=$A1_DIR/$itype/$iT
			ALLCONF=($(ls -d $THISPATH/*))
			THISCONF=$THISPATH/4pt.$itype.+$iT.gfix_$GAUGE.BIN$ibin
			if [ ${ALLCONF[$iconf]} = $THISCONF ]; then
				unset 'ALLCONF[$iconf]'
			fi

			# Jackknife resample
			echo -e "JR: $GAUGE:$itype.$iT.BIN$ibin..."
			JR_DIR=$REC_DIR/BIN$ibin/$X4PT/jsample/$itype/$iT
			rm -rf $JR_DIR
			mkdir -p $JR_DIR
			$BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR ${ALLCONF[@]}

			# Calculate laplacian
			echo -e "LAP: $GAUGE:$itype.$iT.BIN$ibin..."
			LAP_DIR=$REC_DIR/BIN$ibin/$X4PT/lap/$itype/$iT
			rm -rf $LAP_DIR
			mkdir -p $LAP_DIR
			$BIN_DIR/prev -n $XYZSIZE -d $LAP_DIR $JR_DIR/*
		done
	done
done
