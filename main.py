# Interactive Plotly dashboard for Chi-square test
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# Example 2x2 contingency table
#        Success  Failure
# Group1   20       15
# Group2   30       25
table = np.array([[50, 30],
                  [40, 60]])

chi2_stat, p, dof, expected = chi2_contingency(table)

# Collect output lines for display and printing
output_lines = []
output_lines.append(f"Degrees of freedom: {dof}")
output_lines.append(f"Chi-square statistic: {chi2_stat:.4f}")
output_lines.append(f"P-value: {p:.4f}")
alpha = 0.05  # significance level
output_lines.append(f"Alpha (significance level): {alpha}")

if p > alpha:
    output_lines.append("P-value is greater than alpha. Fail to reject the null hypothesis: the variables are independent.")
else:
    output_lines.append("P-value is less than or equal to alpha. Reject the null hypothesis: the variables are not independent.")

for line in output_lines:
    print(line)

# Matplotlib visualization
fig, axs = plt.subplots(2, 2, figsize=(10, 8), gridspec_kw={'wspace': 0.2, 'hspace': 0.3})
fig.suptitle('Chi-Squared Test Visualization', fontsize=16)

# Upper left: Contingency table
axs[0, 0].axis('off')
table_text = [[str(cell) for cell in row] for row in table]
row_labels = ['Group 1', 'Group 2']
col_labels = ['Success', 'Failure']
table_obj = axs[0, 0].table(cellText=table_text,
                            rowLabels=row_labels,
                            colLabels=col_labels,
                            loc='center',
                            cellLoc='center')
table_obj.scale(1, 1.75)
axs[0, 0].set_title('Contingency Table', fontsize=12)

# Upper right: Chi-square distribution
from scipy.stats import chi2 as chi2_dist
x = np.linspace(0, max(chi2_stat * 2, 10), 500)
axs[0, 1].plot(x, chi2_dist.pdf(x, dof), label=f'Chi2 PDF (df={dof})')
axs[0, 1].axvline(chi2_stat, color='red', linestyle='--', label=f'Statistic = {chi2_stat:.2f}')
axs[0, 1].fill_between(x, 0, chi2_dist.pdf(x, dof), where=(x >= chi2_stat), color='red', alpha=0.2)
axs[0, 1].set_title('Chi-Square Distribution', fontsize=12)
axs[0, 1].set_xlabel('Value')
axs[0, 1].set_ylabel('Density')
axs[0, 1].legend()

# Lower left: Output from print statements
axs[1, 0].axis('off')
output_text = '\n'.join(output_lines)
axs[1, 0].text(0, 1, output_text, va='top', ha='left', fontsize=11)
axs[1, 0].set_title('Test Output', fontsize=12)

# Lower right: Empty
axs[1, 1].axis('off')

#plt.tight_layout(rect=[0.01, 0.05, 0.99, 0.93])
plt.savefig('chi_square_test_results.png')
plt.show()