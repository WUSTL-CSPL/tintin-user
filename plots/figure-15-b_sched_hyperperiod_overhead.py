import numpy as np
import matplotlib.pyplot as plt


def main():

    #############
    # Data load
    #############

    labels = ["15ms", "10ms", "8ms", "6ms", "4ms", "2ms", "1ms"]

    baseline_exe_time = 373.297467

    tintin_overhead = [384.085075,	# -> 15ms
                       385.160049,	# -> 10ms
                       386.165428,	# -> 8ms
                       386.272717,	# -> 6ms
                       387.446705,	# -> 4ms
                       390.288957,	# -> 2ms
                       391.165532]  # -> 1ms

    perf_overhead = [374.533443,	# -> 15ms
                     374.771692,	# -> 10ms
                     374.956457,	# -> 8ms
                     374.940195,	# -> 6ms
                     374.111413,	# -> 4ms
                     374.633297,	# -> 2ms
                     377.170915]    # -> 1ms
    
    tintin_overhead = [((x - baseline_exe_time) * 100) / baseline_exe_time for x in tintin_overhead]
    perf_overhead = [((x - baseline_exe_time) * 100) / baseline_exe_time for x in perf_overhead]


    #############
    # End of data
    #############

    bar_width = 0.2
    import statistics
    print("Perf Average", statistics.mean(perf_overhead))
    print("Tintin Average", statistics.mean(tintin_overhead))
    bar1_idxes = np.arange(len(perf_overhead))
    bar2_idxes = [x + bar_width for x in bar1_idxes]

    # Create the line plot
    fig, ax = plt.subplots(figsize=(4, 2.5))


    plt.text(4.2, 4.0, "CPU task \n scheduling \n interval", color='black', fontsize=8, ha='center')

    plt.bar(bar1_idxes, perf_overhead, color='#f4f1bb', width=bar_width,
        edgecolor='black', linewidth=1.5, label='Linux Perf', hatch='\\\\')
    
    plt.bar(bar2_idxes, tintin_overhead, color="#A2C5AC", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Tintin', hatch='//')

    ax.set_ylabel('Overhead (%)')

    ax.legend(loc="upper left")
    ax.grid(True, linestyle='--', alpha=0.7)

    x = [0, 1, 2, 3, 4]
    plt.xticks([r + 0.5 for r in range(len(labels))], labels, ha='right')

    plt.locator_params(axis='y', nbins=5)
    plt.tight_layout()

    plt.savefig('sched_scalability_overhead.pdf', format='pdf')
    plt.show()


if __name__ == '__main__':
    main()
