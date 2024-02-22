#!/bin/bash
# version: 1.2

# Usage
usage() {
	echo -e "\033[1mUSAGE:\033[0m $(basename $0) [TSIZE] [BINDIR] [RDATADIR] [OFDIR] [PREFIX]"
	return
}

if [[ "$#" -ne 6 ]]; then
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
PREFIX=$5
IS_REFRESH=$6

if [[ -e "$OFDIR" && "$IS_REFRESH" = Y ]]; then
	rm -rf $OFDIR
fi

echo -e "Jackknife averaging data from \033[1;35m$RDATADIR\033[0m"
echo " "

for type in $(ls $RDATADIR); do
	echo "Processing \"$RDATADIR/$type\""
	mkdir -p $OFDIR/binary
	$BINDIR/mean -l $TSIZE -o $OFDIR/$PREFIX.$type -j -t $RDATADIR/$type/$PREFIX.*
	mv $OFDIR/$PREFIX.$type $OFDIR/binary
	echo " "
done

echo -e "\033[1;35mFinished!\033[0m\n"
echo " "

# Jackknife and finalize part
mkdir -p $O_DIR/binary

for T in $(ls $FKS_DIR); do
	echo -e "Jackknife average \033[1;35m$FKS_DIR/$T\033[0m ..."
	$BIN_DIR/mean -j -l $ARRAY_LENGTH -o $O_DIR/binary/$T $FKS_DIR/$T/4pt.*
	echo " "
done

$BIN_DIR/cart2sphr -n $XYZSIZE -d $O_DIR -p "txt" $O_DIR/binary/*
echo " "