from enum import Enum
from dataclasses import dataclass
from collections import OrderedDict

class WorkloadType(Enum):
    L100 = 0 # 100% Local DRAM Memory
    L0 = 1 # 0% Local DRAM Memory, 100% CXL Simulated Memory

class ReadingType(Enum):
    Tintin = 0
    EMON = 1

@dataclass 
class CountReading:
    type: ReadingType
    count: int
    uncertainty: int #unused if type is EMON

@dataclass
class WorkloadRun:
    type: WorkloadType
    time: float
    counts: OrderedDict[str, list[CountReading]]

@dataclass 
class Workload:
    name: str
    runs: dict[WorkloadType, WorkloadRun]

def calculate_slowdown(baseWorkload: WorkloadRun, workload: WorkloadRun):
    return (workload.time - baseWorkload.time) / baseWorkload.time