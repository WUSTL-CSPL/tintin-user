# statcalc.py
# Lien Zhu
# Data processing for perfstress.py


import numpy as np

from EventDataPoint import *


TIME_INDEX = 0
COUNT_INDEX = 1
UNIT_INDEX = 2
EVENT_INDEX = 3


# Parses event counts from data file
#
def parse_counts_from_file(data_file):

    data_point = []
    data_point_arr = []

    with open(data_file, 'r') as f:
        for line in f:
            if line[0] == "#" or not line.strip() or "<not counted>" in line:
                continue

            data_point = line.split(',')
            data_point = data_point[0:EVENT_INDEX + 1]
            data_point[UNIT_INDEX] = "counts" if data_point[UNIT_INDEX] == '' else data_point[UNIT_INDEX]
            data_point[COUNT_INDEX] = int( data_point[COUNT_INDEX] )
            data_point_arr.append(data_point)
    
    data_point_arr.sort(key = lambda x : x[EVENT_INDEX])

    # the early signs of life in OOP refactor
    event_data_point_arr = makeEventDataPoints(data_point_arr)
    # print(event_data_point_arr[0])
    print(event_data_point_arr[0].getTotal())

    return data_point_arr


# Creates objects of EventDataPoint's
#
def makeEventDataPoints(data_point_arr):
    event_data_point_arr = []

    num_of_points = len(data_point_arr)
    scheduled_events = set()
    for data_point in data_point_arr:
        scheduled_events.add(data_point[EVENT_INDEX])

    num_scheduled_events = len(scheduled_events)
    num_of_intervals = num_of_points / num_scheduled_events # first figure out how many intervals fit into the scheduled time
    currEventDataPoint = EventDataPoint(None, None)
    for individual_event_index, data_point in enumerate(data_point_arr):
        if individual_event_index % num_of_intervals == 0: # the first delta of each event
            currEventDataPoint.event = data_point[EVENT_INDEX]
            currEventDataPoint.unit = data_point[UNIT_INDEX]

        currEventDataPoint.counts[data_point[TIME_INDEX]] = data_point[COUNT_INDEX] # add to dictionary

        if individual_event_index % num_of_intervals == num_of_intervals - 1: # the last delta of each event
            event_data_point_arr.append(currEventDataPoint)
            currEventDataPoint = EventDataPoint(None, None)

    return event_data_point_arr