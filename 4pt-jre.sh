#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [OFDIR] [IFDIR]"
	exit 1
}

if [[ ! -d "$3" || ! -d "$5" || "$#" -lt 5 ]]; then
	usage
	exit 1
fi

ARRAY_LENGTH=$(($1 * $1 * $1))
T_HALF=$(($2 / 2))
BINDIR=$(dirname $3)/$(basename $3)
OFDIR=$(dirname $4)/$(basename $4)
IFDIR=$(dirname $5)/$(basename $5)

for ((it = 0; it <= T_HALF; it = it + 1)); do
	t=$(printf "%02d" $it)

	if [[ ! -d $OFDIR/$t ]]; then
		mkdir -p $OFDIR/$t
	fi

	$BINDIR/jre -l $ARRAY_LENGTH -d $OFDIR/$t $IFDIR/$t/4pt.*
done
echo -e "\033[34m$OFDIR\033[0m: Jackknife resampling done!"
