from collections import OrderedDict
from pathlib import Path
from workload import CountReading, ReadingType

def _process_emon_line(line: str, cpu_index: int) -> CountReading:
    '''
    Emon lines have the format: <metric> <identifier> <time> <cpu0> <cpu1> ...
    '''
    count = int(line.split()[cpu_index + 3].replace(",",""))
    return CountReading(ReadingType.EMON, count, 0)

def _process_tintin_line(line: str) -> CountReading:
    '''
    Tintin lines have the format: <metric> <count> <uncertainty>
    '''
    line_split = line.split()
    return CountReading(ReadingType.Tintin, int(line_split[1]), int(line_split[2]))

def _parse_counts(filepath: Path, metrics: set[str], line_parse_func: callable) -> OrderedDict[str, list[CountReading]]:
    if not filepath.exists():
        raise RuntimeError(f"File {filepath} does not exist")

    metric_data: dict[str, list[CountReading]] = {metric:[] for metric in metrics}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            for metric in metrics:
                if line.startswith(metric):
                    metric_data[metric].append(line_parse_func(line))
                    break

    return OrderedDict(sorted(metric_data.items()))

def parse_emon_counts(filepath: Path, metrics: set[str], cpu_index: int = 0) -> OrderedDict[str, list[CountReading]]:
    return _parse_counts(filepath, metrics, lambda line: _process_emon_line(line, cpu_index))

def parse_tintin_counts(filepath: Path, metrics: set[str])-> OrderedDict[str, list[CountReading]]:
    return _parse_counts(filepath, metrics, _process_tintin_line)

def parse_time_file(filepath: Path) -> float:
    '''
    Time files have the format:
   
    ...
    Real: <real time in seconds> <real time in hh:mm:ss>
    ...
   
    '''
    with open(filepath) as f:
        last_real_time = float("nan")
        for line in f:
            line = line.strip()
            if line.startswith("Real"):
                last_real_time = float(line.split()[1])
        if last_real_time == float("nan"):
            raise RuntimeError(f"Could not find real time component in file {filepath}")
        return last_real_time