import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np

# Set the font family to Helvetica and the weight to Light
plt.rcParams['font.family'] = 'Liberation Sans'
plt.rcParams['font.weight'] = 'light'


# Regular expression to match events
event_regex = re.compile(r"(\d+\.\d+): .* (L1-dcache-load-misses|bus-cycles)")
# event_regex = re.compile(r"(\d+\.\d+): .* (LLC-load-misses|instructions|dTLB-load-misses|topdown-fetch-bubbles|branch-misses|bus-cycles|L1-dcache-load-misses|L1-icache-load-misses)")


# Accumulate events over time intervals (1 ms)
interval = 0.01
event_counts = defaultdict(lambda: defaultdict(int))


start_timestamp = 0

# Parse the perf output
with open("cpu2017_541_perf_output.txt") as f:
    for line in f:
        match = event_regex.search(line)
        if match:
            timestamp = float(match.group(1))

            if start_timestamp == 0:
                start_timestamp = timestamp
            
            timestamp = timestamp - start_timestamp

            if timestamp < 135 or timestamp > 136:
                continue

            event = match.group(2)
            time_bucket = int(timestamp // interval) * interval
            event_counts[time_bucket][event] += 1

# Separate the data for plotting
timestamps = sorted(event_counts.keys())


llc_load_misses = [event_counts[t]["L1-dcache-load-misses"] for t in timestamps]
# branch_misses = [event_counts[t]["branch-misses"] for t in timestamps]
# l1_icache_load_misses = [event_counts[t]["L1-icache-load-misses"] for t in timestamps]
# l1_dcache_load_misses = [event_counts[t]["L1-dcache-load-misses"] for t in timestamps]
bus_cycles = [event_counts[t]["bus-cycles"] for t in timestamps]


timestamps = [t - 135 for t in timestamps]

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(5, 2.2))


ax.set_xlabel("Time (s)")
ax.plot(timestamps, bus_cycles, label="bus-cycles", linestyle="--", color="#545775", linewidth=2)
# axes[1].scatter(timestamps, branch_misses, label="branch-misses")

ax.set_xlabel("Time (s)")
ax.plot(timestamps, llc_load_misses, label="L1-dcache-load-misses", linestyle="-", color="#243E36")
# axes[0].scatter(timestamps, llc_load_misses, label="LLC-load-misses")


ax.grid()

ax.axvspan(0.29, 0.35, color='grey', alpha=0.3, label='workload change')


# ax.axvline(x=0.295, color='grey', linestyle='-', linewidth=2)
# ax.axvline(x=0.355, color='grey', linestyle='-', linewidth=2)

xticks = [0.0, 0.2, 0.5, 0.8, 1.0]  # Ticks from 0 to 10 at intervals of 1
xticks = np.append(xticks, 0.29)
xticks = np.append(xticks, 0.35)
xticks = np.sort(xticks)  # Sort the ticks

ax.set_xticklabels(["{:.2f}".format(t) for t in xticks])  # Format tick labels with two decimal places

ax.set_xticks(xticks)

# Rotate x-tick labels by 45 degrees using plt.setp()
plt.setp(ax.get_xticklabels(), rotation=30)

ax.legend(loc="lower right")
ax.set_ylabel("Event Count")

plt.tight_layout()
plt.savefig("count-changes.pdf", format="pdf")
plt.show()