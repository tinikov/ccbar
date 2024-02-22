#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [OFPATH] [IFDIR] [IFPREF]"
	return
}

if [[ ! -d "$3" || ! -d "$5" || "$#" -lt 6 ]]; then
	usage
	exit 1
fi

# Read options
ARRAY_LENGTH=$(($1 * $1 * $1))
T_HALF=$(($2 / 2))
BINDIR=$(dirname $3)/$(basename $3)
OFPATH=$(dirname $4)/$(basename $4)
OFDIR=$(dirname $4)
IFDIR=$(dirname $5)/$(basename $5)
IFPREF=$6

for ((it = 0; it <= T_HALF; it = it + 1)); do
	t=$(printf "%02d" $it)

	if [[ ! -d $OFPATH/$t ]]; then
		mkdir -p $OFPATH/$t
	fi

	$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/binary/$T $FKS_DIR/$T/4pt.*
done
