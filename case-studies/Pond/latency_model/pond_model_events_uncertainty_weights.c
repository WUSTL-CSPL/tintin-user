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
#define TINTIN_SYSCALL_WEIGHTS_NR 549
#define EVENT_NUM 20

int tintin_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp, unsigned long flags) {
    	return syscall(TINTIN_SYSCALL_NR, hw, pid, cpu, grp, flags);
}

int tintin_event_open_weight(struct perf_event_attr *hw, pid_t pid, int cpu, int grp, unsigned long flags, unsigned int weight) {
    	return syscall(TINTIN_SYSCALL_WEIGHTS_NR, hw, pid, cpu, grp, flags, weight);
}

static const char* events[EVENT_NUM] = {
    "CPU_CLK_UNHALTED",
    "CYCLE_ACTIVITY.STALLS_L1D_MISS",
    "CYCLE_ACTIVITY.STALLS_L2_MISS",
    "CYCLE_ACTIVITY.STALLS_L3_MISS",
    "CYCLE_ACTIVITY.STALLS_MEM_ANY",
    "EXE_ACTIVITY.1_PORTS_UTIL",
    "EXE_ACTIVITY.2_PORTS_UTIL",
    "EXE_ACTIVITY.BOUND_ON_STORES",
    "EXE_ACTIVITY.EXE_BOUND_0_PORTS",
    "IDQ_UOPS_NOT_DELIVERED.CORE",
    "INST_RETIRED",
    "INT_MISC.RECOVERY_CYCLES_ANY",
    "L1D.REPLACEMENT",
    "L2_LINES_IN.ALL",
    "MEM_INST_RETIRED.ALL_LOADS",
    "MEM_INST_RETIRED.ALL_STORES",
    "OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_L3_MISS_DEMAND_DATA_RD",
    "OFFCORE_REQUESTS_OUTSTANDING.L3_MISS_DEMAND_DATA_RD_GE_6",
    "UOPS_ISSUED.ANY",
    "UOPS_RETIRED.RETIRE_SLOTS",
};

static unsigned int weights[EVENT_NUM] = {
    24,
    50,
    61,
    1010,
    20,
    132,
    37,
    70,
    75,
    195,
    5619,
    91,
    426,
    334,
    376,
    129,
    1008,
    233,
    41,
    59,
};

struct cmd_args {
    pid_t pid;
    long millis_read_period;
};

struct tintin_read_back {
    unsigned long long count;
    unsigned long long uncertainty;
};

#define USAGE "Usage: ./pond_model_events [pid] [milliseconds read period]"

volatile int received_exit_signal = 0;

void sig_handler(int signo)
{
  if (signo == SIGUSR1){
    received_exit_signal = 1;
  }
}

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
    
    return attr;
}


struct perf_event_attr attr[EVENT_NUM];
int fd[EVENT_NUM];
unsigned long long counts[EVENT_NUM];
unsigned long long uncertainty[EVENT_NUM];

int main(int argc, char *argv[])
{
    int ret = pfm_initialize();
    if (ret != PFM_SUCCESS) {
        errx(1, "cannot initialize library %s", pfm_strerror(ret));
    }

    struct cmd_args args;
    parse_cmd_args(argc, argv, &args);
    printf("here\n");   

    for (int i = 0; i < EVENT_NUM; i++){
        attr[i] = get_perf_event_attr(events[i]);
        fd[i] = tintin_event_open_weight(&attr[i], args.pid, -1, -1, 0, weights[i]);
        if (fd[i] < 0){
            printf("Opening event %s failed\n", events[i]);
        }

        // ioctl(fd[i], PERF_EVENT_IOC_RESET, 0);
        // ioctl(fd[i], PERF_EVENT_IOC_ENABLE, 0);
    }

    struct tintin_read_back tintin_data;
    while (!received_exit_signal){
        for (int i = 0; i < EVENT_NUM; i++){
            ret = read(fd[i], &tintin_data, sizeof(tintin_data));
            if (!ret){  
                printf("Failed reading %s\n", events[i]);
                continue;
            }

            counts[i] = tintin_data.count;
            uncertainty[i] = tintin_data.uncertainty;
        }


        for (int i = 0; i < EVENT_NUM; i++){
            printf("%s %llu %llu\n", events[i], counts[i], uncertainty[i]);
        }

        printf("\n\n");
        usleep(args.millis_read_period * 1000);
    }

    fflush(stdout);
    return 0;
}
