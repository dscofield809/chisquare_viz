import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
from matplotlib.gridspec import GridSpec
import numpy as np
import sys
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist

#######################################################################

# This modification of main.py examines a situation in which two variables A and B
# may be related, but we're unsure of the causal direction.
# From a population, we collect a sample that is balanced with respect to A, and 
# perform a chi square test to see if A and B are independent. 
# We then do the same with a sample that is balanced with respect to B and compare the results. 
# In both cases, we use the largest possible balanced sample.

# For simplicity, let A be "treatment" and B be "recovery".

#######################################################################

def chiTest(table, alpha, sample_size, axis_to_graph, axis_to_print):
    # Performs chi2 test and displays result
    # Assumes that numbers in table are proportions of sample_size
    chi2_stat, p, dof, expected = chi2_contingency(table*sample_size)

    x = np.linspace(0, max(chi2_stat * 2, 10), 500)
    chiLine, = axis_to_graph.plot(x, chi2_dist.pdf(x, dof), label=f'Chi2 PDF (df={dof})')
    statLine = axis_to_graph.axvline(chi2_stat, color='red', linestyle='--', label=f'Statistic = {chi2_stat:.2f}')
    axis_to_graph.fill_between(x, 0, chi2_dist.pdf(x, dof), where=(x >= chi2_stat), color='red', alpha=1)
    axis_to_graph.set_title('Chi-Square Distribution', fontsize=12)
    axis_to_graph.set_xlabel('Value')
    axis_to_graph.set_ylabel('Density')
    axis_to_graph.set_ylim(0,0.5)
    axis_to_graph.legend()

    output_lines = []
    # output_lines.append(f"Degrees of freedom: {dof}")
    output_lines.append(f"Sample size: {sample_size:.2f}")
    output_lines.append(f"\nChi-square statistic: {chi2_stat:.4f}")
    output_lines.append(f"p-value: {p:.4f}")
    # output_lines.append(f"Alpha (significance level): {alpha}\n")

    # if p > alpha:
    #     output_lines.append("p-value is greater than alpha.\n\nFail to reject the null hypothesis:\ntreatment and recovery may be independent")
    # else:
    #     output_lines.append("p-value is less than or equal to alpha.\n\nReject the null hypothesis:\nwe conclude that treatment and recovery are dependent")

    output_text = '\n'.join(output_lines)
    axis_to_print.text(0, 1, output_text, va='top', ha='left', fontsize=14)
    #axis_to_print.set_title('Result of Chi-Square Test', fontsize=12)

    return

#######################################################################

# define parameters 
proportion_treated_recovered = 0.15
proportion_treated_not_recovered = 0.15
proportion_not_treated_recovered = 0.3
proportion_not_treated_not_recovered = 0.4

# proportion_treated_recovered = 4/138
# proportion_treated_not_recovered = 78/138
# proportion_not_treated_recovered = 11/138
# proportion_not_treated_not_recovered = 45/138

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
gs = GridSpec(5, 2, figure=fig, height_ratios=[1.75, 0.2, 1.5, 0.1, 1])

# ---- TABLE A (Top Left) ----
ax_table_A = fig.add_subplot(gs[0, 0])
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
ax_table_A.set_title('Contingency Table (Treatment Balanced)')

for key, cell in table_A.get_celld().items():
    cell.get_text().set_fontsize(12)

# Store references to text cells
cell_text_refs_A = [
    table_A.get_celld()[(1, 0)].get_text(),
    table_A.get_celld()[(1, 1)].get_text(),
    table_A.get_celld()[(2, 0)].get_text(),
    table_A.get_celld()[(2, 1)].get_text()
]

# ---- TABLE B (Top Right) ----
ax_table_B = fig.add_subplot(gs[0, 1])
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
ax_table_B.set_title('Contingency Table (Recovery Balanced)')

for key, cell in table_B.get_celld().items():
    cell.get_text().set_fontsize(12)

# Store references to text cells
cell_text_refs_B = [
    table_B.get_celld()[(1, 0)].get_text(),
    table_B.get_celld()[(1, 1)].get_text(),
    table_B.get_celld()[(2, 0)].get_text(),
    table_B.get_celld()[(2, 1)].get_text()
]

# # ---- SLIDER ----
slider_axes = fig.add_subplot(gs[1, 0])
sliders = [
    Slider(slider_axes, label="Population size", valmin=0, valmax=10000, valstep=100, valinit=1000),
]
sliders[0].label.set_fontsize(12)  # Increase label font size
sliders[0].valtext.set_fontsize(12)  # Increase value font size


# ---- GRAPH (Mid left side) ----
ax_graph_A = fig.add_subplot(gs[2, 0]) 

# ---- GRAPH (Mid right side) ----
ax_graph_B = fig.add_subplot(gs[2, 1]) 

# ---- Text output (Lower left side) ----
ax_print_A = fig.add_subplot(gs[4, 0])
ax_print_A.axis('off')

# ---- Text output (Lower right side) ----
ax_print_B = fig.add_subplot(gs[4, 1])
ax_print_B.axis('off')


#######################################################################

alpha = 0.05 # significance level
N = 1000
proportion_balancedT = min(proportion_treated, proportion_not_treated)*2
sample_size_balancedT = proportion_balancedT*N
proportion_balancedR = min(proportion_recovered, proportion_not_recovered)*2
sample_size_balancedR = proportion_balancedR*N
# Run test once initially, then update dynamically with slider input
chiTest(contingency_table_balancedT, alpha, sample_size_balancedT, ax_graph_A, ax_print_A)
chiTest(contingency_table_balancedR, alpha, sample_size_balancedR, ax_graph_B, ax_print_B)

# ---- UPDATE FUNCTION ----
def update(val):
    # Update N from slider
    N = sliders[0].val

    # clear stuff
    ax_graph_A.clear()
    ax_graph_B.clear()
    ax_print_A.clear()
    ax_print_A.axis('off')
    ax_print_B.clear()
    ax_print_B.axis('off')

    # Recalculate with new N
    proportion_balancedT = min(proportion_treated, proportion_not_treated)*2
    sample_size_balancedT = proportion_balancedT*N
    proportion_balancedR = min(proportion_recovered, proportion_not_recovered)*2
    sample_size_balancedR = proportion_balancedR*N
    chiTest(contingency_table_balancedT, alpha, sample_size_balancedT, ax_graph_A, ax_print_A)
    chiTest(contingency_table_balancedR, alpha, sample_size_balancedR, ax_graph_B, ax_print_B)

    fig.canvas.draw_idle()

# Connect sliders to update
for slider in sliders:
    slider.on_changed(update)

fig.subplots_adjust(hspace=0.5)  # Increase vertical space between rows
plt.show()