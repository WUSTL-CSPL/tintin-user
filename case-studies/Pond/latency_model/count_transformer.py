from collections import OrderedDict
from workload import Workload, WorkloadRun, CountReading


def cumulative_data_to_individual(workload: Workload) -> Workload:
    new_runs = dict()
    for workload_type, run in workload.runs.items():
        new_runs[workload_type] = WorkloadRun(workload_type, run.time, __cumulative_data_to_individual(run.counts))
    return Workload(workload.name, new_runs)


def individual_data_to_cumulative(workload: Workload) -> Workload:
    new_runs = dict()
    for workload_type, run in workload.runs.items():
        new_runs[workload_type] = WorkloadRun(workload_type, run.time, __individual_data_to_cumulative(run.counts))
    return Workload(workload.name, new_runs)


def __cumulative_data_to_individual(metrics: OrderedDict[str, list[CountReading]]) -> OrderedDict[str, list[CountReading]]:
    new_metrics = OrderedDict()
    for metric, count_readings in metrics.items():
        readings = []
        for i, reading in enumerate(count_readings):
            if i == 0:
                new_count = reading.count
                new_uncertainty = reading.uncertainty
            else:
                new_count = reading.count - count_readings[i-1].count
                new_uncertainty = reading.uncertainty - count_readings[i-1].uncertainty

            readings.append(CountReading(reading.type, new_count, new_uncertainty))
        new_metrics[metric] = readings
    return new_metrics


def __individual_data_to_cumulative(metrics: OrderedDict[str, list[CountReading]]) -> OrderedDict[str, list[CountReading]]:
    new_metrics = OrderedDict()
    for metric, count_readings in metrics.items():
        readings = []
        for i, reading in enumerate(count_readings):
            if i == 0:
                new_count = reading.count
                new_uncertainty = reading.uncertainty
            else:
                new_count = reading.count + readings[-1].count
                new_uncertainty = reading.uncertainty + readings[-1].uncertainty

            readings.append(CountReading(reading.type, new_count, new_uncertainty))
        new_metrics[metric] = readings
    return new_metrics
