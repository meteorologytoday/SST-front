#!/bin/bash

fig_dir=figures_exp02_sine_weakwind_200km

input_dirs=""
exp_names=""
input_dir_root="../16_SST_sine_weakwind/lab_sine"
#for dT in 000 020 040 060 080 100 ; do
for dT in 000 010 020 030 040 050 060 070 080 090 100 ; do
#for dT in 000 020 040 ; do
        for MLsetup in woML ; do
            for MLscheme in MYNN25 ; do 
                for wnm in 01 ; do
                    input_dirs="$input_dirs $input_dir_root/case_mph-off_dT${dT}_wnm${wnm}_${MLsetup}_U5_${MLscheme}"
                    exp_names="$exp_names $dT"
                done
            done
    done
done

output_dir=$fig_dir
mkdir -p $output_dir
N=2

dhr=6
for i in $( seq 0 5 ); do
#for i in 1 5 ; do
    
    ((j=j%N)); ((j++==0)) && wait

    hrs_beg=$( printf "%02d" $(( $i * $dhr )) )
    hrs_end=$( printf "%02d" $(( ($i + 1) * $dhr )) )
    output_name="$output_dir/comparison_total_flux_woML_${hrs_beg}-${hrs_end}.png"
    output_name_decomp="$output_dir/decomp_comparison_total_flux_woML_${hrs_beg}-${hrs_end}.png"

    python3 plot_comparison_total_flux_more_decomposition.py  \
        --input-dirs $input_dirs  \
        --exp-beg-time "2001-01-01 00:00:00" \
        --time-rng $hrs_beg $hrs_end \
        --x-rng 0 200        \
        --HFX-rng -15 10        \
        --LH-rng 10 35        \
        --exp-names $exp_names \
        --ref-exp-order 1 \
        --wrfout-data-interval 60 \
        --frames-per-wrfout-file 60 \
        --output $output_name \
        --output-decomp $output_name_decomp \
        --no-display 


    if [ ]; then
    output_name="$output_dir/comparison_woML_${hrs_beg}-${hrs_end}.png"
    python3 plot_comparison.py  \
        --input-dirs $input_dirs  \
        --exp-beg-time "2001-01-01 00:00:00" \
        --time-rng $hrs_beg $hrs_end \
        --exp-names $exp_names \
        --wrfout-data-interval 60 \
        --frames-per-wrfout-file 60 \
        --no-display \
        --output $output_name &

    fi
done

wait

echo "DONE!"
