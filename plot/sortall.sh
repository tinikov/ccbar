#!/bin/bash

cd $1
DATA_ROOT=$(pwd -P)

cd $DATA_ROOT

mkdir -p \
2ptC/s  \
2ptC/v  \
2ptC/t  \
2ptC/av \
2ptC/ps \
4ptC/s  \
4ptC/v  \
4ptC/t  \
4ptC/av \
4ptC/ps \
2ptL/s  \
2ptL/v  \
2ptL/t  \
2ptL/av \
2ptL/ps \
4ptL/s  \
4ptL/v  \
4ptL/t  \
4ptL/av \
4ptL/ps

find ./coulomb -name "2pt.s.*" -exec mv {} ./2ptC/s \;
find ./coulomb -name "2pt.v.*" -exec mv {} ./2ptC/v \;
find ./coulomb -name "2pt.t.*" -exec mv {} ./2ptC/t \;
find ./coulomb -name "2pt.av.*" -exec mv {} ./2ptC/av \;
find ./coulomb -name "2pt.ps.*" -exec mv {} ./2ptC/ps \;
find ./coulomb -name "4pt.s.*" -exec mv {} ./4ptC/s \;
find ./coulomb -name "4pt.v.*" -exec mv {} ./4ptC/v \;
find ./coulomb -name "4pt.t.*" -exec mv {} ./4ptC/t \;
find ./coulomb -name "4pt.av.*" -exec mv {} ./4ptC/av \;
find ./coulomb -name "4pt.ps.*" -exec mv {} ./4ptC/ps \;

find ./landau -name "2pt.s.*" -exec mv {} ./2ptL/s \;
find ./landau -name "2pt.v.*" -exec mv {} ./2ptL/v \;
find ./landau -name "2pt.t.*" -exec mv {} ./2ptL/t \;
find ./landau -name "2pt.av.*" -exec mv {} ./2ptL/av \;
find ./landau -name "2pt.ps.*" -exec mv {} ./2ptL/ps \;
find ./landau -name "4pt.s.*" -exec mv {} ./4ptL/s \;
find ./landau -name "4pt.v.*" -exec mv {} ./4ptL/v \;
find ./landau -name "4pt.t.*" -exec mv {} ./4ptL/t \;
find ./landau -name "4pt.av.*" -exec mv {} ./4ptL/av \;
find ./landau -name "4pt.ps.*" -exec mv {} ./4ptL/ps \;
