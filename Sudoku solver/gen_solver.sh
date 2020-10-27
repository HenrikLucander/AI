#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: `basename $0` <4|9>"
    exit
fi
n=$1
./gen_solver.py $n > tmp/solver$n.fml
./ground.sh $n tmp/solver$n.fml > tmp/solver$n.sm