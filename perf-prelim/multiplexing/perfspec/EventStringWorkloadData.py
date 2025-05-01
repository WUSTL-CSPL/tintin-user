# EventStringWorkloadData class definition
#
class EventStringWorkloadData:
    def __init__(self, _eventstring, _workload):
        self.eventstring = _eventstring
        self.workload = _workload
        self.DataPoint_arr = [] # array of DataPoints