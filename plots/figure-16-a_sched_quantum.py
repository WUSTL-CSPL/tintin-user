import numpy as np
import matplotlib.pyplot as plt


def main():


    #############
    # Data load
    #############
    labels = ["4ms", "2ms", "1ms", "0.4", "0.2", "0.1", "0.05"]

    original_exe_time = 370.399442

    tintin_exe_times = [
        371.036586,  # -> 4ms
        372.776459,  # -> 2ms
        374.429786,  # -> 1ms
        386.250793,  # -> 0.4ms
        406.504589,  # -> 0.2ms
        441.389778,  # -> 0.1ms
        527.7013     # -> 0.05ms
    ]

    tintin_overhead = [((x - original_exe_time) * 100) / original_exe_time for x in tintin_exe_times]

    tintin_acc = [
        7.362423,  # -> 4ms
        2.294223,  # -> 2ms
        1.59283,   # -> 1ms
        0.609147,  # -> 0.4ms
        0.783832,  # -> 0.2ms
        0.77174,   # -> 0.1ms
        0.904821   # -> 0.05ms
    ]
    #############
    # End of data
    #############

    bar_width = 0.2
    bar1_idxes = np.arange(len(tintin_acc))

    # Create the line plot
    fig, ax = plt.subplots(figsize=(4.5, 2.5))

    ax1 = ax.twinx()
    
    # ax.bar([1], [0], color='#7180B9', width=bar_width,
        # edgecolor='black', linewidth=1.5, label='Accuracy Linux Perf - N/A', hatch='\\\\')
    
    ax.plot([1], [-1], markerfacecolor='#774E24', color="black", marker='s', linestyle='-', label='Overhead')
    ax.bar(bar1_idxes, tintin_acc, color="#9DB5B2", width=bar_width,
        edgecolor='black', linewidth=1.5, label='Error', hatch='//')

    # ax1.plot(bar1_idxes, perf_overhead, color='#f4f1bb', marker='x', linestyle='-', label='Overhead - Linux Perf')
    ax1.plot(bar1_idxes, tintin_overhead, markerfacecolor='#774E24', color="black", marker='s', linestyle='-', label='Overhead')



    # ax.plot(iterations, method1, 'x', label='Linux Perf', linestyle='-',
    #         markerfacecolor='none', ms=8, markeredgecolor=colors[2], color=colors[2])
    # ax.plot(iterations, method2, 's', label='Tintin', linestyle='-',
    #         markerfacecolor='none', ms=8, markeredgecolor=colors[1], color=colors[1])
    # ax.plot(iterations, method3, '^', label='Tintin w/ Miner', linestyle='-',
    #         markerfacecolor='none', ms=8, markeredgecolor=colors[0], color=colors[0])

    # Customize the appearance of the plot
    # ax.set_xlabel('Frequency (HZ)', fontsize=16)
    ax.set_ylabel('Error (%)')
    ax1.set_ylabel('Overhead (%)')

    # ax.set_title('Training time per iteration for different optimization methods')

    ax.legend(loc="upper center")
    ax.set_ylim(0, 10)
    # ax1.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    # plt.xticks(np.arange(0, 9000, 1000))
    # plt.yticks(np.arange(0, 1.1, 0.1))
    x = [0, 1, 2, 3, 4, 5, 6]
    plt.xticks(x, labels)
    # ax.set_xticklabels(labels)
    # plt.ylim(0.5, 1.5)
    # plt.locator_params(axis='y', nbins=4)
    ax.locator_params(axis='y', nbins=4)
    plt.tight_layout()
    plt.savefig('monitor_scalability_accuracy.pdf', format='pdf')
    plt.show()


if __name__ == '__main__':
    main()
