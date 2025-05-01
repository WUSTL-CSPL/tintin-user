import numpy as np
import matplotlib.pyplot as plt


def main():
    
    #############
    # Data load #
    #############
    labels = ["15ms", "10ms", "8ms", "6ms", "4ms", "2ms", "1ms"]

    tintin_acc = [1.016529, # -> 15ms
                  1.002772, # -> 10ms
                  1.03464,  # -> 8ms
                  0.821001, # -> 6ms	
                  0.320673, # -> 4ms
                  0.2546,	# -> 2ms
                  0.225636] # -> 1ms

    perf_acc =   [7.877099,	# -> 15ms
                  4.966144,	# -> 10ms
                  3.114047,	# -> 8ms
                  3.101177,	# -> 6ms
                  1.457191,	# -> 4ms
                  2.01528,	# -> 2ms
                  2.879169] # -> 1ms
    

    #############
    # End of data
    #############

    bar_width = 0.2
    import statistics
    print("Perf Average", statistics.mean(perf_acc))
    print("Tintin Average", statistics.mean(tintin_acc))
    bar1_idxes = np.arange(len(perf_acc))
    bar2_idxes = [x + bar_width for x in bar1_idxes]

    # Create the line plot
    fig, ax = plt.subplots(figsize=(4, 2.5))


    plt.text(4.2, 4.5, "CPU task \n scheduling \n interval", color='black', fontsize=8, ha='center')

    plt.bar(bar1_idxes, perf_acc, color='#7180B9', width=bar_width,
        edgecolor='black', linewidth=1.5, label='Linux Perf', hatch='\\\\')
    
    plt.bar(bar2_idxes, tintin_acc, color="#9DB5B2", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Tintin', hatch='//')

    ax.set_ylabel('Error (%)')

    ax.legend(loc="upper right")
    ax.grid(True, linestyle='--', alpha=0.7)

    x = [0, 1, 2, 3, 4]
    plt.xticks([r + 0.5 for r in range(len(labels))], labels, ha='right')
    plt.locator_params(axis='y', nbins=5)
    plt.tight_layout()

    plt.savefig('sched_scalability_accuracy.pdf', format='pdf')
    plt.show()


if __name__ == '__main__':
    main()
