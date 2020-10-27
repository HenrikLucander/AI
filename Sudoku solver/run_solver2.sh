#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: `basename $0` <instance> <4|9>"
    exit
fi
instance=$1
n=$2
echo "Instance:"
cat $instance | ./print_sudoku.py $n "clue"
echo "Original solution:"
cat $instance.solution | ./print_sudoku.py $n "origvalue"
bin/enforce_atoms.py -to $instance -to $instance.solution tmp/solver$n-2.sm > tmp/instance.sm
echo "Your solutions:"
clasp tmp/instance.sm 10 --verbose=0 --project | ./print_sudoku.py $n