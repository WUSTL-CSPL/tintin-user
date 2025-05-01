#!/bin/bash

rm -rf perf.data selected.txt stride stride.txt tmp.txt without-debug profiling_results_dmon.txt 
clang++ stride_benchmark.cpp -g -o stride
objdump --dwarf=decodedline stride > stride.txt
awk 'NF>=3 && $2 ~ /^[0-9]+$/{print $1,$2,$3}' stride.txt > tmp.txt
mv tmp.txt stride.txt
cp stride without-debug
strip --strip-debug without-debug
# export PATH=/path/to/pmu-tools:$PATH
taskset -c 2,3 ./without-debug &
toplev.py -l1 --no-desc --core C2 -o profiling_results_dmon.txt sleep 1 &> /dev/null
val=$(grep Backend_Bound profiling_results_dmon.txt |awk '{printf "%d\n", $6}')
if (( $(echo "$val > 9.9" | bc -l) == 1 ))
then
  echo "Severe backend bound problems ($val% of pipeline slots) identified, enabling memory bound profiling";
  toplev.py -l2 --no-desc --core C2 -o profiling_results_dmon.txt sleep 1 &> /dev/null
  # Backend_Bound.Memory_Bound
  val=$(grep Backend_Bound.Memory_Bound profiling_results_dmon.txt | awk '{printf "%d\n", $6}')
  if (( $(echo "$val > 9.9" | bc -l) == 1 ))
  then
    echo "Severe memory bound problems ($val% of pipeline slots) identified, enabling L1/L2/L3 bound profiling";
    toplev.py -l3 --no-desc --core C2 -o profiling_results_dmon.txt sleep 1 &> /dev/null
  fi
fi


cat profiling_results_dmon.txt
