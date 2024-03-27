#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [OFDIR] [OFPREF] [OFSUFFIX] [IFDIR] [IFPREF]"
	return
}

if [[ ! -d "$3" || ! -d "$7" || "$#" -lt 8 ]]; then
	usage
	exit 1
fi

# Read options
ARRAY_LENGTH=$(($1 * $1 * $1))
T_HALF=$(($2 / 2))
BINDIR=$(dirname $3)/$(basename $3)
OFDIR=$(dirname $4)/$(basename $4)
IFDIR=$(dirname $7)/$(basename $7)

for ((it = 0; it <= T_HALF; it = it + 1)); do
	t=$(printf "%02d" $it)

	if [[ ! -d $OFDIR ]]; then
		mkdir -p $OFDIR
	fi

	OFPATH=$OFDIR/$5.$t.$6

	$BINDIR/mean -l $ARRAY_LENGTH -o $OFPATH -j $IFDIR/$t/$8.*
done
$BINDIR/cart2sphr -n $1 -d $OFDIR -s "txt" $OFDIR/$5.*.$6

echo -e "\033[34m$IFDIR\033[0m: Averaged to \033[33m$OFDIR\033[0m!"
