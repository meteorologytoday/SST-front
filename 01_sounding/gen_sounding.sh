#!/bin/bash

SST_base=288.15 # 15 degC
RH=90
U=15
deltaGammaFt=3e-3
H_mix=1500.0
H_tpp=10000.0

python3 ideal_sounding.py --output input_sounding_wML.ref --Delta-Gamma-ft $deltaGammaFt --U $U --H-mix $H_mix --RH-mix $RH --RH-ft $RH --theta-sfc $SST_base

python3 ideal_sounding.py --output input_sounding_woML.ref --Delta-Gamma-ft $deltaGammaFt --U $U --H-mix $H_mix --RH-mix $RH --RH-ft $RH --theta-sfc $SST_base --dthetadz-mix 3e-3

# N = 5-3 s^-1 in the mixed layer
python3 ideal_sounding.py --output input_sounding_wML_weakstrat.ref --Delta-Gamma-ft $deltaGammaFt --U $U --H-mix $H_mix --RH-mix $RH --RH-ft $RH --theta-sfc $SST_base --dthetadz-mix .75e-3
