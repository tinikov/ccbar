#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINPATH] [DATAPATH] [IFPREFIX] [OFPREFIX]"
	return
}

if [[ ! -d "$2" || ! -d "$3" || "$#" -ne 5 ]]; then
	usage
	exit 1
fi

# Read options
BINPATH=$(dirname $2)/$(basename $2)
DATAPATH=$(dirname $3)/$(basename $3)

$BINPATH/jre -l $1 -p $5 -d $DATAPATH -v -t $DATAPATH/$4.* # Jackknife resampling
echo -e "\033[34m$DATAPATH\033[0m: Jackknife resampling done!"
