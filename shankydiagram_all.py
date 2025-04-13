import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Load data
data_90_95 = pd.read_csv('/Users/z5459080/Desktop/Papar_1/scripts/Transitions_1990_1995.csv')
data_95_00 = pd.read_csv('/Users/z5459080/Desktop/Papar_1/scripts/Transitions_1995_2000.csv')

# Function to process transition data
def process_transition_data(data):
    adjacency_matrix = data.iloc[:, 3:]
    adjacency_matrix = adjacency_matrix.drop(adjacency_matrix.index[6]).drop(adjacency_matrix.columns[6], axis=1)
    matrix = np.array(adjacency_matrix, dtype=float)
    row_sums = matrix.sum(axis=1, keepdims=True)
    percentage_matrix = (matrix / row_sums) * 100
    return percentage_matrix

# Process both transition matrices
percentage_matrix_90_95 = process_transition_data(data_90_95)
percentage_matrix_95_00 = process_transition_data(data_95_00)

# Define labels
labels_order = ['1.Compact\nHighrise', '2.Compat\nMidrise', '3.Compact\nLowrise', '4.Open\nHighrise', '5.Open\nMidrise',
                '6.Open Lowrise', '8.Large Lowrise', '9.Sparsely Built', '10. Heavy\nIndustry', 'A. Dense Tree', 
                'B. Scattered\nTree', 'C.Bush\nScrub', 'D.Low Plants', 'E.Bare\nRock\nor Paved', 'F. Bare\nSoil\n or Sand', 
                'G.Water']

# Convert matrices to DataFrames
matrix_df_90_95 = pd.DataFrame(percentage_matrix_90_95, index=labels_order, columns=labels_order)
matrix_df_95_00 = pd.DataFrame(percentage_matrix_95_00, index=labels_order, columns=labels_order)

# Filter significant transitions
significant_df_90_95 = matrix_df_90_95[matrix_df_90_95 > 10].fillna(0)
significant_df_95_00 = matrix_df_95_00[matrix_df_95_00 > 10].fillna(0)

# Prepare data for Sankey diagram
labels = labels_order + labels_order + labels_order
source = []
target = []
value = []
link_colors = []

colors = [
    '#8C0000', '#D10000', '#FF0000', '#BF4D00', '#FF6600', '#FF9955', '#BCBCBC', '#FFCCAA',
    '#555555', '#006A00', '#00AA00', '#648525', '#B9DB79', '#000000', '#FBF7AE', '#6A6ACD'
]

# Function to convert hex color to rgba
def hex_to_rgba(hex_color, alpha=0.6):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return f'rgba({r},{g},{b},{alpha})'

# Prepare the link data and colors for 1990-1995
for i, col in enumerate(significant_df_90_95.columns):
    for j, val in enumerate(significant_df_90_95[col]):
        if val > 0:
            source.append(labels_order.index(col))
            target.append(labels_order.index(significant_df_90_95.index[j]) + len(labels_order))
            value.append(val)
            link_colors.append(hex_to_rgba(colors[j]))

# Prepare the link data and colors for 1995-2000
for i, col in enumerate(significant_df_95_00.columns):
    for j, val in enumerate(significant_df_95_00[col]):
        if val > 0:
            source.append(labels_order.index(col) + len(labels_order))
            target.append(labels_order.index(significant_df_95_00.index[j]) + 2 * len(labels_order))
            value.append(val)
            link_colors.append(hex_to_rgba(colors[j]))

# Create the node colors list with correct order
node_colors = colors + colors + colors

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=40,
        line=dict(color="black", width=0.9),
        label=labels,
        color=node_colors
    ),
    link=dict(
        arrowlen=15,
        source=source,
        target=target,
        value=value,
        color=link_colors
    )
)])

# Update layout
fig.update_layout(title_text="Class Transition Sankey Diagram (1990-1995 and 1995-2000)", font_size=10, width=800, height=1200)
# fig.write_html("class_transition_sankey_diagram.html")
fig.write_image("class_transition_sankey_diagram.png")
