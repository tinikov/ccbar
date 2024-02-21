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

# # Time reversal
# echo "##  Time reversal! "
# echo -e "##  Time sites total:  \033[1;35m$TSIZE\033[0m"
# echo "##  Array length:      $ARRAY_LENGTH"
# echo "#######################################"
# for ((it = 0; it <= T_HALF; it = it + 1)); do
# 	T=$(printf "%02d" $it)
# 	t1=$T
# 	t2=$(printf "%02d" $(((TSIZE - it) % TSIZE)))
# 	echo -e "Averaging \033[1;35m$t1\033[0m and \033[1;35m$t2\033[0m to generate \033[1;35m$T\033[0m now..."
# 	mkdir -p $TR_DIR/$type/$t1
# 	for gauge in $(ls $RAW_DIR/$type/$t1); do
# 		gt1=$gauge
# 		gt2=${gauge/+$t1/+$t2}
# 		$BIN_DIR/mean -l $ARRAY_LENGTH -o $TR_DIR/$type/$T/$gauge $RAW_DIR/$type/$t1/$gt1 $RAW_DIR/$type/$t2/$gt2 >/dev/null 2>&1
# 	done
# done
# echo " "

# # A1+ Projection
# for ((it = 0; it <= T_HALF; it = it + 1)); do
# 	T=$(printf "%02d" $it)
# 	echo -e "For \033[1;35m$T\033[0m ..."
# 	mkdir -p $A1_DIR/$type/$T
# 	$BIN_DIR/a1plus -n $XYZSIZE -d $A1_DIR/$type/$T $TR_DIR/$type/$T/4pt.*
# done
# echo " "

# # Jackknife resampling
# for ((it = 0; it <= T_HALF; it = it + 1)); do
# 	T=$(printf "%02d" $it)
# 	echo -e "For \033[1;35m$T\033[0m ..."
# 	mkdir -p $JR_DIR/$type/$T
# 	$BIN_DIR/jre -l $ARRAY_LENGTH -d $JR_DIR/$type/$T $A1_DIR/$type/$T/4pt.*
# done
# echo " "
