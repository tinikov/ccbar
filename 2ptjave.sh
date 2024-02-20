#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINPATH] [DATAPATH] [INPREFIX] [OFNAME]"
	return
}

if [[ ! -d "$2" || ! -d "$3" || "$#" -ne 5 ]]; then
	usage
	exit 1
fi

# Read options
BINPATH=$(dirname $2)/$(basename $2)
DATAPATH=$(dirname $3)/$(basename $3)
OFNAME=$(dirname $5)/$(basename $5)
TXTOFNAME=$(dirname $5)/txt.$(basename $5)

$BINPATH/mean -l $1 -o $OFNAME -j -t $DATAPATH/$4.*
echo -e "\033[34m$DATAPATH\033[0m: Averaged to \033[33m$OFNAME\033[0m & \033[33m$TXTOFNAME\033[0m!"
