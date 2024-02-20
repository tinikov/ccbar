#!/bin/bash
# version: 1.0

# Usage
usage() {
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [MPS] [MV] [MC] [BINDIR] [RDATADIR] [OFDIR] [IS_REFRESH]=Y/n"
	return
}

if [ $# != 9 ]; then
	usage
	exit 1
fi

# Remove the limit for file path length
ulimit -n 1024

# Read options
XYZSIZE=$1
TSIZE=$2
MC=$3
MPS=$4
MV=$5
BINDIR=$(dirname $6)/$(basename $6)
RDATADIR=$(dirname $7)/$(basename $7)
OFDIR=$(dirname $8)/$(basename $8)
IS_REFRESH=$9

ARRAYLENGTH=$((XYZSIZE * XYZSIZE * XYZSIZE))
THALF=$((TSIZE / 2))

if [[ -e "$OFDIR" && "$IS_REFRESH" = Y ]]; then
	rm -rf $OFDIR
fi

echo -e "Calculating potential by data from \033[1;35m$RDATADIR\033[0m"
echo " "

for ((it = 0; it < THALF; it = it + 1)); do
	T=$(printf "%02d" $it)
	echo -e "Potential of t=\033[1;35m$T\033[0m"
	mkdir -p $OFDIR/v0/$T
	mkdir -p $OFDIR/vs/$T
	for psgauge in $(ls $RDATADIR/ps/$T); do
		ogauge=${psgauge/.ps./.}
		vgauge=${psgauge/.ps./.v.}

		$BINDIR/v-ti -l $ARRAYLENGTH -mps $MPS -mv $MV -mc $MC -ov0 $OFDIR/v0/$T/$ogauge -ovs $OFDIR/vs/$T/$ogauge $RDATADIR/v/$T/$vgauge $RDATADIR/ps/$T/$psgauge
	done
done
echo " "

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
