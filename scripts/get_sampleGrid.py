import json
import matplotlib.pyplot as plt
import numpy as np

# Read JSON data from the file
with open('grid_monoHtt_run2.json', 'r') as f:
    data = json.load(f)

# Function to plot data from a given dataset
def plot_dataset(dataset, ax, legend_, title, x_ax, y_ax, bullet_size):
    x = []
    y = []

    for key, values in dataset.items():
        for value in values:
            x.append(int(key))
            y.append(value)

    ax.scatter(x, y, label=legend_, s=bullet_size)
    ax.set_title(title)
    ax.set_xlabel(x_ax)
    ax.set_ylabel(y_ax)
    ax.legend()


# Create a figure with subplots
#fig, axs = plt.subplots(1, 3, figsize=(15, 5))
fig1, axs1 = plt.subplots()
fig2, axs2 = plt.subplots()
#axs.legend()

# Plot each dataset
plot_dataset(data['twohdma_2017'], axs1, '2HDMa 2017/2018', '2HDMa Grid', '$M_A$ (GeV)', '$M_a$ (GeV)', 15)
plot_dataset(data['new_twohdma_2017'], axs1, 'new 2017/2018', '2HDMa Grid', '$M_A$ (GeV)', '$M_a$ (GeV)', 15)
fig1.savefig('twoHDMa_grid.pdf', format='pdf')
#plot_dataset(data['zprime_2016'], axs[2], 'Dataset 3')
plot_dataset(data['new_zprime_2017'], axs2, 'new_zprime_2017/2018', "Baryonic-Z'", "$M_Z'$ (GeV)", "$M_{#chi} GeV$", 75)
plot_dataset(data['zprime_2017'], axs2, 'zprime_2017/2018', 'Baryonic-Z', '$M_Z$ (GeV)', '$M_{chi}$ GeV', 50)
plot_dataset(data['zprime_2016'], axs2, 'zprime_2016', 'Baryonic-Z', '$M_Z$ (GeV)', '$M_{chi}$ GeV', 10)
fig2.savefig('zprime_grid.pdf', format='pdf')
#plot_dataset(data['new_zprime_2017'], axs[2], 'Dataset 3')

# Adjust layout and show plot
#plt.tight_layout()
#plt.show()
