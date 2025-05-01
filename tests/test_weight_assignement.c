/*
 ============================================================================
 Name        : branch_mispred.c
 Author      : John Demme
 Version     : Mar 21, 2011
 Description : A template for perf_event. Requires Linux 2.6.32 or higher
 ============================================================================
*/

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


#define EVENT_NUM 24


// perf counter syscall
 int perf_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp,
                     unsigned long flags)
 {
 	// printf("The syscall number is %d", __NR_perf_event_open);
     	return syscall(548, hw, pid, cpu, grp, flags);
 }


// tintin monitor syscall
int tintin_event_open_with_weight(struct perf_event_attr *hw, pid_t pid, int cpu, int grp,
                    unsigned long flags, unsigned int weight)
{
	// printf("The syscall number is %d", __NR_tintin_event_open_with_weight);
    	return syscall(549, hw, pid, cpu, grp, flags, weight);
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
        fd[i] = tintin_event_open_with_weight(&attr[i], getpid(), -1, -1, 0, i);
        if (fd[i] < 0)
        {
            printf("Opening the %luth event failed\n", i);
        }
    }
}


// Setup info for perf_event
struct perf_event_attr attr[EVENT_NUM];
int fd[EVENT_NUM];

// function implementation
int main(int argc, char *argv[])
{
    size_t i, y;
    uint64_t begin_values[EVENT_NUM], end_values[EVENT_NUM];
    int rc;
    unsigned int event_index;

    // Open 10 events hardware generic events
    event_index = 0;
    for (i = 0; i < 10; i++){
        attr[i].type = PERF_TYPE_HARDWARE;
        attr[i].config = event_index; // generic PMU event PERF_COUNT_HW_CPU_CYCLES = 0, all events can be found in "include/uapi/linux/perf_event.h"
        attr[i].disabled = 0;
        fd[i] = tintin_event_open_with_weight(&attr[i], getpid(), -1, -1, 0, i);
        if (fd[i] < 0)
        {
            printf("Opening the %luth event failed\n", i);
            perror("error:");
        }
        event_index++;
    }

    // Open 6 events cache generic events
    event_index = 0;
    for (i = 10; i < 16; i++){
        attr[i].type = PERF_TYPE_HW_CACHE;
        attr[i].config = event_index; // generic PMU event PERF_COUNT_HW_CPU_CYCLES = 0
        attr[i].disabled = 0;
        fd[i] = tintin_event_open_with_weight(&attr[i], getpid(), -1, -1, 0, i);
        if (fd[i] < 0)
        {
            printf("Opening the %luth event failed\n", i);
        }
        event_index++;
    }

    // Open 8 events RAM generic events
    event_index = 0;
    for (i = 16; i < 18; i++){
        attr[i].type = PERF_TYPE_RAW;
        attr[i].config = event_index; // generic PMU event PERF_COUNT_HW_CPU_CYCLES = 0
        attr[i].disabled = 0;
        fd[i] = tintin_event_open_with_weight(&attr[i], getpid(), -1, -1, 0, i);
        if (fd[i] < 0)
        {
            printf("Opening the %luth event failed\n", i);
        }
        event_index++;
    }

    // Read the count at the very beginning
    asm volatile("nop;"); // pseudo-barrier

    for (i = 0; i < 18; i++){
        if (fd[i] < 0){
            begin_values[i] = 0;
            continue;
        }
        rc = read(fd[i], &begin_values[i], sizeof(begin_values[i]));
        assert(rc);
    }

    /**
     * Synthetic workload
     */
    for (i = 0; i < 100000000; i++)
    {
        if (i % 3 == 0)
        {
            y += 1;
        }
    }

    printf("Output to avoid optimization: %lu\n", y);

    printf("---------------------------------------- \n");
    printf("----------Profiling Results------------- \n");
    printf("---------------------------------------- \n");

    // Read the counter
    for (i = 0; i < 18; i++){
        if (fd[i] < 0){
            end_values[i] = 0;
            continue;
        }
        rc = read(fd[i], &end_values[i], sizeof(begin_values[i]));
        assert(rc);
    }

    asm volatile("nop;"); // pseudo-barrier

    // Close the counter
    for (i = 0; i < 18; i++){
        close(fd[i]);
    }

    for (i = 0; i < 18; i++){
        printf("%lu\n", end_values[i] - begin_values[i]);
    }

    // Print part of the information
    printf("CPU Cycles:           %lu \n", end_values[0] - begin_values[0]);
    printf("Instructions:         %lu \n", end_values[1] - begin_values[1]);
    printf("IPC:                  %lf\n",
           ((double)end_values[1] - begin_values[1]) / (end_values[0] - begin_values[0]));

    printf("Branch misses:        %lu \n", end_values[5] - begin_values[5]);
    printf("Branch instructions:  %lu \n", end_values[4] - begin_values[4]);
    printf("Branch mispred. rate: %lf%%\n",
           100.0 * ((double)end_values[5] - begin_values[5]) / (end_values[4] - begin_values[4]));

    printf("Cache misses:        %lu \n", end_values[3] - begin_values[3]);
    printf("Cache references:  %lu \n", end_values[2] - begin_values[2]);
    printf("Cache misses rate: %lf%%\n",
           100.0 * ((double)end_values[3] - begin_values[3]) / (end_values[2] - begin_values[2]));

    printf("Bus Cycles:           %lu \n", end_values[6] - begin_values[6]);
    printf("\n");

    return 0;
}
