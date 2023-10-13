#!/bin/bash

fig_dir=figures_exp02_compare_ML_and_bl_scheme

input_dir=/home/t2hsu/projects/SST-front/11_SST_gaussian/lab_gaussian/case_mph-off_dT100_wid050_woML_MYNN3_wpkt01
#input_dir=/home/t2hsu/projects/SST-front/11_SST_gaussian/lab_gaussian/case_mph-off_dT100_wid050_woML_YSU_wpkt01

python3 budget_analysis.py  \
    --input-dir $input_dir  \
    --time-rng 12 13 \
    --timestep 60 \
    --title-template time \
    --overlay \
    --exp-beg-time 2001-01-01 \
    --output example.png

