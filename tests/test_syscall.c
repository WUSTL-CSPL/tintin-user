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

// tintin monitor syscall
int tintin_syscall(pid_t pid)
{
	// printf("The syscall number is %d", __NR_tintin_event_open);
    	return syscall(552, pid);
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

    int cid;
    cid = tintin_syscall(getpid());
    
    printf("The profiling context id is : %d", cid);
    printf("\n");

    return 0;
}
