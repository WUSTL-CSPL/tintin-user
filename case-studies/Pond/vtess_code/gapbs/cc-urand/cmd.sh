#!/bin/bash
export OMP_NUM_THREADS=8
${GAPBS_DIR}/cc -f ${GAPBS_GRAPH_DIR}/urand.sg -n16 &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null

