# #!/bin/bash
# ulimit -n 1024

# cd $1
# DATA_DIR=$(pwd -P)
# DATA_DIR_BASE=$(basename $DATA_DIR)
# LQCD_BASE_DIR=/home/puppy/LQCD
# SPACESITES=32

# cd $DATA_DIR

# rm -rf lap-tmp mc-tmp

# for config in $(ls raw/ps/00); do
#     conftmp=${config/TR.4pt.ps.+00./}
#     confbase=${conftmp/RC32x64_B1900Kud01378100Ks01364000C1715-/}

#     echo "###########################################################################"
#     echo start for $confbase
#     echo "###########################################################################"
#     echo ""
#     for time in {00..31}; do
#         echo "###########################################################################"
#         echo "$time without $confbase started at: "
#         date
#         echo "###########################################################################"
#         echo ""
#         for type in $(ls raw); do
#             thisconf=${config/TR.4pt.ps.+00/TR.4pt.$type.+$time}

#             # select one out to generate JK sample
#             mv raw/$type/$time/$thisconf $DATA_DIR

#             # make directory for laplacian tmp files
#             mkdir -p lap-tmp/$type

#             # calculate
#             echo "###########################################################################"
#             echo "Laplacian of \"$DATA_DIR_BASE/raw/$type/$time\" (without $confbase)"
#             echo "###########################################################################"
#             $LQCD_BASE_DIR/bin/recc_mc -spacelength $SPACESITES raw/$type/$time/TR.*

#             # move the tmp files
#             mv raw/$type/$time/lap.* lap-tmp/$type

#             # move JK sample back
#             mv $DATA_DIR/$thisconf raw/$type/$time
#         done

#         echo ""
#         echo "###########################################################################"
#         echo "Calculating m_c of $time (without $confbase)"
#         echo "###########################################################################"
#         for idata in $(ls lap-tmp/v); do
#             V_DATA=$idata
#             PS_DATA=${idata/.v./.ps.}
#             # V0_DATA=${idata/lap.TR.4pt.v./v0.}
#             MC_DATA=${idata/lap.TR.4pt.v./mc.}

#             mkdir -p mc-tmp/$time-$confbase

#             # $LQCD_BASE_DIR/bin/KSpot -v0 -spacelength $SPACESITES -ofname pot-tmp/v0/$time/$V0_DATA laplacian-tmp/v/$time/$V_DATA laplacian-tmp/ps/$time/$PS_DATA
#             $LQCD_BASE_DIR/bin/KSpot -vs -spacelength $SPACESITES -ofname mc-tmp/$time-$confbase/$MC_DATA lap-tmp/v/$V_DATA lap-tmp/ps/$PS_DATA
#         done

#         rm -rf lap-tmp

#         mkdir -p mc-tmp/$time
#         $LQCD_BASE_DIR/bin/space -spacelength $SPACESITES -sphout mc-tmp/$time/WO-$confbase mc-tmp/$time-$confbase/mc.*

#         rm -rf mc-tmp/$time-$confbase
#         echo ""
#         echo "###########################################################################"
#         echo "$time without $confbase finished at: "
#         date
#         echo "###########################################################################"
#         echo ""
#     done
# done
