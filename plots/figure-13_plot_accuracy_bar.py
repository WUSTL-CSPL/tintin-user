
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
# Linux Perf #
##############
accuracy_linux_perf = [16.529447,  # -> 0
                       6.062688,   # -> 1	
                       1.457191,   # -> 2
                       5.32018,	   # -> 3
                       3.011186,   # -> 4
                       1.644545,   # -> 5
                       1.248174,   # -> 6
                       8.810304,   # -> 7
                       2.542991,   # -> 8
                       3.469216,   # -> 9
                       1.88251,	   # -> 10
                       2.590688,   # -> 11
                       0.243488,   # -> 12
                       20.039743,  # -> 13
                       5.366726,   # -> 14
                       10.915386,  # -> 15
                       20.356418,  # -> 16
                       13.51021,   # -> 17
                       14.359493,  # -> 18
                       14.300477,  # -> 19
                       1.953851,   # -> 20
                       1.042217,   # -> 21
                       7.137145,   # -> 22
                       8.955128,   # -> 23
                       53.273962,  # -> 24
                       8.23165]    # -> 25


#################
# Counter Miner #
#################
# Counter Miner #
#################
accuracy_counterminer = [10.828034,  # -> 0
                        8.639544,  # -> 1
                        1.113775,  # -> 2
                        4.924028,  # -> 3
                        5.305169, # -> 4
                        4.660027, # -> 5
                        2.295187,  # -> 6
                        10.232882, # -> 7
                        2.398043,  # -> 8
                        4.232566,  # -> 9
                        5.342633,  # -> 10
                        3.575787,  # -> 11
                        0.748921,  # -> 12
                        10.05949,  # -> 13
                        2.597341,  # -> 14
                        9.46037,   # -> 15
                        18.213501, # -> 16
                        14.176647, # -> 17
                        11.216938, # -> 18
                        14.906806, # -> 19
                        1.397313,  # -> 20
                        0.900864,  # -> 21
                        7.906806,  # -> 22
                        8.782847,  # -> 23
                        56.212632, # -> 24
                        8.581886]  # -> 25

############################
# Tintin Uncertainty-first #
############################
accuracy_uncertainty_first =   [8.82844,    # -> 0
                                2.922589,   # -> 1
                                5.068412,   # -> 2
                                2.102675,   # -> 3
                                2.4813,     # -> 4
                                0.806214,   # -> 5
                                0.325028,   # -> 6
                                4.078172,   # -> 7
                                4.876656,   # -> 8
                                8.168708,   # -> 9
                                2.303954,  # -> 10
                                1.909191,   # -> 11
                                1.757906,   # -> 12
                                8.667662,   # -> 13
                                2.1067,     # -> 14
                                1.17207,    # -> 15
                                4.366121,   # -> 16
                                2.946088,   # -> 17
                                6.62333,    # -> 18
                                4.464218,   # -> 19
                                2.56801,    # -> 20
                                1.906672,   # -> 21
                                4.303825,   # -> 22
                                32.898662,  # -> 23
                                50.600398,  # -> 24
                                1.192058]   # -> 25

##################
# Tintin Elastic # 
##################

accuracy_tintin_elastic =      [4.163906,   # -> 0
                                2.255919,   # -> 1
                                0.320673,   # -> 2
                                0.109137,   # -> 3
                                0.603455,   # -> 4
                                0.752569,   # -> 5
                                0.377711,   # -> 6
                                4.841263,   # -> 7
                                0.634844,   # -> 8
                                0.609077,   # -> 9
                                1.067431,   # -> 10
                                1.210764,   # -> 11
                                0.130639,   # -> 12
                                6.745031,   # -> 13
                                1.031357,   # -> 14
                                0.521014,   # -> 15
                                0.005863,   # -> 16
                                0.058797,   # -> 17
                                5.868118,   # -> 18
                                3.315176,   # -> 19
                                0.270783,   # -> 20
                                0.200274,   # -> 21
                                0.234408,   # -> 22
                                1.254573,   # -> 23
                                38.994042,  # -> 24
                                0.30719]    # -> 25
### End of loading data

#### Overover accuracy

print("Accuracy of Native Perf: ")
print("Average: ", statistics.mean(accuracy_linux_perf))
print("Max: ", max(accuracy_linux_perf))
print("Accuracy of CounterMiner: ")
print("Average: ", statistics.mean(accuracy_counterminer))
print("Max: ", max(accuracy_counterminer))
print("Accuracy of Uncertainty-first: ")
print("Average: ", statistics.mean(accuracy_uncertainty_first))
print("Max: ", max(accuracy_uncertainty_first))
print("Accuracy of Elastic Scheduling: ")
print("Average: ", statistics.mean(accuracy_tintin_elastic))
print("Max: ", max(accuracy_tintin_elastic))


#### Plot the figure
colors = sb.hls_palette(s=.3)
bar_width = 0.2
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 2.5))
plt.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.25)
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# Set position of bar on X axis
bar1_idxes = np.arange(len(workloads))
bar2_idxes = [x + bar_width for x in bar1_idxes]
bar3_idxes = [x + 2*bar_width for x in bar1_idxes]
bar4_idxes = [x + 3*bar_width for x in bar1_idxes]

# plt.grid(axis = 'y', color='grey', linestyle='--', linewidth=3, zorder=-1.0)
# plt.rcParams['axes.axisbelow'] = True

ax2.yaxis.grid(color='gray', linestyle='dashed', linewidth=2)
ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=2)
ax2.set_axisbelow(True)
# ax.set_zorder(3)

# Make the plot
ax2.bar(bar1_idxes, accuracy_linux_perf, color="#f4edea", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Linux Perf')
ax2.bar(bar2_idxes, accuracy_counterminer, color="#f4f1bb", width=bar_width,
        edgecolor='black', linewidth=1.5, label='CounterMiner', hatch='//')
ax2.bar([-1], [-1], color="#e6ebe0", width=bar_width,
        edgecolor='black', linewidth=1.5, label='BayesPerf - N/A', hatch='+')
ax2.bar(bar3_idxes, accuracy_uncertainty_first, color="#9BC1BC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Uncertainty-First', hatch='\\\\')
ax2.bar(bar4_idxes, accuracy_tintin_elastic, color="#A2C5AC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Elastic Scheduling', hatch='xxx')


# Make the plot
ax1.bar(bar1_idxes, accuracy_linux_perf, color="#f4edea", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Linux Perf')
ax1.bar(bar2_idxes, accuracy_counterminer, color="#f4f1bb", width=bar_width,
        edgecolor='black', linewidth=1.5, label='CounterMiner', hatch='//')
ax1.bar([-1], [-1], color="#e6ebe0", width=bar_width,
        edgecolor='black', linewidth=1.5, label='BayesPerf - N/A', hatch='+')
ax1.bar(bar3_idxes, accuracy_uncertainty_first, color="#9BC1BC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Uncertainty-First', hatch='\\\\')
ax1.bar(bar4_idxes, accuracy_tintin_elastic, color="#A2C5AC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Elastic Scheduling', hatch='xxx')




ax2.set_xticks([r + bar_width + 0.1 for r in range(len(workloads))])
ax2.set_xticklabels(workloads, rotation=30, ha='right', position=(0, 0.05))

ax1.set_xticks([])

# plt.yscale("log", base = 2)

# plt.locator_params(axis='y', nbins=4)
ax2.set_xlim(-0.5, len(workloads)+0.2)
ax1.set_xlim(-0.5, len(workloads)+0.2)

ax2.set_ylim(0, 10)
ax1.set_ylim(10, 50)

fig.text(0.01, 0.6, 'Normalized Error (%)', va='center', rotation='vertical')

ax1.legend(ncol=5, loc="upper left")
# plt.tight_layout()

plt.savefig("titnin_benchmark_error.pdf", format='pdf')
plt.show()
