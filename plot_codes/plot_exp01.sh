#!/bin/bash

fig_dir=figures_exp02_compare_ML_and_bl_scheme

nproc=20

proc_cnt=0

for dT in "-100" "100"; do
    for _ML in "wML" "woML"; do
        for _bl_scheme in "YSU" ; do
            input_dir=../11_SST_gaussian/lab_gaussian/case_dT${dT}_wid050_${_ML}_${_bl_scheme}_wpkt01

            output_dir=$fig_dir/dT${dT}/${_ML}_${_bl_scheme}

            mkdir -p $output_dir

            for t in $( seq 0 7 ); do
             
                hrs_beg=$( printf "%02d" $(( $t * 6 )) )
                hrs_end=$( printf "%02d" $(( ($t + 1) * 6 )) )

                output_name="$output_dir/comparison_woML_${hrs_beg}-${hrs_end}.png"
                extra_title=""

                if [ "$_ML" = "wML" ] ; then
                    extra_title="$extra_title with ML"
                elif [ "$_ML" = "woML" ] ; then
                    extra_title="$extra_title without ML"
                fi

                extra_title="$extra_title, $_bl_scheme. "
         
                python3 plot_snapshot.py  \
                    --input-dir $input_dir  \
                    --exp-beg-time "0001-01-01 00:00:00" \
                    --time-rng $hrs_beg $hrs_end \
                    --extra-title "$extra_title" \
                    --output $output_name \
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
done
