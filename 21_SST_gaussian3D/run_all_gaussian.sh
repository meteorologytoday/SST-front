#!/bin/bash
trap 'kill $( jobs -p )' EXIT
( echo "Running case case_mph-off_dT100_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT100_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT100_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT100_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT100_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT100_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT075_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT075_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT075_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT075_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT075_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT075_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT050_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT050_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT050_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT050_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT050_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT050_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT025_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT025_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT025_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT025_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT025_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT025_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT000_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT000_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT000_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT000_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT000_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT000_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-25_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-25_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-25_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-25_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT-25_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-25_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-50_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-50_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-50_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-50_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-50_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-50_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT-75_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-75_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-75_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-75_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-75_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-75_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-100_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-100_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
( echo "Running case case_mph-off_dT-100_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-100_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
( echo "Running case case_mph-off_dT-100_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_mph-off_dT-100_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
wait
