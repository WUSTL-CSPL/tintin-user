# grapher.py
# Lien Zhu
# Graphs results from perfstress.py

import os, sys
import subprocess
import numpy as np
import re           # for parsing data
import shutil       # rm -rf functionality
import csv
import datetime
import argparse
import itertools    # event combinations
import random


COUNT_INDEX = 1
EVENT_INDEX = 3


# Handles writing to csv
#
def write_to_csv(results_path, trial, num_of_simultaneous_events, results_arr, events, workloads):

    # set up csv file
    os.chdir(results_path)
    results_file_name = "results_" + str(trial) + ".csv"
    data_file = open(results_file_name, 'w')
    csv_writer = csv.writer(data_file)

    num_events_title = [str(num_of_simultaneous_events) + " Events Counted per Perf Invocation: "]
    columns_header = ["Interval Timestamp", "Count", "Unit", "Event"]

    csv_writer.writerow(num_events_title)
    csv_writer.writerow([])
    csv_writer.writerow([])
    csv_writer.writerow(columns_header)
    csv_writer.writerow([])
    csv_writer.writerow([])


    # write to csv
    for event_string_index, event_string_data_arr in enumerate(results_arr):

        event_string_title_row = [ events[event_string_index] ]
        csv_writer.writerow(event_string_title_row)
        csv_writer.writerow([])

        for workload_index, data_point_arr in enumerate(event_string_data_arr):
            workload_title_row = [ workloads[workload_index] ]
            csv_writer.writerow(workload_title_row)

            # things get complicated here because Tomson Li needs totals for each event
            num_of_points = len(data_point_arr)

            scheduled_events = set()
            for data_point in data_point_arr:
                scheduled_events.add(data_point[EVENT_INDEX])

            num_scheduled_events = len(scheduled_events)
            num_of_intervals = num_of_points / num_scheduled_events # first figure out how many intervals fit into the scheduled time
            event_total = 0

            for individual_event_index, data_point in enumerate(data_point_arr):
                if individual_event_index % num_of_intervals == num_of_intervals - 1: # we are on the last data_point of this event
                    # increment total
                    # write data_point
                    # print total
                    # reset total
                    event_total += data_point[COUNT_INDEX]
                    csv_writer.writerow(data_point)
                    csv_writer.writerow([str(event_total)])
                    csv_writer.writerow([])
                    event_total = 0
                else: 
                    event_total += data_point[COUNT_INDEX]
                    csv_writer.writerow(data_point)
            csv_writer.writerow([])

        csv_writer.writerow([])
        csv_writer.writerow([])

    data_file.close()