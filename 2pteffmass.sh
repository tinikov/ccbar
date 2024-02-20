#!/bin/bash
# version: 1.1

# Usage
usage() {
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [TSIZE] [BINDIR] [RDATADIR] [OFDIR] [IS_REFRESH]=Y/n"
	return
}

if [[ "$#" -ne 5 ]]; then
	usage
	exit 1
fi

# Remove the limit for file path length
ulimit -n 1024

# Read options
TSIZE=$1
BINDIR=$(dirname $2)/$(basename $2)
RDATADIR=$(dirname $3)/$(basename $3)
OFDIR=$(dirname $4)/$(basename $4)
IS_REFRESH=$5

if [[ -e "$OFDIR" && "$IS_REFRESH" = Y ]]; then
	rm -rf $OFDIR
fi

echo -e "Calculating effective masses by data from \033[1;35m$RDATADIR\033[0m"
echo " "

for type in $(ls $RDATADIR); do
	echo "Effective mass of \"$RDATADIR/$type\""
	mkdir -p $OFDIR/$type
	$BINDIR/effmass -n $TSIZE -d $OFDIR/$type $RDATADIR/$type/2pt.*
	echo " "
done

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "
