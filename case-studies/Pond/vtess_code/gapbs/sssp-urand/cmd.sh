#!/bin/bash
export OMP_NUM_THREADS=8
${GAPBS_DIR}/sssp -f ${GAPBS_GRAPH_DIR}/urand.wsg -n8 -d2 &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
