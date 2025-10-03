import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
from matplotlib.gridspec import GridSpec
import numpy as np
import sys
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist

#######################################################################

# this version does not currently work because the sliders for proportions need to be
# appropriately constrained so that the sum of all four proportions is 1

# This modification of main.py examines a situation in which two variables A and B
# may be related, but we're unsure of the causal direction.
# From a population, we collect a sample that is balanced with respect to A, and 
# perform a chi square test to see if A and B are independent. 
# We then do the same with a sample that is balanced with respect to B and compare the results. 
# In both cases, we use the largest possible balanced sample.

# For simplicity, let A be "treatment" and B be "recovery".

#######################################################################

def chiTestNoGraph(table, alpha, sample_size, axis_to_print):
    # Performs chi2 test and displays result
    # Assumes that numbers in table are proportions of sample_size
    chi2_stat, p, dof, expected = chi2_contingency(table*sample_size)

    output_lines = []
    output_lines.append(f"Sample size: {sample_size:.2f}")
    output_lines.append(f"\nChi-square statistic: {chi2_stat:.4f}")
    output_lines.append(f"p-value: {p:.4f}")

    output_text = '\n'.join(output_lines)
    axis_to_print.text(0, 1, output_text, va='top', ha='left', fontsize=14)

    return

#######################################################################

# initial proportions for population
proportion_treated_recovered = 0.15
proportion_treated_not_recovered = 0.15
proportion_not_treated_recovered = 0.30
proportion_not_treated_not_recovered = 0.40

# Initial values for table
population_table = np.array([[proportion_treated_recovered, proportion_treated_not_recovered],
                  [proportion_not_treated_recovered, proportion_not_treated_not_recovered]])

proportion_treated = proportion_treated_recovered + proportion_treated_not_recovered
proportion_not_treated = proportion_not_treated_recovered + proportion_not_treated_not_recovered
proportion_recovered = proportion_treated_recovered + proportion_not_treated_recovered
proportion_not_recovered = proportion_treated_not_recovered + proportion_not_treated_not_recovered

pTgivenR = proportion_treated_recovered / proportion_recovered
pTgivenNotR = proportion_treated_not_recovered / proportion_not_recovered
pNotTgivenR = proportion_not_treated_recovered / proportion_recovered
pNotTgivenNotR = proportion_not_treated_not_recovered / proportion_not_recovered

pRgivenT = proportion_treated_recovered / proportion_treated
pRgivenNotT = proportion_not_treated_recovered / proportion_not_treated
pNotRgivenT = proportion_treated_not_recovered / proportion_treated
pNotRgivenNotT = proportion_not_treated_not_recovered / proportion_not_treated


# Random sample balanced for treatment
contingency_table_balancedT = np.array([[0.5*pRgivenT, 0.5*pNotRgivenT], #treated/recovered, treated/not recovered
                  [0.5*pRgivenNotT, 0.5*pNotRgivenNotT]]) #not treated/recovered, not treated/not recovered

# Random sample balanced for recovery
contingency_table_balancedR = np.array([[0.5*pTgivenR, 0.5*pTgivenNotR], #treated/recovered, treated/not recovered
                  [0.5*pNotTgivenR, 0.5*pNotTgivenNotR]]) #not treated/recovered, not treated/not recovered



# Create figure with 2 columns
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(9, 2, figure=fig, height_ratios=[0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.4, 2, 0.4])



# ---- SLIDERS (Top Left) ----
slider_cont_axes = [fig.add_subplot(gs[i, 0]) for i in range(4)]
slider_cont = [
    Slider(slider_cont_axes[0], label="Treat/Rec", valmin=0, valmax=1, valstep=0.01, valinit=0.5),
    Slider(slider_cont_axes[1], label="Treat/NotRec", valmin=0, valmax=1, valstep=0.01, valinit=0.5),
    Slider(slider_cont_axes[2], label="NotTreat/Rec", valmin=0, valmax=1, valstep=0.01, valinit=0.5),
    Slider(slider_cont_axes[3], label="NotTreat/NotRec", valmin=0, valmax=1, valstep=0.01, valinit=0.5)
]
for i in range(4):
    slider_cont[i].label.set_fontsize(12)  # Increase label font size
    slider_cont[i].valtext.set_fontsize(12)  # Increase value font size  

# ---- Text output (Upper right side) ----
ax_print_poptitle = fig.add_subplot(gs[0, 1])
ax_print_poptitle.axis('off')
ax_print_poptitle.text(0.1, 1, 'Population', va='top', ha='center', fontsize=14)

# ---- TABLE (Top Right) ----
ax_table_pop = fig.add_subplot(gs[1:5, 1])
ax_table_pop.axis('off')

cell_text_pop = [
    [f"{population_table[0][0]:.3f}", f"{population_table[0][1]:.3f}"],
    [f"{population_table[1][0]:.3f}", f"{population_table[1][1]:.3f}"]
]
col_labels_pop = ["Recovered", "Did not recover"]
row_labels_pop = ["Treatment", "No treatment"]

table_pop = ax_table_pop.table(
    cellText=cell_text_pop,
    rowLabels=row_labels_pop,
    colLabels=col_labels_pop,
    #loc='center',
    bbox=[.3, .3, 0.8, 0.8],
    cellLoc='center'
)
#table_pop.scale(0.8, 2.5)
#ax_table_pop.set_title('Population')

for key, cell in table_pop.get_celld().items():
    cell.get_text().set_fontsize(12)

# Store references to text cells
cell_text_refs = [
    table_pop.get_celld()[(1, 0)].get_text(),
    table_pop.get_celld()[(1, 1)].get_text(),
    table_pop.get_celld()[(2, 0)].get_text(),
    table_pop.get_celld()[(2, 1)].get_text()
]


# # ---- SLIDER (population size) ----
slider_pop_axes = fig.add_subplot(gs[5, 0])
slider_pop = [
    Slider(slider_pop_axes, label="Population size", valmin=0, valmax=10000, valstep=100, valinit=1000, color='red'),
]
slider_pop[0].label.set_fontsize(12)  # Increase label font size
slider_pop[0].valtext.set_fontsize(12)  # Increase value font size

# ---- TABLE A  ----
ax_table_A = fig.add_subplot(gs[7, 0])
ax_table_A.axis('off')

cell_text_A = [
    [f"{contingency_table_balancedT[0][0]:.3f}", f"{contingency_table_balancedT[0][1]:.3f}"],
    [f"{contingency_table_balancedT[1][0]:.3f}", f"{contingency_table_balancedT[1][1]:.3f}"]
]
col_labels_A = ["Recovered", "Did not recover"]
row_labels_A = ["Treatment", "No treatment"]

table_A = ax_table_A.table(
    cellText=cell_text_A,
    rowLabels=row_labels_A,
    colLabels=col_labels_A,
    loc='center',
    cellLoc='center'
)
table_A.scale(0.8, 2.5)
ax_table_A.set_title('Contingency Table (Treatment Balanced Sample)')

for key, cell in table_A.get_celld().items():
    cell.get_text().set_fontsize(12)

# Store references to text cells
cell_text_refs_A = [
    table_A.get_celld()[(1, 0)].get_text(),
    table_A.get_celld()[(1, 1)].get_text(),
    table_A.get_celld()[(2, 0)].get_text(),
    table_A.get_celld()[(2, 1)].get_text()
]

# ---- TABLE B ----
ax_table_B = fig.add_subplot(gs[7, 1])
ax_table_B.axis('off')

cell_text_B = [
    [f"{contingency_table_balancedR[0][0]:.3f}", f"{contingency_table_balancedR[0][1]:.3f}"],
    [f"{contingency_table_balancedR[1][0]:.3f}", f"{contingency_table_balancedR[1][1]:.3f}"]
]
col_labels_B = ["Recovered", "Did not recover"]
row_labels_B = ["Treatment", "No treatment"]

table_B = ax_table_B.table(
    cellText=cell_text_B,
    rowLabels=row_labels_B,
    colLabels=col_labels_B,
    loc='center right',
    cellLoc='center',
)
table_B.scale(0.8, 2.5)
ax_table_B.set_title('Contingency Table (Recovery Balanced Sample)')

for key, cell in table_B.get_celld().items():
    cell.get_text().set_fontsize(12)

# Store references to text cells
cell_text_refs_B = [
    table_B.get_celld()[(1, 0)].get_text(),
    table_B.get_celld()[(1, 1)].get_text(),
    table_B.get_celld()[(2, 0)].get_text(),
    table_B.get_celld()[(2, 1)].get_text()
]


# ---- Text output (Lower left side) ----
ax_print_A = fig.add_subplot(gs[8, 0])
ax_print_A.axis('off')

# ---- Text output (Lower right side) ----
ax_print_B = fig.add_subplot(gs[8, 1])
ax_print_B.axis('off')



#######################################################################

alpha = 0.05 # significance level
N = 1000
proportion_balancedT = min(proportion_treated, proportion_not_treated)*2
sample_size_balancedT = proportion_balancedT*N
proportion_balancedR = min(proportion_recovered, proportion_not_recovered)*2
sample_size_balancedR = proportion_balancedR*N
# Run test once initially, then update dynamically with slider input
chiTestNoGraph(contingency_table_balancedT, alpha, sample_size_balancedT, ax_print_A)
chiTestNoGraph(contingency_table_balancedR, alpha, sample_size_balancedR, ax_print_B)

# ---- UPDATE FUNCTION ----
def update(val):
    # Update values from slider
    N = slider_pop[0].val
    for i, slider in enumerate(slider_cont):
        cell_text_refs[i].set_text(f"{slider.val:.3f}")

    proportion_treated_recovered = slider_cont[0].val
    proportion_treated_not_recovered = slider_cont[1].val
    proportion_not_treated_recovered = slider_cont[2].val
    proportion_not_treated_not_recovered = slider_cont[3].val

    # pop_table_update = np.array([[proportion_treated_recovered, proportion_treated_not_recovered],
    #               [proportion_not_treated_recovered, proportion_not_treated_not_recovered]])

    # clear stuff
    ax_print_A.clear()
    ax_print_A.axis('off')
    ax_print_B.clear()
    ax_print_B.axis('off')

    # Recalculate with new values
    
    proportion_treated = proportion_treated_recovered + proportion_treated_not_recovered
    proportion_not_treated = proportion_not_treated_recovered + proportion_not_treated_not_recovered
    proportion_recovered = proportion_treated_recovered + proportion_not_treated_recovered
    proportion_not_recovered = proportion_treated_not_recovered + proportion_not_treated_not_recovered

    pTgivenR = proportion_treated_recovered / proportion_recovered
    pTgivenNotR = proportion_treated_not_recovered / proportion_not_recovered
    pNotTgivenR = proportion_not_treated_recovered / proportion_recovered
    pNotTgivenNotR = proportion_not_treated_not_recovered / proportion_not_recovered

    pRgivenT = proportion_treated_recovered / proportion_treated
    pRgivenNotT = proportion_not_treated_recovered / proportion_not_treated
    pNotRgivenT = proportion_treated_not_recovered / proportion_treated
    pNotRgivenNotT = proportion_not_treated_not_recovered / proportion_not_treated

    # Random sample balanced for treatment
    contingency_table_balancedT = np.array([[0.5*pRgivenT, 0.5*pNotRgivenT], #treated/recovered, treated/not recovered
                    [0.5*pRgivenNotT, 0.5*pNotRgivenNotT]]) #not treated/recovered, not treated/not recovered

    # Random sample balanced for recovery
    contingency_table_balancedR = np.array([[0.5*pTgivenR, 0.5*pTgivenNotR], #treated/recovered, treated/not recovered
                    [0.5*pNotTgivenR, 0.5*pNotTgivenNotR]]) #not treated/recovered, not treated/not recovered

    proportion_balancedT = min(proportion_treated, proportion_not_treated)*2
    sample_size_balancedT = proportion_balancedT*N
    proportion_balancedR = min(proportion_recovered, proportion_not_recovered)*2
    sample_size_balancedR = proportion_balancedR*N
    chiTestNoGraph(contingency_table_balancedT, alpha, sample_size_balancedT, ax_print_A)
    chiTestNoGraph(contingency_table_balancedR, alpha, sample_size_balancedR, ax_print_B)

    fig.canvas.draw_idle()

# Connect sliders to update
for slider in slider_pop:
    slider.on_changed(update)
for slider in slider_cont:
    slider.on_changed(update)

fig.subplots_adjust(hspace=0.5)  # Increase vertical space between rows
plt.show()