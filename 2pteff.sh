#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [TSIZE] [BINPATH] [DATAPATH] [IFPREFIX]"
	return
}

if [[ ! -d "$2" || ! -d "$3" || "$#" -ne 4 ]]; then
	usage
	exit 1
fi

# Read options
BINPATH=$(dirname $2)/$(basename $2)
DATAPATH=$(dirname $3)/$(basename $3)

$BINPATH/effmass -n $1 -d $DATAPATH $DATAPATH/$4.* >/dev/null 2>&1
echo -e "\033[34m$DATAPATH\033[0m: Effective mass calculation done!"
