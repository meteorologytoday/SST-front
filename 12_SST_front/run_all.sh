#!/bin/bash

trap 'kill $(jobs -p)' EXIT

N=6
cwd=$( pwd )
for casename in $( ls lab_front | grep YSU ); do
    
    ((i=i%N)); ((i++==0)) && wait

    echo "Running case: $casename"    
    cd lab_front/$casename
    ./run_front.sh &

    cd $cwd
done


wait
