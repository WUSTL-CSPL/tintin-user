#include "tintin-utils.h"
#include <stdio.h>

extern tintin_event_group event_group;

extern "C" void tintin_start() {
    tintin_first_layer_events_init(&event_group, TINTIN_MODE_NATIVE);
    tintin_read_group_begin(&event_group);
}

extern "C" void tintin_end() {
    tintin_read_group_end(&event_group);
    long long slots = tintin_get_delta(&event_group, 0);
    long long backend = tintin_get_delta(&event_group, 1);
    long long bad_speculation = tintin_get_delta(&event_group, 2);
    long long frontend = tintin_get_delta(&event_group, 3);
    long long retired_instructions = tintin_get_delta(&event_group, 4);

    double backend_percentage = 100.0 * backend / (slots ? slots : 1);
    double bad_speculation_percentage = 100.0 * bad_speculation / (slots ? slots : 1);
    double frontend_percentage = 100.0 * frontend / (slots ? slots : 1);
    double retiring_percentage = 100.0 * retired_instructions / (slots ? slots : 1);
    // There is not backend event in our target CPU
    backend_percentage = 100.0 - bad_speculation_percentage - frontend_percentage - retiring_percentage;
    // Print results
    printf("-----------------------------------------------------------------\n");
    printf("%-20s %-20s %20s\n", "-", "Metrics",  "\%Slots");
    printf("%-20s %-35s %.4f%%\n", "S1", "Backend_Bound", backend_percentage);
    printf("%-20s %-35s %.4f%%\n", "S1", "Bad Speculation", bad_speculation_percentage);
    printf("%-20s %-35s %.4f%%\n", "S1", "Frontend_Bound", frontend_percentage);
    printf("%-20s %-35s %.4f%%\n", "S1", "Retiring", retiring_percentage);
    // printf("Bad speculation percentage: %.4f%%\n", bad_speculation_percentage);
    // printf("Frontend percentage: %.4f%%\n", frontend_percentage);
    // printf("Retiring percentage: %.4f%%\n", retiring_percentage);
}