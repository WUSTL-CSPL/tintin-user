import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Regular expression to match events
# event_regex = re.compile(r"(\d+\.\d+): .* (L1-icache-load-misses|L1-dcache-load-misses|bus-cycles)")
event_regex = re.compile(r"(\d+\.\d+): .* (LLC-load-misses|instructions|dTLB-load-misses|topdown-fetch-bubbles|branch-misses|bus-cycles|L1-dcache-load-misses|L1-icache-load-misses)")


# Accumulate events over time intervals (1 ms)
interval = 0.001
all_event_counts = defaultdict(list)
all_event_timestamps = defaultdict(list)

# Parse the perf output
pattern = re.compile(r"(\d+\.\d+):\s+(\d+)\s+(\S+)")
with open("cpu2017_541_perf_output.txt") as f:
    for line in f:
        items = line.split()

        timestamp = float(items[2].replace(":", ""))
        event_name = items[4]
        event_count = int(items[3])

        # print(timestamp, event_name, event_count)

        if not event_name in all_event_counts:
            all_event_counts[event_name] = []
            all_event_timestamps[event_name] = []
        
        all_event_counts[event_name].append(event_count)
        all_event_timestamps[event_name].append(timestamp)

# Plotting
fig, axes = plt.subplots(3, 1, figsize=(4, 2.2))


i = 0
for event_name, event_counts in all_event_counts.items():

    # print(event_name)
    # print(len(event_counts))
    timestamps = all_event_timestamps[event_name]
    axes[i].bar(timestamps, event_counts, width=interval, label=event_name)
    # axes[i].scatter(timestamps, event_counts, label=event_name)
    axes[i].legend()
    axes[i].grid()

    i = i + 1

axes[i-1].set_xlabel("Time (s)")
axes[i-1].set_ylabel("Event Count")


plt.tight_layout()

plt.show()