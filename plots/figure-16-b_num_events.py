import numpy as np
import matplotlib.pyplot as plt


def main():

    labels = ["8", "16", "48", "96", "256", "512"] # , "1024"]

    linux_perf_errors = [1.080109, # -> 8
                        4.314312,  # -> 16
                        16.585817, # -> 48
                        18.827776, # -> 96
                        21.585817, # -> 256
                        25.081633] #, # -> 512
                        # 31.585904] # -> 1024
    tintin_errors = [0.042007,     # -> 8
                     0.192172,    # -> 16
                     0.87899,     # -> 48
                     1.616877,    # -> 96
                     2.238578,    # -> 256
                     5.416915]#,    # -> 512     
                    #  -1.0]        # -> 1024     Tintin gets stuck in kernel
    
    #############
    # End of data
    #############

    bar_width = 0.2
    bar1_idxes = np.arange(len(tintin_errors))
    bar2_idxes = [x + bar_width for x in bar1_idxes]


    # Create the line plot
    # fig, ax = plt.subplots(figsize=(3.7, 2.5))
    fig, ax = plt.subplots(figsize=(2.775, 1.875))

    plt.subplots_adjust(
        top=0.94,
        bottom=0.162,
        left=0.183,
        right=0.842,
        hspace=0.145,
        wspace=0.105
    )


    ax.bar(bar1_idxes, linux_perf_errors, color="#7180B9", width=bar_width,
        edgecolor='black', linewidth=1.5, hatch='\\\\', label='Perf')
    ax.bar(bar2_idxes, tintin_errors, color="#9DB5B2", width=bar_width,
        edgecolor='black', linewidth=1.5, hatch='//', label='Tintin')

    ax.set_ylabel('Error (%)')


    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_ylim(0, 35)
    ax.legend()
    # x = [0, 1, 2, 3, 4, 5, 6]
    x = [0, 1, 2, 3, 4, 5]
    plt.xticks(x, labels)
    ax.locator_params(axis='y', nbins=4)
    plt.tight_layout()
    plt.savefig('num_of_event_accuracy.pdf', format='pdf')
    plt.show()


if __name__ == '__main__':
    main()
