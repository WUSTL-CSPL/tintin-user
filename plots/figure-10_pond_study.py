import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker


colors = sns.color_palette("Paired")

count = 0
rr_better_than_emon = 0
elastic_better_than_rr = 0
diff = 0
emon_res = []
tintin_rr_res = []
tintin_elastic_res = []
tintin_rr_uncertainty_res = []
tintin_elastic_uncertainty_res = []


with open("results.txt", "r") as f:
    for line in f:        
        emon_value = float(re.search(r'emon=([\-0-9.]+)', line).group(1))
        emon_res.append(emon_value)
        rr_value = float(re.search(r'tintin_rr=([\-0-9.]+)', line).group(1))
        tintin_rr_res.append(rr_value)
        elastic_value = float(re.search(r'elastic_score=([\-0-9.]+)', line).group(1))
        tintin_elastic_res.append(elastic_value)
        tintin_rr_uncertainty_value = float(re.search(r'rr_nrmse=([\-0-9.]+)', line).group(1))
        tintin_rr_uncertainty_res.append(tintin_rr_uncertainty_value)
        tintin_elastic_uncertainty_value = float(re.search(r'nrmse_elastic=([\-0-9.]+)', line).group(1))
        tintin_elastic_uncertainty_res.append(tintin_elastic_uncertainty_value)

        count += 1

        if elastic_value > rr_value : # and elastic_value < rr_value:
            diff += elastic_value - rr_value       
            elastic_better_than_rr += 1


# Sort the data by tintin_elastic_uncertainty_res
sorted_data = sorted(
    zip(
        emon_res,
        tintin_elastic_uncertainty_res,
        tintin_rr_res,
        tintin_elastic_res,
        tintin_rr_uncertainty_res,
    ),
    key=lambda x: x[1],
)

# Unpack the sorted data back into individual lists
(
    emon_res,
    tintin_elastic_uncertainty_res,
    tintin_rr_res,
    tintin_elastic_res,
    tintin_rr_uncertainty_res,
) = map(list, zip(*sorted_data))


### Plot the figure
fig, axs = plt.subplots(1, 3, figsize=(5, 5))

indexes = range(len(emon_res))

# axs[0].set_xticks([])
axs[1].set_yticks([])
axs[2].set_yticks([])

colors[3] = '#1F6B34'

axs[0].barh(indexes, tintin_rr_res, color=colors[3], label='Tintin')
axs[0].barh(indexes, emon_res, color='#AE6B88', label='EMON')
axs[0].set_xlim([0, 1])
axs[0].set_ylim([0, 100])
axs[0].legend(loc='lower right')
axs[0].xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))

axs[1].barh(indexes, tintin_elastic_res, color=colors[3], label='Elastic')
axs[1].barh(indexes, tintin_rr_res, color='#6D7DA2', label='RR')

axs[1].set_xlim([0, 1])
axs[1].set_ylim([0, 100])
axs[1].legend(loc='lower right')
axs[1].xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))


axs[2].barh(indexes, tintin_elastic_uncertainty_res, color=colors[3], label='with U.')
axs[2].barh(indexes, tintin_elastic_res, color='#DF845D', label='w/o U.')

axs[2].set_xlim([0, 1])
axs[2].set_ylim([0, 100])
axs[2].legend(loc='lower right')
axs[2].xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))


axs[0].set_ylabel('Experiment Set')
axs[0].set_xlabel('Flexible Scope')
axs[1].set_xlabel('Elastic Scheduling')
axs[2].set_xlabel('Uncertainty')

plt.tight_layout()
plt.subplots_adjust(wspace=0.06, hspace=0.06)
plt.savefig('pond_results.pdf', format='pdf', bbox_inches='tight')
plt.show()
