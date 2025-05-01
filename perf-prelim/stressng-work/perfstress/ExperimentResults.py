# ExperimentResults class definition
#
import datetime

class ExperimentResults:
    def __init__(self, 
                 _num_of_trials, 
                 _num_of_events_together, 
                 _events_input_file, 
                 _workloads_input_file, 
                 _event_strings, 
                 _workloads, 
                 _scheduler, _priority, _perfversion, _perfcore, _stressversion, _stresscore, _stresscpu):
        self.datetime = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        self.num_of_trials = _num_of_trials
        self.num_of_events_together = _num_of_events_together
        self.events_input_file = _events_input_file
        self.workloads_input_file = _workloads_input_file
        self.event_strings = _event_strings
        self.workloads = _workloads
        self.scheduler = _scheduler
        self.priority = _priority
        self.perfversion = _perfversion
        self.perfcore = _perfcore
        self.stressversion = _stressversion
        self.stresscore = _stresscore
        self.stresscpu = _stresscpu
        self.EventStringData_arr = [] 