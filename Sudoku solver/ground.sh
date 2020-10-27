#!/bin/bash

n=$1
sol=$2
show=$3
if [ "$show" == "" ]; then
  show="value"
fi

cat $sol | bin/reify.py --ground --show $show