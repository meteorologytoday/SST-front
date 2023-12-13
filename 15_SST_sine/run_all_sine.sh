#!/bin/bash
trap 'kill $( jobs -p )' EXIT
( echo "Running case case_mph-on_dT000_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT000_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT000_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT000_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT000_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT000_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT000_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT000_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT010_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT010_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT010_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT010_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT010_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT010_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT010_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT010_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT020_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT020_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT020_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT020_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT020_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT020_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT020_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT020_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT030_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT030_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT030_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT030_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT030_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT030_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT030_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT030_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT040_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT040_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT040_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT040_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT040_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT040_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT040_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT040_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT050_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT050_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT050_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT050_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT050_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT050_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT050_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT050_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT060_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT060_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT060_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT060_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT060_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT060_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT060_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT060_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT070_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT070_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT070_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT070_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT070_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT070_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT070_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT070_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT080_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT080_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT080_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT080_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT080_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT080_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT080_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT080_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT090_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT090_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT090_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT090_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT090_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT090_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT090_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT090_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT100_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-on_dT100_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
wait
( echo "Running case case_mph-off_dT100_wnm01_woML_MYNN25 " ; cd lab_sine/case_mph-off_dT100_wnm01_woML_MYNN25 ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-on_dT100_wnm01_woML_YSU " ; cd lab_sine/case_mph-on_dT100_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
( echo "Running case case_mph-off_dT100_wnm01_woML_YSU " ; cd lab_sine/case_mph-off_dT100_wnm01_woML_YSU ; bash ./run_sine.sh ) & 
wait
