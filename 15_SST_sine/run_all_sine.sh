#!/bin/bash
trap 'kill $( jobs -p )' EXIT
( echo "Running case case_mph-on_dT100_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT100_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT100_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT100_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT100_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT100_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT100_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT100_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT075_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT075_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT075_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT075_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT075_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT075_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT075_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT075_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT050_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT050_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT050_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT050_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT050_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT050_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT050_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT050_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT025_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT025_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT025_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT025_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT025_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT025_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT025_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT025_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT000_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT000_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT000_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT000_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT000_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT000_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT000_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT000_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-25_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT-25_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT-25_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT-25_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-25_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT-25_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT-25_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT-25_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-50_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT-50_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT-50_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT-50_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-50_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT-50_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT-50_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT-50_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-75_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT-75_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT-75_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT-75_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-75_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT-75_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT-75_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT-75_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-100_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT-100_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT-100_wnm06_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT-100_wnm06_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT-100_wnm06_woML_YSU " ; cd lab_sine/case_mph-on_dT-100_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT-100_wnm06_woML_YSU " ; cd lab_sine/case_mph-off_dT-100_wnm06_woML_YSU ; bash ./run_sine.sh ) & 
wait
