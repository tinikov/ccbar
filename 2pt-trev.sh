#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINDIR] [OFDIR] [IFDIR]"
	return
}

if [[ ! -d "$2" || ! -d "$4" || "$#" -lt 4 ]]; then
	usage
	exit 1
fi

BINDIR=$(dirname $2)/$(basename $2)
OFDIR=$(dirname $3)/$(basename $3)
IFDIR=$(dirname $4)/$(basename $4)

if [[ ! -d $OFDIR ]]; then
	mkdir -p $OFDIR
fi

$BINDIR/trev2 -n $1 -d $OFDIR $IFDIR/2pt.* # Time reversal
echo -e "\033[34m$OFDIR\033[0m: Finished calculating [C(t) + C(T - t)]/2!"
