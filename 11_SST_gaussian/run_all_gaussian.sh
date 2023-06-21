#!/bin/bash
( echo "Running case case_dT100_wid050_wML_YSU_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_wML_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[0]=$!
( echo "Running case case_dT100_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[1]=$!
( echo "Running case case_dT100_wid050_woML_YSU_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_woML_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[2]=$!
( echo "Running case case_dT100_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[3]=$!
( echo "Running case case_dT100_wid050_wMLweakstrat_YSU_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_wMLweakstrat_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[4]=$!
( echo "Running case case_dT100_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT100_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[5]=$!
( echo "Running case case_dT-100_wid050_wML_YSU_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_wML_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[6]=$!
( echo "Running case case_dT-100_wid050_wML_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_wML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[7]=$!
( echo "Running case case_dT-100_wid050_woML_YSU_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_woML_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[8]=$!
( echo "Running case case_dT-100_wid050_woML_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_woML_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[9]=$!
( echo "Running case case_dT-100_wid050_wMLweakstrat_YSU_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_wMLweakstrat_YSU_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[10]=$!
( echo "Running case case_dT-100_wid050_wMLweakstrat_MYNN3_wpkt01 " ; cd lab_gaussian/case_dT-100_wid050_wMLweakstrat_MYNN3_wpkt01 ; bash ./run_gaussian.sh ) & 
pid[11]=$!
pid_str=$(IFS=" "; echo "${pid[*]}")
echo "Going to trap kill: " $pid_str
trap "kill $pid_str; exit 1" INT
wait
