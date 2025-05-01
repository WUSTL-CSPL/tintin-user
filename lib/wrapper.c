
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


// tintin monitor syscall
int tintin_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp,
                    unsigned long flags)
{
	// printf("The syscall number is %d", __NR_tintin_event_open);
    	return syscall(548, hw, pid, cpu, grp, flags);
}


int open_hardware_generic_events(struct perf_event_attr* attr, int num, int* fd) {
    // The max number is 10
    if (num >= 10) {
        printf("The number of events exceeds the max.\n");
        return -1;
    }

    size_t i, y;
    for (i = 0; i < num; i++){
        attr[i].type = PERF_TYPE_HARDWARE;
        attr[i].config = i; // generic PMU event PERF_COUNT_HW_CPU_CYCLES = 0, all events can be found in "include/uapi/linux/perf_event.h"
        attr[i].disabled = 0;
        fd[i] = tintin_event_open(&attr[i], getpid(), -1, -1, 0);
        if (fd[i] < 0)
        {
            printf("Opening the %luth hardware event failed\n", i);
        }
    }
}