#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINPATH] [OFPATH] [IFPATH] [IF_PREFIX=2pt]"
	return
}

if [[ ! -d "$2" || ! -d "$4" || "$#" -lt 4 ]]; then
	usage
	exit 1
fi

BINPATH=$(dirname $2)/$(basename $2)
OFPATH=$(dirname $3)/$(basename $3)
IFPATH=$(dirname $4)/$(basename $4)

if [[ ! -d $OFPATH ]]; then
	mkdir -p $OFPATH
fi

if [[ -z "$5" ]]; then
	IF_PREFIX="2pt"
else
	IF_PREFIX=$5
fi

$BINPATH/effmass -n $1 -d $OFPATH $IFPATH/$IF_PREFIX.* >/dev/null 2>&1
echo -e "\033[34m$OFPATH\033[0m: Effective mass calculation done!"
