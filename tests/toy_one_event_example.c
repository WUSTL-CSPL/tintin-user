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


struct tinin_read_back {
    long long count;
    int uncertainty;
};

// perf counter syscall
 int perf_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp,
                     unsigned long flags)
 {
 	// printf("The syscall number is %d", __NR_perf_event_open);
     	return syscall(__NR_perf_event_open, hw, pid, cpu, grp, flags);
 }


// tintin monitor syscall
int tintin_event_open(struct perf_event_attr *hw, pid_t pid, int cpu, int grp,
                    unsigned long flags)
{
	// printf("The syscall number is %d", __NR_tintin_event_open);
    	return syscall(548, hw, pid, cpu, grp, flags);
}


void print_bytes_in_long_long(long long value) {
    unsigned char* byte_ptr = (unsigned char*)&value;
    size_t num_bytes = sizeof(long long);
    printf("In Bytes: 0x");
    for (size_t i = 0; i < num_bytes; i++) {
        printf("%02X", byte_ptr[i]);
    }
    printf("\n");
}


// Setup info for perf_event
struct perf_event_attr attr[4];

// function implementation
int main(int argc, char *argv[])
{
    size_t i, y = 0;
    long long begin_values[EVENT_NUM], end_values[EVENT_NUM];
    int fd[EVENT_NUM], rc;
    unsigned int event_index;

    struct tinin_read_back count_and_uncertainty;

    attr[0].type = PERF_TYPE_HARDWARE;
    attr[0].config = 3; // 3 is cache misses generic PMU event PERF_COUNT_HW_CPU_CYCLES = 0, all events can be found in "include/uapi/linux/perf_event.h"
    attr[0].disabled = 0;
    fd[0] = tintin_event_open(&attr[0], getpid(), -1, -1, 0);
    if (fd[0] < 0)
    {
        printf("Opening the event failed \n");
    }

    // Read the count at the very beginning
    asm volatile("nop;"); // pseudo-barrier

    begin_values[0] = 0;
    rc = read(fd[0], &begin_values[0], sizeof(begin_values[0]));
    printf("Begin Count is %lld \n", begin_values[0]);
    print_bytes_in_long_long(begin_values[0]);
    // printf("Begin Count is 0x%x%x%x%x%x%x%x%x \n", *(&begin_values[0]), *(&begin_values[0]+1), *(&begin_values[0]+2),
	// 			*(&begin_values[0]+3), *(&begin_values[0]+4), *(&begin_values[0]+5), *(&begin_values[0]+6), *(&begin_values[0]+7));
    /**
     * Synthetic workload
     */

    for (i = 0; i < 500000000; i++)
    {
        if (i % 3 == 0)
        {
            y += 1;
        }
    }

    printf("---------------------------------------- \n");
    printf("----------Profiling Results------------- \n");
    printf("---------------------------------------- \n");

    // Read the counter
    end_values[0] = 0;
    rc = read(fd[0], &end_values[0], sizeof(begin_values[0]));
    printf("End Count is %lld \n", end_values[0]);
    print_bytes_in_long_long(end_values[0]);


    rc = read(fd[0], &count_and_uncertainty, sizeof(struct tinin_read_back));

    printf("Read count: %lld, with uncertainy: %d \n", count_and_uncertainty.count, count_and_uncertainty.uncertainty);
    

    // printf("End Count is 0x%x%x%x%x%x%x%x%x \n", *(&end_values[0]), *(&end_values[0]+1), *(&end_values[0]+2),
	// 			*(&end_values[0]+3), *(&end_values[0]+4), *(&end_values[0]+5), *(&end_values[0]+6), *(&end_values[0]+7));

    asm volatile("nop;"); // pseudo-barrier

    // Close the counter
    close(fd[0]);

    // Print part of the information
    printf("Cache misses:           %lld \n", end_values[0] - begin_values[0]);
    printf("Y is : %lu", y);
    printf("\n");

    return 0;
}
