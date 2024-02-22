#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINDIR] [OFPATH] [IFDIR] [IFPREF]"
	return
}

if [[ ! -d "$2" || ! -d "$4" || "$#" -lt 5 ]]; then
	usage
	exit 1
fi

BINDIR=$(dirname $2)/$(basename $2)
OFPATH=$(dirname $3)/$(basename $3)
OFDIR=$(dirname $3)
IFDIR=$(dirname $4)/$(basename $4)

if [[ ! -d $OFDIR ]]; then
	mkdir -p $OFDIR
fi

$BINDIR/mean -l $1 -o $OFPATH -j -t $IFDIR/$IFPREF.*
echo -e "\033[34m$IFDIR\033[0m: Averaged to \033[33m$OFPATH\033[0m & \033[33m$OFPATH.txt\033[0m!"
