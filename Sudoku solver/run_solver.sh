#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: `basename $0` <instance> <4|9>"
    exit
fi
instance=$1
n=$2
echo "Instance:"
cat $instance | ./print_sudoku.py $n "value"
echo "Your solution:"

bin/enforce_atoms.py -t $instance tmp/solver$n.sm > tmp/instance.sm
clasp tmp/instance.sm 10 --verbose=0 | ./print_sudoku.py $n