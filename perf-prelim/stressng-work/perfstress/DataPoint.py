# DataPoint class definition
#
class DataPoint:
    def __init__(self, _event, _eventstring, _workload):
        self.event = _event
        self.eventstring = _eventstring
        self.workload = _workload
        self.unit = "Counts"
        self.counts = [] # list of counts, each element at index i is the count from the ith trial
        self.stats = {} # dictionary with calculated statistical metrics

    def __str__(self):
        return f"\n{self.eventstring}\n{self.workload}\n{self.event}\n{self.counts}\n{self.unit}"