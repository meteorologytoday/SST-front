#!/bin/bash

fig_dir=figures_exp02_compare_ML_and_bl_scheme

nproc=20

proc_cnt=0

for _ML in "wML" "woML"; do

    for _bl_scheme in "YSU" "MYNN3"; do
    
        input_file=../02_SST_gaussian/lab_gaussian/case_dT100_wid050_${_ML}_${_bl_scheme}_wpkt01/wrfout_d01_0001-01-01_00\:00\:00

        output_dir=$fig_dir/${_ML}_${_bl_scheme}

        mkdir -p $output_dir

        avg_len=2
        for t in $( seq 0 287 ); do
         
            output_file=$output_dir/$( printf "%03d" $t ).png

            title=""

            if [ "$_ML" = "wML" ] ; then
                title="$title with ML"
            elif [ "$_ML" = "woML" ] ; then
                title="$title without ML"
            fi

            title="$title, $_bl_scheme. Time: $(( $t * 10 )) min"
     
            python3 plot_snapshot.py  \
                --wrfout $input_file  \
                --time-idx $(( $avg_len * $t )) $(( $avg_len * $t + $avg_len - 1 ))  \
                --title "$title" \
                --output $output_file \
                --no-display &

            proc_cnt=$(( $proc_cnt + 1))
            
            if (( $proc_cnt >= $nproc )) ; then
                echo "Max proc reached: $nproc"
                wait
                proc_cnt=0
            fi
        done
    done

done
