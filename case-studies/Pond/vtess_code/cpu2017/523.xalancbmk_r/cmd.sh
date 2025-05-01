#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./cpuxalan_r_base.lienz-perf-m64 -v t5.xml xalanc.xsl > ref-t5.out 2>> ref-t5.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
