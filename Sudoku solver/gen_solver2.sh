#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: `basename $0` <4|9>"
    exit
fi
n=$1
./gen_solver2.py $n > tmp/solver$n-2.fml
./ground.sh $n tmp/solver$n-2.fml "origvalue,clue,value" > tmp/solver$n-2.sm