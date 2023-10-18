#!/bin/bash

fig_dir=figures_exp02_compare_ML_and_bl_scheme_mph-off

input_dirs=""
exp_names=""
input_dir_root="../11_SST_gaussian/lab_gaussian"
for dT in -100 -75 -50 -25 000 025 050 075 100 ; do
    for wid in 050 ; do
        for MLsetup in wML ; do
            for MLscheme in YSU ; do 
                for wpkt in 01 ; do
                    input_dirs="$input_dirs $input_dir_root/case_dT${dT}_wid${wid}_${MLsetup}_${MLscheme}_wpkt${wpkt}"
                    exp_names="$exp_names $dT"
                done
            done
        done
    done
done

exp_names=""
input_dirs=""
for dT in -100 -75 -50 -25 000 025 050 075 100 ; do
    for wid in 050 ; do
        for MLsetup in woML ; do
            for MLscheme in MYNN3 ; do 
                for wpkt in 01 ; do
                    input_dirs="$input_dirs $input_dir_root/case_mph-off_dT${dT}_wid${wid}_${MLsetup}_${MLscheme}_wpkt${wpkt}"
                    exp_names="$exp_names $dT"
                done
            done
        done
    done
done


output_dir=$fig_dir
mkdir -p $output_dir
N=1

for i in $( seq 0 7 ); do
    
    ((j=j%N)); ((j++==0)) && wait

    hrs_beg=$( printf "%02d" $(( $i * 6 )) )
    hrs_end=$( printf "%02d" $(( ($i + 1) * 6 )) )
    output_name="$output_dir/comparison_total_flux_wML_${hrs_beg}-${hrs_end}.png"

    python3 plot_comparison_total_flux.py  \
        --input-dirs $input_dirs  \
        --exp-beg-time "2001-01-01 00:00:00" \
        --time-rng $hrs_beg $hrs_end \
        --x-rng 400 800        \
        --HFX-rng 10 70        \
        --LH-rng 40 80        \
        --exp-names $exp_names \
        --wrfout-data-interval 60 \
        --frames-per-wrfout-file 60 \
        --no-display           \
        --output $output_name  &

    if [ ] ; then
    output_name="$output_dir/comparison_wML_${hrs_beg}-${hrs_end}.png"
    python3 plot_comparison.py  \
        --input-dirs $input_dirs  \
        --exp-beg-time "0001-01-01 00:00:00" \
        --time-rng $hrs_beg $hrs_end \
        --exp-names $exp_names \
        --no-display \
        --output $output_name &
    fi

done

wait

echo "DONE!"
