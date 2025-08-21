import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist

# Initial values for the table
init_values = [5, 3, 
               7, 2]  # [R1C1, R1C2, R2C1, R2C2]

# # Example 2x2 contingency table
# #        Success  Failure
# # Group1   20       15
# # Group2   30       25
contingency_table = np.array([[55, 45],
                  [40, 60]])


# Create figure with 2 columns: left for table+sliders, right for graph
fig = plt.figure(figsize=(8, 6))
gs = GridSpec(6, 2, figure=fig, height_ratios=[2, 0.5, 0.5, 0.5, 0.5, 0.4])

# ---- TABLE (Top Left) ----
ax_table = fig.add_subplot(gs[0, 0])
ax_table.axis('off')

cell_text = [
    [f"{contingency_table[0][0]:.2f}", f"{contingency_table[0][1]:.2f}"],
    [f"{contingency_table[1][0]:.2f}", f"{contingency_table[1][1]:.2f}"]
]
col_labels = ["Recovered", "Did not recover"]
row_labels = ["Treatment", "No treatment"]

table = ax_table.table(
    cellText=cell_text,
    rowLabels=row_labels,
    colLabels=col_labels,
    loc='upper left',
    cellLoc='center'
)
table.scale(1, 2)

# Store references to text cells
cell_text_refs = [
    table.get_celld()[(1, 0)].get_text(),
    table.get_celld()[(1, 1)].get_text(),
    table.get_celld()[(2, 0)].get_text(),
    table.get_celld()[(2, 1)].get_text()
]

# ---- SLIDERS (Bottom Left) ----
slider_axes = [fig.add_subplot(gs[i, 0]) for i in range(1, 5)]
sliders = [
    Slider(slider_axes[0], label="Value (R1C1)", valmin=0, valmax=100, valinit=contingency_table[0][0]),
    Slider(slider_axes[1], label="Value (R1C2)", valmin=0, valmax=100, valinit=contingency_table[0][1]),
    Slider(slider_axes[2], label="Value (R2C1)", valmin=0, valmax=100, valinit=contingency_table[1][0]),
    Slider(slider_axes[3], label="Value (R2C2)", valmin=0, valmax=100, valinit=contingency_table[1][1])
]

# ---- GRAPH (Right Side) ----
ax_graph = fig.add_subplot(gs[0, 1])  # Big plot spanning top rows on right
# x = np.linspace(0, 10, 100)
# Calculate initial state when window opens
chi2_stat, p, dof, expected = chi2_contingency(contingency_table)

x = np.linspace(0, max(chi2_stat * 2, 10), 500)
chiLine, = ax_graph.plot(x, chi2_dist.pdf(x, dof), label=f'Chi2 PDF (df={dof})')
statLine = ax_graph.axvline(chi2_stat, color='red', linestyle='--', label=f'Statistic = {chi2_stat:.2f}')
ax_graph.fill_between(x, 0, chi2_dist.pdf(x, dof), where=(x >= chi2_stat), color='red', alpha=1)
ax_graph.set_title('Chi-Square Distribution', fontsize=12)
ax_graph.set_xlabel('Value')
ax_graph.set_ylabel('Density')
ax_graph.legend()

# A_init = contingency_table[0][0] + contingency_table[0][1]
# B_init = contingency_table[1][0] + contingency_table[1][1]
# line, = ax_graph.plot(x, A_init * x + B_init, lw=2)
# ax_graph.set_xlabel("x")
# ax_graph.set_ylabel("f(x) = A*x + B")
# ax_graph.grid(True)



# Lower left: Output from print statements
ax_print = fig.add_subplot(gs[3, 1])
ax_print.axis('off')


# Collect output lines for display and printing
output_lines = []
output_lines.append(f"Degrees of freedom: {dof}")
output_lines.append(f"Chi-square statistic: {chi2_stat:.4f}")
output_lines.append(f"P-value: {p:.4f}")
alpha = 0.05  # significance level
output_lines.append(f"Alpha (significance level): {alpha}\n")

if p > alpha:
    output_lines.append("P-value is greater than alpha.\n\nFail to reject the null hypothesis:\nthe variables are independent.")
else:
    output_lines.append("P-value is less than or equal to alpha.\n\nReject the null hypothesis:\nthe variables are not independent.")


output_text = '\n'.join(output_lines)
ax_print.text(0, 1, output_text, va='top', ha='left', fontsize=11)
ax_print.set_title('Test Output', fontsize=12)

# ---- UPDATE FUNCTION ----
def update(val):
    # Update table text from sliders
    for i, slider in enumerate(sliders):
        cell_text_refs[i].set_text(f"{slider.val:.2f}")

    # # Compute A and B from column sums
    # A = sliders[0].val + sliders[2].val  # sum of first column
    # B = sliders[1].val + sliders[3].val  # sum of second column

    # recalculate stats
    contingency_table_update = np.array([[sliders[0].val, sliders[1].val],
                  [sliders[2].val, sliders[3].val]])
    chi2_stat_update, p_update, dof_update, expected_update = chi2_contingency(contingency_table_update)

    # Update graph
    # line.set_ydata(A * x + B)
    # chiLine.set_ydata(chi2_dist.pdf(x, dof_update))
    # statLine.remove()   # erases the line from the axes
    # statLine_update = ax_graph.axvline(chi2_stat_update, color='red', linestyle='--', label=f'Statistic = {chi2_stat_update:.2f}')
    
    ax_graph.clear()
    x_update = np.linspace(0, max(chi2_stat_update * 2, 10), 500)
    chiLine_update, = ax_graph.plot(x, chi2_dist.pdf(x_update, dof_update), label=f'Chi2 PDF (df={dof_update})')
    statLine_update = ax_graph.axvline(chi2_stat_update, color='red', linestyle='--', label=f'Statistic = {chi2_stat_update:.2f}')
    ax_graph.fill_between(x_update, 0, chi2_dist.pdf(x_update, dof_update), where=(x >= chi2_stat_update), color='red', alpha=1)
    ax_graph.set_title('Chi-Square Distribution', fontsize=12)
    ax_graph.set_xlabel('Value')
    ax_graph.set_ylabel('Density')
    ax_graph.legend()
    fig.canvas.draw_idle()

    # update text
    ax_print.clear()
    ax_print.axis('off')
    output_lines = []
    output_lines.append(f"Degrees of freedom: {dof_update}")
    output_lines.append(f"Chi-square statistic: {chi2_stat_update:.4f}")
    output_lines.append(f"P-value: {p_update:.4f}")
    alpha = 0.05  # significance level
    output_lines.append(f"Alpha (significance level): {alpha}\n")

    if p_update > alpha:
        output_lines.append("P-value is greater than alpha.\n\nFail to reject the null hypothesis:\nthe variables are independent.")
    else:
        output_lines.append("P-value is less than or equal to alpha.\n\nReject the null hypothesis:\nthe variables are not independent.")


    output_text = '\n'.join(output_lines)
    ax_print.text(0, 1, output_text, va='top', ha='left', fontsize=11)
    ax_print.set_title('Test Output', fontsize=12)

# Connect sliders to update
for slider in sliders:
    slider.on_changed(update)

# ---- RESET BUTTON ----
# resetax = fig.add_subplot(gs[5, 0])
# resetax.axis('off')
button_ax = fig.add_axes([0.05, 0.1, 0.2, 0.05])
button = Button(button_ax, 'Reset', hovercolor='0.975')

def reset(event):
    for slider in sliders:
        slider.reset()

button.on_clicked(reset)

#plt.tight_layout()
plt.show()