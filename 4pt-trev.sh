#!/bin/bash
# version: 1.2

# Remove the path length limit
ulimit -n 1024

# Usage
usage() {
	echo -e "\033[1;33mUSAGE:\033[0m $(basename $0) [XYZSIZE] [TSIZE] [BINDIR] [OFPATH] [IFPATH] [IF_PREFIX=4pt]"
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

if [[ ! -d $OFPATH ]]; then
	mkdir -p $OFPATH
fi

if [[ -z "$6" ]]; then
	IF_PREFIX="4pt"
else
	IF_PREFIX=$6
fi

for ((it = 0; it <= T_HALF; it = it + 1)); do
	t1=$(printf "%02d" $it)
	t2=$(printf "%02d" $(((TSIZE - it) % TSIZE)))
	for gconf1 in $(ls $IFPATH/$t1); do
		gconf2=${gconf1/+$t1/+$t2}
		$BIN_DIR/mean -l $ARRAY_LENGTH -o $TR_DIR/$type/$t1/$gconf1 $IFPATH/$t1/$gt1 $RAW_DIR/$type/$t2/$gconf2 >/dev/null 2>&1
	done
	echo -e "Averaging \033[1;35m$t1\033[0m and \033[1;35m$t2\033[0m to generate \033[1;35m$t1\033[0m now..."
done
echo " "
