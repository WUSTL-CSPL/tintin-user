#define _GNU_SOURCE

#include <assert.h>
#include <fcntl.h>
#include <linux/perf_event.h>
#include <linux/unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/file.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#include <err.h>
#include <errno.h>
#include <perfmon/pfmlib.h>
#include <perfmon/pfmlib_perf_event.h>


#define TINTIN_SYSCALL_NR 548
#define EVENT_NUM 24

int tintin_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp, unsigned long flags) {
    	return syscall(TINTIN_SYSCALL_NR, hw, pid, cpu, grp, flags);
}

static const char* events[EVENT_NUM] = {
    //Replaced these two events with CPU_CLK_UNHALTED, since the ".THREAD" and ".REF_TSC" modifiers don't exist in perf
    //"CPU_CLK_UNHALTED.THREAD",
    //"CPU_CLK_UNHALTED.REF_TSC",
    "CPU_CLK_UNHALTED",
    //Replaced INST_RETIRED.ANY with INST_RETIRED
    //"INST_RETIRED.ANY",
    "INST_RETIRED",
    "MEM_INST_RETIRED.ALL_LOADS",
    "MEM_INST_RETIRED.ALL_STORES",
    "L1D.REPLACEMENT",
    "L2_LINES_IN.ALL",
    "UNC_C_CLOCKTICKS",
    //Replaced UNC_UPI_TxL_FLITS.DATA:u0xf with UNC_UPI_TxL_FLITS.DATA
    // "UNC_UPI_TxL_FLITS.DATA",
    "UNC_UPI_TxL_FLITS.DATA",
    "UNC_M_CAS_COUNT.RD",
    "UNC_M_CAS_COUNT.WR",
    "IDQ_UOPS_NOT_DELIVERED.CORE",
    "UOPS_ISSUED.ANY",
    "INT_MISC.RECOVERY_CYCLES_ANY",
    "UOPS_RETIRED.RETIRE_SLOTS",
    "CYCLE_ACTIVITY.STALLS_MEM_ANY",
    "EXE_ACTIVITY.BOUND_ON_STORES",
    "EXE_ACTIVITY.1_PORTS_UTIL",
    "EXE_ACTIVITY.2_PORTS_UTIL",
    "EXE_ACTIVITY.EXE_BOUND_0_PORTS",
    "CYCLE_ACTIVITY.STALLS_L1D_MISS",
    "CYCLE_ACTIVITY.STALLS_L2_MISS",
    "CYCLE_ACTIVITY.STALLS_L3_MISS",
    "OFFCORE_REQUESTS_OUTSTANDING.L3_MISS_DEMAND_DATA_RD_GE_6",
    "OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_L3_MISS_DEMAND_DATA_RD"
};

// static const char* events[EVENT_NUM] = {
// "cpu-cycles",
// "instructions",
// "cache-references",
// "cache-misses",
// "branch-instructions",
// "branch-misses",
// "bus-cycles",
// "L1-dcache-loads",
// "L1-dcache-load-misses",
// "L1-dcache-stores",
// "L1-dcache-store-misses",
// "L1-dcache-prefetches",
// "L1-dcache-prefetch-misses",
// "LLC-loads",
// "LLC-load-misses",
// "LLC-stores",
// "LLC-store-misses",
// "LLC-prefetches",
// "LLC-prefetch-misses",
// "dTLB-loads",
// "dTLB-load-misses",
// "dTLB-stores",
// "dTLB-store-misses",
// "dTLB-prefetches",
// "dTLB-prefetch-misses",
// "iTLB-loads",
// "iTLB-load-misses",
// "branch-loads",
// "branch-load-misses",
// };

struct cmd_args {
    pid_t pid;
    long millis_read_period;
};

#define USAGE "Usage: ./pond_model_events [pid] [milliseconds read period]"

void parse_cmd_args(int argc, char* argv[], struct cmd_args *args){
    if (argc != 3){
        errx(1, USAGE);
    }

    char *end;
    pid_t pid = strtol(argv[1], &end, 10);
    if (end == argv[1] || *end != '\0' || errno == ERANGE){
        errx(1, "Error when parsing pid. Expected integer\n");
    }

    long millis_period = strtol(argv[2], &end, 10);
    if (end == argv[2] || *end != '\0' || errno == ERANGE){
        errx(1, "Error when parsing milliseconds read period. Expected integer\n");
    }

    args->pid = pid;
    args->millis_read_period = millis_period;
}

struct perf_event_attr get_perf_event_attr(const char* event){
    struct perf_event_attr attr;
    pfm_perf_encode_arg_t arg;
    memset(&arg, 0, sizeof(arg));
    memset(&attr, 0, sizeof(attr));
    
    arg.attr = &attr;
    arg.size = sizeof(pfm_perf_encode_arg_t);
    int ret = pfm_get_os_event_encoding(event, PFM_PLM3, PFM_OS_PERF_EVENT, &arg);
    if (!ret == PFM_SUCCESS){
        printf("%s %s\n", event, pfm_strerror(ret));
    }

    printf("period: %lld\n", attr.sample_period);
    printf("freq: %d\n", attr.freq);
    return attr;
}


struct perf_event_attr attr[EVENT_NUM];
int fd[EVENT_NUM];
unsigned long long counts[EVENT_NUM];

int main(int argc, char *argv[])
{
    int ret = pfm_initialize();
    if (ret != PFM_SUCCESS) {
        errx(1, "cannot initialize library %s", pfm_strerror(ret));
    }

    struct cmd_args args;
    parse_cmd_args(argc, argv, &args);

    for (int i = 0; i < EVENT_NUM; i++){
        attr[i] = get_perf_event_attr(events[i]);
        fd[i] = tintin_event_open(&attr[i], args.pid, -1, -1, 0);
        if (fd[i] < 0){
            printf("Opening event %s failed\n", events[i]);
        }

        // ioctl(fd[i], PERF_EVENT_IOC_RESET, 0);
        // ioctl(fd[i], PERF_EVENT_IOC_ENABLE, 0);
    }

    while (1){
        for (int i = 0; i < EVENT_NUM; i++){
            ret = read(fd[i], &counts[i], sizeof(&counts[i]));
            if (!ret){
                printf("Failed reading %s\n", events[i]);
            }
        }


        for (int i = 0; i < EVENT_NUM; i++){
            printf("%s %llu\n", events[i], counts[i]);
        }

        printf("\n\n");
        usleep(args.millis_read_period * 1000);
    }

    return 0;
}
