import matplotlib.pyplot as plt
import numpy as np


##### Raw data for sampling + process switching
#[15371648 8805088 8687254 11007492 21005948 15355361 16791905 23579814 20463560 22298547 ]
########


# Defining the data for the plots
# Data from the left plot (approximated from the image)
left_x = [1, 2, 3, 4, 8, 16]
left_y = [0.96e7, 0.965e7, 0.96e7, 0.959e7, 1.14e7, 1.06e7]
left_yerr = [0.03e7, 0.035e7, 0.025e7, 0.025e7, 0.2e7, 0.2e7]  # Uniform error as placeholder

even_spaced_x = np.arange(len(left_x))

# Data from the right plot (approximated from the image)
right_x = ['Core', 'Task', 'Phase', 'Sampl.']
right_y = [1.1e7, 0.92e7, 0.9e7, 16336662]
right_yerr = [0.25e7, 0.07e7, 0.05e7, 5220923]

# Creating a new figure and a subplot with shared y-axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 2.8),gridspec_kw={'width_ratios': [3, 2.5]}, sharey=True)

ax1.set_facecolor('lightgrey')
ax2.set_facecolor('lightgrey')

# Plotting the left graph
ax1.errorbar(even_spaced_x, left_y, yerr=left_yerr, fmt='rx--', ecolor='black', elinewidth=1, capsize=6, capthick=2, markersize=10)
# ax1.set_xscale('linear')
ax1.set_yscale('linear')
# ax1.set_title('Number of Multiplexed Events')
ax1.set_xlabel('Number of Multiplexed Events')
ax1.set_ylabel('Counter Value')
ax1.set_xticks(even_spaced_x)
# ax1.set_yticks(np.arange(0.8e7, 1.4e7, 0.1e7))
ax1.set_xticklabels(left_x)
ax1.grid(True, which='both', linestyle='-', linewidth=0.5, color='white')

ax1.spines['top'].set_visible(False)    # Remove top border
ax1.spines['right'].set_visible(False)  # Remove right border
ax1.spines['bottom'].set_visible(False) # Remove bottom border
ax1.spines['left'].set_visible(False)   # Remove left border
ax1.set_ylim([0.8e7, 1.8e7])
ax2.set_ylim([0.8e7, 1.8e7])

# Plotting the right graph
right_x_numeric = np.arange(len(right_x))  # Convert category labels to numeric values for plotting
ax2.errorbar(right_x_numeric, right_y, yerr=right_yerr, fmt='o-', color='purple', ecolor='black', elinewidth=1, capsize=6, capthick=2, markersize=8)
ax2.set_xlabel('Scope')
ax2.set_xticks(right_x_numeric)
ax2.set_xticklabels(right_x)
ax2.grid(True, which='both', linestyle='-', linewidth=0.5, color='white')

ax2.spines['top'].set_visible(False)    # Remove top border
ax2.spines['right'].set_visible(False)  # Remove right border
ax2.spines['bottom'].set_visible(False) # Remove bottom border
ax2.spines['left'].set_visible(False)   # Remove left border

# Set the background color for both subplots to match the image
for label in ax1.get_yticklabels():
    label#.set_fontsize(15)
ax1.yaxis.get_offset_text()#.set_fontsize(15)

# Set the background color for the figure to match the image
# fig.patch.set_facecolor('white')

# Tight layout to ensure no overlapping
plt.tight_layout()

# Display the plot
plt.savefig('new_multiplexing.pdf', format='pdf', bbox_inches='tight')
plt.show()


