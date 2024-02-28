#!/bin/bash

#trap 'kill $( jobs -p )' EXIT

lab_dir=./lab_sine

target_file=wrfout_d01_2001-01-04_23:00:00
#target_file=wrfout_d01_2001-01-05_23:00:00
for run_dir in $( ls $lab_dir ) ; do


if [ ] ; then
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

#    if ! [[ "$run_dir" =~ dT100 ]] ; then
#        echo "Skip $run_dir "
#        continue
#    fi
fi



    full_run_dir=$lab_dir/$run_dir

    # Test if wrfout is there

    cwd=`pwd`
    if [ -f "$full_run_dir/$target_file" ]; then
        echo "Target file detected in $run_dir . Skip."
    else
        echo "Submitting the case: $run_dir" 
        cd $full_run_dir
        sbatch submit_cw3e-shared.sh
        #sbatch submit_cw3e-compute.sh
    fi
    cd $cwd
done

