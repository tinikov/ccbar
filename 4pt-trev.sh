#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [OFPATH] [IFPATH]"
	exit 1
}

if [[ ! -d "$3" || ! -d "$5" || "$#" -lt 5 ]]; then
	usage
	exit 1
fi

ARRAY_LENGTH=$(($1 * $1 * $1))
T_HALF=$(($2 / 2))
BINPATH=$(dirname $3)/$(basename $3)
OFPATH=$(dirname $4)/$(basename $4)
IFPATH=$(dirname $5)/$(basename $5)

for ((it = 0; it <= T_HALF; it = it + 1)); do
	t1=$(printf "%02d" $it)
	t2=$(printf "%02d" $((($2 - it) % $2)))

	if [[ ! -d $OFPATH/$t1 ]]; then
		mkdir -p $OFPATH/$t1
	fi

	for gconf1 in $(ls $IFPATH/$t1); do
		gconf2=${gconf1/+$t1/+$t2}

		$BINPATH/mean -l $ARRAY_LENGTH -o $OFPATH/$t1/$gconf1 $IFPATH/$t1/$gconf1 $IFPATH/$t2/$gconf2
	done
	echo -e "\033[34m$OFPATH/$t1\033[0m: Finished calculating [C($t1) + C($t2)]/2!"
done
