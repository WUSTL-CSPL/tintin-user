# statcalc.py
# Lien Zhu
# This file contains functions for calculating results
# and writing results to csv


import csv
import os

from ExperimentResults import *
from EventStringData import *
from EventStringWorkloadData import *
from DataPoint import *

COUNT_INDEX = 0
UNIT_INDEX = 1
EVENT_INDEX = 2


### Data Processing ###

# Parses event counts from datafile
#
def parse_counts_from_file(datafile, string_workload_obj):

    datapoint_arr_index = 0
    with open(datafile, 'r') as f:
        for line in f:
            if line[0] == "#" or not line.strip() or "<not counted>" in line:
                continue

            line_of_data = line.split(',')
            curr_datapoint = string_workload_obj.DataPoint_arr[datapoint_arr_index]

            _count = int( line_of_data[COUNT_INDEX].replace(',', '') )
            curr_datapoint.counts.append(_count)
            curr_datapoint.eventstring = string_workload_obj.eventstring
            curr_datapoint.workload = string_workload_obj.workload
            curr_datapoint.unit = line_of_data[UNIT_INDEX] if line_of_data[UNIT_INDEX] != "" else "Counts"
            curr_datapoint.event = line_of_data[EVENT_INDEX]

            datapoint_arr_index += 1


# Calculates statistics from experiment_obj passed to it
#
def calc_stats(experiment_obj):
    pass

# Handles writing to csv
# TODO: Refactor
def write_results_to_csv(experiment_obj, experiment_path):

    # set up csv file
    os.chdir(experiment_path)
    with open('results.csv', 'w') as datafile:
        csv_writer = csv.writer(datafile)

        num_events_title = [str(experiment_obj.num_of_events_together) + " Events Counted per Perf Invocation: "]
        num_trials_title = ["Each Perf Invocation was repeated " + str(experiment_obj.num_of_trials) + " times"]

        csv_writer.writerow(num_events_title)
        csv_writer.writerow(num_trials_title)
        csv_writer.writerow([])

        # write data to csv
        for event_string_index, event_string_obj in enumerate(experiment_obj.EventStringData_arr):
            event_string_title_row = [ experiment_obj.event_strings[event_string_index] ]
            csv_writer.writerow(event_string_title_row)
            csv_writer.writerow([])

            for workload_index, event_string_workload_obj in enumerate(event_string_obj.EventStringWorkloadData_arr):
                workload_title_row = [ experiment_obj.workloads[workload_index] ]
                csv_writer.writerow(workload_title_row)

                for data_point in event_string_workload_obj.DataPoint_arr:
                    datapoint_row = [data_point.event] + data_point.counts
                    csv_writer.writerow(datapoint_row)
                csv_writer.writerow([])
            
            csv_writer.writerow([])