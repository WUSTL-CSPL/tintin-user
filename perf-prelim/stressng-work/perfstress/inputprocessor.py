# inputprocessor.py
# Lien Zhu
# Processes input into perfstress.py


import itertools    # event combinations


# Populates the arrays that contain all events and all workloads
#
def process_input(events_input_file, workloads_input_file):

    all_events = []
    all_workloads = [] # stress-ng workloads from input. Type [string]. Example item: "--matrix-ops 100"

    with open(events_input_file) as events_file:
        for line in events_file:
            all_events.append(line.strip())

    with open(workloads_input_file) as workloads_file:
        for line in workloads_file:
            all_workloads.append(line.strip())

    return all_events, all_workloads


# Processes the array that contains all events to count
# such that each element in the resulting array
# is a stringed combination of events to count
# to count together
#
def process_events_arr(all_events_arr, num_of_simultaneous_events):

    if num_of_simultaneous_events == 1:
        return all_events_arr

    events_combos_list = list( itertools.combinations(all_events_arr, num_of_simultaneous_events) )

    processed_events_arr = []
    for combo_tuple in events_combos_list:
        event_string = ""
        for index in range(num_of_simultaneous_events - 1):
            event_string += combo_tuple[index] + ","
        event_string += combo_tuple[num_of_simultaneous_events - 1]
        processed_events_arr.append(event_string)
    
    return processed_events_arr

# Simple process_events_arr that only takes the first event_string
def simple_process_events_arr(all_events_arr, num_of_simultaneous_events):

    events_combos_list = list( itertools.combinations(all_events_arr, num_of_simultaneous_events) )

    processed_events_arr = []
    combo = events_combos_list[0]
    event_string = ""
    for index in range(num_of_simultaneous_events - 1):
        event_string += combo[index] + ","
    event_string += combo[num_of_simultaneous_events - 1]
    processed_events_arr.append(event_string)
    
    return processed_events_arr