/* 
 * tintin_perf.h - Single-header performance monitoring library
 * Usage: #define TINTIN_PERF_IMPLEMENTATION in one source file before including
 */

#ifndef TINTIN_PERF_H
#define TINTIN_PERF_H

#include <stdint.h>
#include <linux/perf_event.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>

#ifdef __cplusplus
extern "C" {
#endif

#define TINTIN_MAX_EVENTS 600

// Library initialization modes
#define TINTIN_MODE_NATIVE 0    // Use native Linux perf events
#define TINTIN_MODE_TINTIN 1    // Use Tintin-specific extensions

typedef struct {
    struct perf_event_attr attr[TINTIN_MAX_EVENTS];
    int fd[TINTIN_MAX_EVENTS];
    uint64_t begin_values[TINTIN_MAX_EVENTS];
    uint64_t end_values[TINTIN_MAX_EVENTS];
    int event_count;
    int mode;
} tintin_event_group;

void tintin_begin();
void tintin_end();

// Function prototypes
int tintin_predefined_events_init(tintin_event_group *group, int mode);

int tintin_read_group_begin(tintin_event_group *group);
int tintin_read_group_end(tintin_event_group *group);
int tintin_perf_stop(tintin_event_group *group);
void tintin_perf_cleanup(tintin_event_group *group);

uint64_t tintin_get_delta(tintin_event_group *group, int event_index);
void tintin_perf_enable_scalability(tintin_event_group *group);
int tintin_event_init(int event_type, int event_code, int event_umask);
int tintin_first_layer_events_init(tintin_event_group *group, int mode);

#ifdef __cplusplus
}
#endif

#endif /* TINTIN_PERF_H */


#ifdef TINTIN_PERF_IMPLEMENTATION

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>



// Internal perf counter syscall wrapper
static inline int tintin_event_open(struct perf_event_attr *hw,
            pid_t pid, int cpu, int grp, unsigned long flags, int mode)
{ 
    if (mode == TINTIN_MODE_NATIVE) {
        return syscall(__NR_perf_event_open, hw, pid, cpu, grp, flags);
    } else { // TINTIN_MODE_TINTIN
        return syscall(548, hw, pid, cpu, grp, flags);
    }
}


int tintin_predefined_events_init(tintin_event_group *group, int mode) {

    int ret = 0;

    if (!group) return -1;
    
    memset(group, 0, sizeof(tintin_event_group));
    group->mode = mode;
    
    unsigned int event_index;
    int ii;

    // Initialize hardware events (10 events)
    event_index = 0;
    for (ii = 0; ii < 10; ii++) {
        group->attr[ii].type = PERF_TYPE_HARDWARE;
        group->attr[ii].config = event_index;
        group->attr[ii].disabled = 0;
        group->fd[ii] = tintin_event_open(&group->attr[ii], getpid(), -1, -1, 0, mode);
        if (group->fd[ii] < 0) {
            fprintf(stderr, "[Tintin-user] Debugging: Opening the %uth hardware event failed\n", ii);
            ret++;
        }
        event_index++;
    }

    // Initialize cache events (6 events)
    event_index = 0;
    for (ii = 10; ii < 16; ii++) {
        group->attr[ii].type = PERF_TYPE_HW_CACHE;
        group->attr[ii].config = event_index;
        group->attr[ii].disabled = 0;
        group->fd[ii] = tintin_event_open(&group->attr[ii], getpid(), -1, -1, 0, mode);
        if (group->fd[ii] < 0) {
            // fprintf(stderr, "[Tintin-user] Debugging: Opening the %uth cache event failed\n", ii);
            ret++;
        }
        event_index++;
    }

    // Initialize RAM events (2 events)
    event_index = 0;
    for (ii = 16; ii < 18; ii++) {
        group->attr[ii].type = PERF_TYPE_RAW;
        group->attr[ii].config = event_index;
        group->attr[ii].disabled = 0;
        group->fd[ii] = tintin_event_open(&group->attr[ii], getpid(), -1, -1, 0, mode);
        if (group->fd[ii] < 0) {
            fprintf(stderr, "[Tintin-user] Debugging: Opening the %uth RAM event failed\n", ii);
            ret++;
        }
        event_index++;
    }

    // Initialize additional hardware events (4 events)
    event_index = 0;
    for (ii = 18; ii < 22; ii++) {
        group->attr[ii].type = PERF_TYPE_HARDWARE;
        group->attr[ii].config = event_index;
        group->attr[ii].disabled = 0;
        group->fd[ii] = tintin_event_open(&group->attr[ii], getpid(), -1, -1, 0, mode);
        if (group->fd[ii] < 0) {
            fprintf(stderr, "[Tintin-user] Debugging: Opening the %uth additional hardware event failed\n", ii);
            ret++;
        }
        event_index++;
    }

    // Configure pinned event (cache misses)
    if (mode == TINTIN_MODE_NATIVE) {
        group->attr[3].pinned = 1;
        close(group->fd[7]);
        group->fd[7] = tintin_event_open(&group->attr[3], 0, -1, -1, 0, mode);
    } else { // TINTIN_MODE_TINTIN
        close(group->fd[7]);
        group->fd[7] = tintin_event_open(&group->attr[3], 0, -1, -1, 0, mode);
        write(group->fd[7], "pin", strlen("pin"));
    }

    group->event_count = 22;
    return ret;
}

void tintin_perf_enable_scalability(tintin_event_group *group) {
    if (!group) return;
    
    for (int j = 23; j < 500; j++) {
        group->fd[j] = tintin_event_open(&group->attr[3], 0, -1, -1, 0, group->mode);
    }
    group->event_count = 500;
}

int tintin_read_group_begin(tintin_event_group *group) {
    if (!group) return -1;
    
    int ret = 0;

    int rc;
    for (int ii = 0; ii < group->event_count; ii++) {
        if (group->fd[ii] >= 0) {
            rc = read(group->fd[ii], &group->begin_values[ii], sizeof(group->begin_values[ii]));
            if (!rc) ret++;
        }
    }
    return 0;
}

int tintin_read_group_end(tintin_event_group *group) {
    if (!group) return -1;
    
    int ret = 0;

    int rc;
    for (int ii = 0; ii < group->event_count; ii++) {
        if (group->fd[ii] >= 0) {
            rc = read(group->fd[ii], &group->end_values[ii], sizeof(group->end_values[ii]));
            // printf("[Tintin-user] Debugging: the value is %lu \n", group->end_values[ii]);
            if (!rc) ret++;
        }
    }
    return 0;
}

uint64_t tintin_get_delta(tintin_event_group *group, int event_index) {
    if (!group || event_index < 0 || event_index >= group->event_count) {
        return 0;
    }
    return group->end_values[event_index] - group->begin_values[event_index];
}

void tintin_group_cleanup(tintin_event_group *group) {
    if (!group) return;
    
    for (int ii = 0; ii < group->event_count; ii++) {
        if (group->fd[ii] >= 0) {
            close(group->fd[ii]);
        }
    }
}

////////////////////////// For DMon

int tintin_first_layer_events_init(tintin_event_group *group, int mode) {
    // Event code reference: https://perfmon-events.intel.com/
    // For the derived metrics, refer to the Intel Topdown paper: https://ieeexplore.ieee.org/document/6844459
    // https://perfmon-events.intel.com/
    // Under the section Alder Lake and Raptor Lake Hybrid Events
    int ret = 0;

    memset(group, 0, sizeof(tintin_event_group));
    group->mode = mode;

    // This is the first opened because it can only be measured at counter 0
    // 2. Topdown Bad Speculation
    int bad_speculation_event_code = 0xC5;
    int bad_speculation_event_umask = 0x01;
    group->attr[2].type = PERF_TYPE_RAW;
    group->attr[2].size = sizeof(struct perf_event_attr);
    group->attr[2].config = bad_speculation_event_code | (bad_speculation_event_umask << 8);
    group->attr[2].disabled = 1;
    group->attr[2].exclude_kernel = 1;  // User-mode events only
    group->attr[2].exclude_hv = 1;      // Don't count hypervisor events
    group->fd[2] = tintin_event_open(&group->attr[2], getpid(), -1, -1, 0, mode);
    if (group->fd[2] < 0) {
        fprintf(stderr, "[Tintin-user] Debugging: Opening the hardware event failed\n");
        ret++;
    }
    ioctl(group->fd[2], PERF_EVENT_IOC_RESET, 0);
    ioctl(group->fd[2], PERF_EVENT_IOC_ENABLE, 0);


    // 0. Topdown slots = Unhalted Core Cycles    
    int cycles_event_code = 0x3C;
    int cycles_event_umask = 0x00;
    group->attr[0].type = PERF_TYPE_RAW;
    group->attr[0].size = sizeof(struct perf_event_attr);
    group->attr[0].config = cycles_event_code | (cycles_event_umask << 8);
    group->attr[0].disabled = 1;
    group->attr[0].exclude_kernel = 1;  // User-mode events only
    group->attr[0].exclude_hv = 1;      // Don't count hypervisor events
    group->fd[0] = tintin_event_open(&group->attr[0], getpid(), -1, -1, 0, mode);
    if (group->fd[0] < 0) {
        fprintf(stderr, "[Tintin-user] Debugging: Opening the hardware event failed\n");
        ret++;
    }
    ioctl(group->fd[0], PERF_EVENT_IOC_RESET, 0);
    ioctl(group->fd[0], PERF_EVENT_IOC_ENABLE, 0);


    // 1. Topdown Backend Bound
    int backend_event_code = 0xA3;
    int backend_event_umask = 0x04;

    group->attr[1].type = PERF_TYPE_RAW;
    group->attr[1].size = sizeof(struct perf_event_attr);
    group->attr[1].config = backend_event_code | (backend_event_umask << 8);
    group->attr[1].disabled = 1;
    group->attr[1].exclude_kernel = 1;  // User-mode events only
    group->attr[1].exclude_hv = 1;      // Don't count hypervisor events
    group->fd[1] = tintin_event_open(&group->attr[1], getpid(), -1, -1, 0, mode);
    if (group->fd[1] < 0) {
        fprintf(stderr, "[Tintin-user] Debugging: Opening the hardware event failed\n");
        ret++;
    }
    // Enable the counter
    ioctl(group->fd[1], PERF_EVENT_IOC_RESET, 0);
    ioctl(group->fd[1], PERF_EVENT_IOC_ENABLE, 0);


    // IDQ_UOPS_NOT_DELIVERED.CORE
    // 3. Topdown Frontend Bound
    int front_event_code = 0xC6;
    int front_event_umask = 0x01;
    group->attr[3].type = PERF_TYPE_RAW;
    group->attr[3].size = sizeof(struct perf_event_attr);
    group->attr[3].config = front_event_code | (front_event_umask << 8);
    group->attr[3].disabled = 1;
    group->attr[3].exclude_kernel = 1;  // User-mode events only
    group->attr[3].exclude_hv = 1;      // Don't count hypervisor events
    group->fd[3] = tintin_event_open(&group->attr[3], getpid(), -1, -1, 0, mode);
    if (group->fd[3] < 0) {
        fprintf(stderr, "[Tintin-user] Debugging: Opening the hardware event failed\n");
        ret++;
    }
    ioctl(group->fd[3], PERF_EVENT_IOC_RESET, 0);
    ioctl(group->fd[3], PERF_EVENT_IOC_ENABLE, 0);


    // 4. Topdown Retiring
    int retiring_event_code = 0xC0;
    int retiring_event_umask = 0x01;
    group->attr[4].type = PERF_TYPE_RAW;
    group->attr[4].size = sizeof(struct perf_event_attr);
    group->attr[4].config = retiring_event_code | (retiring_event_umask << 8);
    group->attr[4].disabled = 1;
    group->attr[4].exclude_kernel = 1;  // User-mode events only
    group->attr[4].exclude_hv = 1;      // Don't count hypervisor events
    group->fd[4] = tintin_event_open(&group->attr[4], getpid(), -1, -1, 0, mode);
    if (group->fd[4] < 0 || group->fd[1] < 0 || group->fd[2] < 0 || group->fd[3] < 0) {
        fprintf(stderr, "[Tintin-user] Debugging: Opening the hardware event failed\n");
        ret++;
    }
    ioctl(group->fd[4], PERF_EVENT_IOC_RESET, 0);
    ioctl(group->fd[4], PERF_EVENT_IOC_ENABLE, 0);


    group->event_count = 5;
    return ret;
}




#endif /* TINTIN_PERF_IMPLEMENTATION */