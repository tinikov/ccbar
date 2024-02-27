#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINDIR] [OFDIR] [OFPREF] [OFSUFFIX] [IFDIR] [IFPREF]"
	return
}

if [[ ! -d "$2" || ! -d "$6" || "$#" -lt 7 ]]; then
	usage
	exit 1
fi

BINDIR=$(dirname $2)/$(basename $2)
OFDIR=$(dirname $3)/$(basename $3)
IFDIR=$(dirname $6)/$(basename $6)

if [[ ! -d $OFDIR ]]; then
	mkdir -p $OFDIR
fi

OFPATH=$OFDIR/$4.$5

$BINDIR/mean -l $1 -o $OFPATH -j -t $IFDIR/$7.*
echo -e "\033[34m$IFDIR\033[0m: Averaged to \033[33m$OFPATH\033[0m & \033[33m$OFPATH.txt\033[0m!"
