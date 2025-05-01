# EventDataPoint class definition
#
class EventDataPoint:
    def __init__(self, _event, _unit):
        self.event = _event
        self.unit = _unit
        self.counts = {} # dictionary of "timestamp: delta" key: value pairs

    def getCounts(self):
        return self.counts
    
    def getTotal(self):
        return sum(self.counts.values())

    def __str__(self):
        return f"\n{self.event}\n{self.unit}\n{self.counts}"