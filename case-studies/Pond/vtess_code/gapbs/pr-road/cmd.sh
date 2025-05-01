#!/bin/bash
export OMP_NUM_THREADS=8
${GAPBS_DIR}/pr -f ${GAPBS_GRAPH_DIR}/road.sg -i1000 -t1e-4 -n32 &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null

