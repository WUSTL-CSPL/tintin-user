
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import statistics
import matplotlib as mpl

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Optional: Specify a particular sans-serif font (e.g., Arial, Helvetica)
mpl.rcParams['font.sans-serif'] = ['Arial']

# Here are the benchmark workload names and their index
workloads = ['perlbench',     # -> 0
              'gcc',          # -> 1
              'mcf',          # -> 2
              'omnetpp',      # -> 3
              'xalancbmk',    # -> 4
              'x264(spec)',   # -> 5
              'deepsjeng',    # -> 6
              'leea',         # -> 7
              'xz',           # -> 8
              'cactuBSSN',    # -> 9
              'namd',         # -> 10
              'parest',       # -> 11
              'lbm',          # -> 12
              'imagick',      # -> 13
              'nab',          # -> 14
              'blackscholes', # -> 15 
              'bodytrack',    # -> 16
              'canneal',      # -> 17
              'ferret',       # -> 18
              'fluidanimate', # -> 19 
              'freqmine',     # -> 20
              'raytrace',     # -> 21
              'streamcluster',# -> 22 
              'swaptions',    # -> 23
              'vips',         # -> 24
              'x264(parsec)'] # -> 25


# @HI Replace All data are here!

##############
# Baseline   #
##############

exe_times_baseline =   [84.733342,   #  -> 0
                        64.419429,   # -> 1
                        368.526103,  # -> 2
                        403.737736,  # -> 3
                        243.038356,  # -> 4
                        175.929024,  # -> 5
                        316.262665,  # -> 6
                        507.713611,  # -> 7
                        108.637528,  # -> 8
                        266.368621,  # -> 9
                        200.897312,  # -> 10
                        539.091527,  # -> 11
                        274.654964,  # -> 12
                        511.271863,  # -> 13
                        422.097304,  # -> 14
                        65.092048,   # -> 15
                        110.037504,  # -> 16
                        156.603743,  # -> 17
                        331.288149,  # -> 18
                        250.214206,  # -> 19
                        358.193269,  # -> 20
                        131.034891,  # -> 21
                        484.665229,  # -> 22
                        175.555478,  # -> 23
                        70.550779,   # -> 24
                        64.407513]   # -> 25

##############
# Linux Perf #
##############

exe_times_linux_perf = [85.291441,   # -> 0
                        66.676171,   # -> 1
                        371.111413,  # -> 2
                        408.171619,  # -> 3
                        244.340488,  # -> 4
                        177.418268,  # -> 5
                        325.985507,  # -> 6
                        518.57891,   # -> 7
                        108.815071,  # -> 8
                        269.273384,  # -> 9
                        203.808631,  # -> 10
                        543.411555,  # -> 11
                        276.535432,  # -> 12
                        519.43096,   # -> 13
                        424.430555,  # -> 14
                        65.784942,   # -> 15
                        113.089892,  # -> 16
                        162.97573,   # -> 17
                        332.588045,  # -> 18
                        256.831802,  # -> 19
                        368.018677,  # -> 20
                        134.225191,  # -> 21
                        484.145748,  # -> 22
                        175.951036,  # -> 23
                        79.520812,   # -> 24
                        65.417167]   # -> 25


#############
# BayesPerf #
#############
exe_times_bayes =      [101.718115,   # -> 0
                        77.429137,    # -> 1
                        452.47867,    # -> 2
                        486.450736,   # -> 3
                        283.363501,   # -> 4
                        205.484054,   # -> 5
                        380.930145,   # -> 6
                        610.723389,   # -> 7
                        128.04117,    # -> 8
                        306.894622,   # -> 9
                        233.09086,    # -> 10
                        610.821464,   # -> 11
                        310.348025,   # -> 12
                        648.954575,   # -> 13
                        500.537292,   # -> 14
                        70.732541,    # -> 15
                        128.027179,   # -> 16
                        205.667009,   # -> 17
                        374.907358,   # -> 18
                        267.339589,   # -> 19
                        442.475616,   # -> 20
                        167.108779,   # -> 21
                        512.448623,   # -> 22
                        222.652749,   # -> 23
                        76.108621,    # -> 24
                        76.817941]    # -> 25

##########
# Tintin #
##########
exe_times_tintin =     [85.480826,   # -> 0
                        67.164979,   # -> 1
                        382.30594,   # -> 2
                        413.09489,   # -> 3
                        245.191778,  # -> 4
                        177.444524,  # -> 5
                        326.098503,  # -> 6
                        517.946813,  # -> 7
                        111.178457,  # -> 8
                        269.071862,  # -> 9
                        203.589311,  # -> 10
                        550.735998,  # -> 11
                        278.025876,  # -> 12
                        536.575863,  # -> 13
                        430.139169,  # -> 14
                        65.999759,   # -> 15
                        118.360124,  # -> 16
                        165.101302,  # -> 17
                        333.032462,  # -> 18
                        252.846588,  # -> 19
                        364.887812,  # -> 20
                        137.184976,  # -> 21
                        487.644592,  # -> 22
                        178.269494,  # -> 23
                        73.102689,   # -> 24
                        65.20504]    # -> 25

### Calculate the overhead
overhead_original = [1] * 26
overhead_original = [x * 100.0 for x in overhead_original]
overhead_linux_perf = [exe_times_linux_perf[i] / exe_times_baseline[i] for i in range(len(exe_times_baseline))]
overhead_linux_perf = [x * 100.0 for x in overhead_linux_perf]
overhead_bayes = [exe_times_bayes[i] / exe_times_baseline[i] for i in range(len(exe_times_baseline))]
overhead_bayes = [x * 100.0 for x in overhead_bayes]
overhead_tintin = [exe_times_tintin[i] / exe_times_baseline[i] for i in range(len(exe_times_baseline))]
overhead_tintin = [x * 100.0 for x in overhead_tintin]

                           
### End of loading data

#### Overover overhead

print("Overhead of Linux Perf: ")
print("Average: ", statistics.mean(overhead_linux_perf))
print("Max: ", max(overhead_linux_perf))
print("Overhead of Simulated BayesPerf: ")
print("Average: ", statistics.mean(overhead_bayes))
print("Max: ", max(overhead_bayes))
print("Overhead of Tintin: ")
print("Average: ", statistics.mean(overhead_tintin))
print("Max: ", max(overhead_tintin))


#### Plot the figure
colors = sb.hls_palette(s=.3)
bar_width = 0.2
fig, ax = plt.subplots(1, 1, figsize=(13, 2.9))
plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.24)

# Set position of bar on X axis
bar1_idxes = np.arange(len(workloads))
bar2_idxes = [x + bar_width for x in bar1_idxes]
bar3_idxes = [x + 2*bar_width for x in bar1_idxes]
bar4_idxes = [x + 3*bar_width for x in bar1_idxes]

# plt.grid(axis = 'y', color='grey', linestyle='--', linewidth=3, zorder=-1.0)
# plt.rcParams['axes.axisbelow'] = True

ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=2)
# ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=2)
ax.set_axisbelow(True)
# ax.set_zorder(3)

# print("Overhead of Original: ", overhead_original)
# Make the plot
ax.bar(bar1_idxes, overhead_original, color="#f4edea", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Original')
ax.bar(bar2_idxes, overhead_bayes, color="#f4f1bb", width=bar_width,
        edgecolor='black', linewidth=1.5, label='BayesPerf (CPU)', hatch='//')
ax.bar([-1], [-1], color="#e6ebe0", width=bar_width,
        edgecolor='black', linewidth=1.5, label='CounterMiner - N/A', hatch='+')
ax.bar(bar3_idxes, overhead_linux_perf, color="#9BC1BC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Linux Perf', hatch='\\\\')
ax.bar(bar4_idxes, overhead_tintin, color="#A2C5AC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Tintin', hatch='xxx')



ax.set_xticks([r + bar_width + 0.1 for r in range(len(workloads))])
ax.set_xticklabels(workloads, rotation=25) #, position=(0, 0.05))


# plt.yscale("log", base = 2)

# plt.locator_params(axis='y', nbins=4)
ax.set_xlim(-0.5, len(workloads)+0.2)

ax.set_ylim(90, 140)

fig.text(0.01, 0.6, 'Normalized Runtime %', va='center', rotation='vertical')

ax.legend(ncol=5, loc="upper left")
# plt.tight_layout()

plt.savefig("titnin_benchmark_overhead.pdf", format='pdf')
plt.show()
