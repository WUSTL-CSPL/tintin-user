#define TINTIN_PERF_IMPLEMENTATION
#include "tintin-utils.h"
#include <stdio.h>

void workload() {
    // Simulate some work
    volatile int sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += i;
    }
}

int main() {
    tintin_event_group event_group;
    
    // Initialize with Tintin mode
    // if (tintin_predefined_events_init(&event_group, TINTIN_MODE_NATIVE) == -1) {
    if (tintin_predefined_events_init(&event_group, TINTIN_MODE_TINTIN) == -1) {
        fprintf(stderr, "Failed to initialize performance monitoring\n");
        return 1;
    }
    
    // Start monitoring
    if (tintin_read_group_begin(&event_group) == -1) {
        fprintf(stderr, "Failed to start performance monitoring\n");
        tintin_group_cleanup(&event_group);
        return 1;
    }
    
    // Run workload
    workload();
     
    // Stop monitoring
    if (tintin_read_group_end(&event_group) == -1) {
        fprintf(stderr, "Failed to stop performance monitoring\n");
    }
    
    // Print results
    printf("Performance counters:\n");
    printf("CPU cycles: %lu\n", tintin_get_delta(&event_group, 0));
    printf("Instructions: %lu\n", tintin_get_delta(&event_group, 1));
    printf("Cache references: %lu\n", tintin_get_delta(&event_group, 2));
    printf("Cache misses: %lu\n", tintin_get_delta(&event_group, 3));
    
    // Clean up
    tintin_group_cleanup(&event_group);
    
    return 0;
}