

#define PERF_TYPE_HARDWARE

#define PERF_COUNT_HW_CPU_CYCLES 0
#define PERF_COUNT_HW_INSTRUCTIONS 1
#define PERF_COUNT_HW_CACHE_REFERENCES 2
#define PERF_COUNT_HW_CACHE_MISSES 3
#define PERF_COUNT_HW_BRANCH_INSTRUCTIONS 4
#define PERF_COUNT_HW_BRANCH_MISSES 5
#define PERF_COUNT_HW_BUS_CYCLES 6
#define PERF_COUNT_HW_STALLED_CYCLES_FRONTEND 7
#define PERF_COUNT_HW_STALLED_CYCLES_BACKEND 8
#define PERF_COUNT_HW_REF_CPU_CYCLES 9
#define PERF_COUNT_HW_MAX 10

#define PERF_TYPE_HW_CACHE

#define PERF_COUNT_HW_CACHE_L1D 0
//  for measuring Level 1 Data Cache

#define PERF_COUNT_HW_CACHE_L1I 1
//  for measuring Level 1 Instruction Cache

#define PERF_COUNT_HW_CACHE_LL 2
//  for measuring Last-Level Cache

#define PERF_COUNT_HW_CACHE_DTLB 3
//  for measuring the Data TLB

#define PERF_COUNT_HW_CACHE_ITLB 4
//  for measuring the Instruction TLB

#define PERF_COUNT_HW_CACHE_BPU 5
//  for measuring the branch prediction unit

#define PERF_COUNT_HW_CACHE_NODE 6
//  for measuring local memory accesses

#define PERF_COUNT_HW_CACHE_MAX 7

#define __NR_tintin_event_open 548
