import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from pgmpy.estimators import HillClimbSearch, BicScore
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Generate a dataset simulating causal events
np.random.seed(42)
data = pd.DataFrame({
    'event_A': np.random.binomial(1, 0.5, 1000),
    'event_B': np.random.binomial(1, 0.5, 1000),
    'event_C': np.random.binomial(1, 0.5, 1000)
})

# Introduce causality
data['event_B'] = (data['event_A'] * 0.8 + np.random.binomial(1, 0.2, 1000)).astype(int)
data['event_C'] = (data['event_B'] * 0.5 + data['event_A'] * 0.3 + np.random.binomial(1, 0.2, 1000)).astype(int)

# Causation structure using Hill Climb Search algorithm
hc = HillClimbSearch(data)
best_model = hc.estimate(scoring_method=BicScore(data))

# Create a visualization with plotly
pos = nx.spring_layout(best_model, seed=42)
edge_x = []
edge_y = []

for edge in best_model.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []
for node in best_model.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[str(node) for node in best_model.nodes()],
    textposition='top center',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2)
)

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Causality Analysis',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper"
                    )],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Launch Dash app
app = Dash(__name__)

# Application layout
app.layout = html.Div([
    html.H1("Causality Analysis"),
    dcc.Graph(id='causal-graph', figure=fig),
    dcc.Dropdown(
        id='event-dropdown',
        options=[
            {'label': 'Event A', 'value': 'event_A'},
            {'label': 'Event B', 'value': 'event_B'},
            {'label': 'Event C', 'value': 'event_C'}
        ],
        value='event_A'
    ),
    dcc.Graph(id='event-graph')
])

# Callback to update the event graph
@app.callback(
    Output('event-graph', 'figure'),
    [Input('event-dropdown', 'value')]
)
def update_event_graph(event):
    fig = px.histogram(data, x=event, title=f"Distribution of {event}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
