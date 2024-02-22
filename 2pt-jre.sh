#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINPATH] [OFPATH] [IFPATH]"
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

$BINPATH/jre -l $1 -v -t -d $OFPATH $IFPATH/2pt.* # Jackknife resampling
echo -e "\033[34m$OFPATH\033[0m: Jackknife resampling done!"
