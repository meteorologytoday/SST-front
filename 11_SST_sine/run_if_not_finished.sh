#!/bin/bash

trap 'kill $( jobs -p )' EXIT

lab_dir=lab_sine

N=11
target_file=wrfout_d01_2001-01-04_23:00:00
#target_file=wrfout_d01_2001-01-08_23:00:00
for run_dir in $( ls $lab_dir ) ; do

    if ! [[ "$run_dir" =~ mph-off ]] ; then
        echo "Skip $run_dir "
        continue
    fi

    if ! [[ "$run_dir" =~ MYNN25 ]] ; then
        echo "Skip $run_dir "
        continue
    fi

    if ! [[ "$run_dir" =~ U15 ]] ; then
        echo "Skip $run_dir "
        continue
    fi

    if ! [[ "$run_dir" =~ Lx100 ]] ; then
        echo "Skip $run_dir "
        continue
    fi

    if ! [[ "$run_dir" =~ dT100 ]] ; then
        echo "Skip $run_dir "
        continue
    fi




    full_run_dir=$lab_dir/$run_dir

    # Test if wrfout is there
    if [ -f "$full_run_dir/$target_file" ]; then
        echo "Target file detected in $run_dir . Skip."
    else
        ((i=i%N)); ((i++==0)) && wait       
        echo "Run: $run_dir" 
        ( echo "Running case $run_dir " ; cd $full_run_dir ; bash ./run_sine.sh ) & 
    fi
done

wait
