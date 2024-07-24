import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import datetime

# Start the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
def generate_random_data():
    return {
        "timestamp": datetime.datetime.now(),
        "NRF": random.randint(100, 1000),
        "NSSF": random.randint(50, 500),
        "NEF": random.randint(200, 1200),
        "APIGW": random.randint(300, 800),
    }
    
    # Create a Dash layout
app.layout = html.Div(
    style={"backgroundColor": '#f9f9f9', 'font-family': 'Arial, sans-serif'},
    children=[
        html.H1("5G Network Functions Dashboard", 
                style={'textAlign': 'center', 'color': '#0073e6'}
                ),
        html.Div(
            children='Monitoring the 5G Network Functions NRF, NSSF, NEF, and APIGW',
            style={'textAlign': 'center', 'color': '#4d4d4d'}
        ),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ]
)

# Create a callback to update the graph every 1 second
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)

def update_graph_live(n):
    data = generate_random_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[data["timestamp"]],
        y=[data["NRF"]],
        mode='lines+markers',
        name='NRF',
        line=dict(color='blue')
    ))	
    
    fig.add_trace(go.Scatter(
        x=[data["timestamp"]],
        y=[data["NSSF"]],
        mode='lines+markers',
        name='NSSF',
        line=dict(color='green')
    ))
    
    fig.add_trace(go.Scatter(
        x=[data["timestamp"]],
        y=[data["NEF"]],
        mode='lines+markers',
        name='NEF',
        line=dict(color='orange')
    ))
    
    fig.add_trace(go.Scatter(
        x=[data["timestamp"]],
        y=[data["APIGW"]],
        mode='lines+markers',
        name='APIGW',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title='Real-Time Monitoring of 5G Functions',
        xaxis_title='Timestamp',
        yaxis_title='Value',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)