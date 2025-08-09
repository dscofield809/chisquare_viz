
# Interactive Plotly dashboard for Chi-square test
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency, chi2
import ipywidgets as widgets

row_labels = ['Male', 'Female']
col_labels = ['Option A', 'Option B']

def update_dashboard(male_a, male_b, female_a, female_b):
    observed_data = np.array([
        [male_a, male_b],
        [female_a, female_b]
    ])
    chi2_stat, p_value, dof, expected = chi2_contingency(observed_data)
    alpha = 0.05
    result_text = (
        f"Degrees of freedom: {dof}<br>"
        f"Chi-square statistic: {chi2_stat:.2f}<br>"
        f"P-value: {p_value:.3f}<br>"
    )
    if p_value < alpha:
        result_text += "<br>p-value < alpha: <b>Reject the null hypothesis.</b><br>There is a significant association between the two categorical variables."
    else:
        result_text += "<br>p-value > alpha: <b>Fail to reject the null hypothesis.</b><br>There is no significant association between the two categorical variables."

    # Create subplots: 2 rows, 2 columns
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "table"}, {"type": "xy"}],
               [{"type": "domain"}, {"type": "xy"}]],
        subplot_titles=("Observed Contingency Table", "Chi-square Distribution", "", "Test Results")
    )

    # Table (upper left)
    fig.add_trace(
        go.Table(
            header=dict(values=["", *col_labels], align='center'),
            cells=dict(values=[[row_labels[0], row_labels[1]],
                              [male_a, female_a],
                              [male_b, female_b]], align='center')
        ),
        row=1, col=1
    )

    # Chi-square distribution (upper right)
    x = np.linspace(0, max(chi2_stat + 10, 20), 500)
    y = chi2.pdf(x, dof)
    fig.add_trace(
        go.Scatter(x=x, y=y, mode='lines', name=f'dof={dof}'),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=[chi2_stat], y=[chi2.pdf(chi2_stat, dof)], mode='markers', marker=dict(color='red', size=10), name='Chi2 stat'),
        row=1, col=2
    )

    # Results (lower right)
    fig.add_trace(
        go.Scatter(
            x=[0], y=[0], text=[result_text], mode='text', showlegend=False
        ),
        row=2, col=2
    )

    fig.update_layout(height=700, width=1000, showlegend=False)
    fig.update_xaxes(title_text="Chi-square value", row=1, col=2)
    fig.update_yaxes(title_text="Probability Density", row=1, col=2)
    fig.show()

# Sliders for each cell
male_a_slider = widgets.IntSlider(value=50, min=10, max=100, step=1, description='Male Option A')
male_b_slider = widgets.IntSlider(value=30, min=10, max=100, step=1, description='Male Option B')
female_a_slider = widgets.IntSlider(value=40, min=10, max=100, step=1, description='Female Option A')
female_b_slider = widgets.IntSlider(value=60, min=10, max=100, step=1, description='Female Option B')

ui = widgets.VBox([male_a_slider, male_b_slider, female_a_slider, female_b_slider])
out = widgets.interactive_output(update_dashboard, {
    'male_a': male_a_slider,
    'male_b': male_b_slider,
    'female_a': female_a_slider,
    'female_b': female_b_slider
})

display(ui, out)