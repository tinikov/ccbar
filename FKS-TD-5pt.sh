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

ARRAY_LENGTH=$(($XYZSIZE * $XYZSIZE * $XYZSIZE))
T_HALF=$(($TSIZE / 2))

echo -e "Conducting KS(TD)-method for \033[1;35m$DATA_DIR/$X4PT\033[0m"
echo " "

O_DIR=result/$X4PT/FKS-TD-5pt
FKS_DIR=$DATA_DIR/$X4PT/fks-td-5pt
rm -rf $O_DIR $FKS_DIR

# F_{KS} (time-dependent)
echo "##  F_{KS} (time-dependent)! "
echo "##  Time sites total: $T_HALF"
echo "##  Array length:     $ARRAY_LENGTH"
echo "#######################################"
for ((it = 2; it < $T_HALF - 1; it = it + 1)); do
	t2m=$(printf "%02d" $(($it - 2)))
	t1m=$(printf "%02d" $(($it - 1)))
	T=$(printf "%02d" $it)
	t1p=$(printf "%02d" $(($it + 1)))
	t2p=$(printf "%02d" $(($it + 2)))

	echo -e "\033[1;35m$T\033[0m now..."

	mkdir -p $FKS_DIR/$T
	for psgauge in $(ls $SAMPLE_DIR/ps/$T); do
		ogauge=${psgauge/.ps./.}
		vgauge=${psgauge/.ps./.v.}
		v2m=${vgauge/+$T/+$t2m}
		v1m=${vgauge/+$T/+$t1m}
		v1p=${vgauge/+$T/+$t1p}
		v2p=${vgauge/+$T/+$t2p}
		ps2m=${psgauge/+$T/+$t2m}
		ps1m=${psgauge/+$T/+$t1m}
		ps1p=${psgauge/+$T/+$t1p}
		ps2p=${psgauge/+$T/+$t2p}

		$BIN_DIR/fks-td-5pt \
			-l $ARRAY_LENGTH \
			-o $FKS_DIR/$T/$ogauge \
			$SAMPLE_DIR/v/$t2m/$v2m \
			$SAMPLE_DIR/v/$t1m/$v1m \
			$SAMPLE_DIR/v/$t1p/$v1p \
			$SAMPLE_DIR/v/$t2p/$v2p \
			$SAMPLE_DIR/ps/$t2m/$ps2m \
			$SAMPLE_DIR/ps/$t1m/$ps1m \
			$SAMPLE_DIR/ps/$t1p/$ps1p \
			$SAMPLE_DIR/ps/$t2p/$ps2p \
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
