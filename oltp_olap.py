# OLTP (Online Transaction Processing) vs OLAP (Online Analytical Processing)
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Function to generate OLTP data randomly
def generate_oltp_data():
    products = ['Gas Turbine', 'Steam Turbine', 
                'Generator', 'Transmitter', 
                'Control Valve', 'Pump', 
                'Compressor', 'Heat Exchanger', 
                'Boiler', 'Turbine Generator Set']
    quantity = np.random.randint(5, 20, size=len(products))
    unit_price = np.random.randint(1000, 500000, size=len(products))
    data = {'Product': products, 'Quantity': quantity, 'Unit_Price': unit_price}
    return pd.DataFrame(data)

# Function to generate OLAP data randomly
def generate_olap_data(df_oltp):
    total_sales = df_oltp['Quantity'] * df_oltp['Unit_Price']
    df_oltp['Total_Sales'] = total_sales
    return df_oltp

# Initialize the Dash application
app = dash.Dash(__name__)

# Dashboard layout
app.layout = html.Div([
    html.H1("Siemens Energy - Sales Dashboard"),
    
    html.Div([
        html.Label('Select a Product:'),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': prod, 'value': prod} for prod in generate_oltp_data()['Product']],
            value='Gas Turbine'
        ),
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='oltp-graph')
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        html.Div([
            dcc.Graph(id='olap-graph')
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'})
    ]),
    
    html.Div([
        dcc.Graph(id='combined-graph')
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update OLTP and OLAP graphs
@app.callback(
    [Output('oltp-graph', 'figure'),
     Output('olap-graph', 'figure'),
     Output('combined-graph', 'figure')],
    [Input('product-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graphs(selected_product, n_intervals):
    # Generate OLTP data randomly
    df_oltp = generate_oltp_data()
    
    # Generate OLAP data randomly
    df_olap = generate_olap_data(df_oltp.copy())
    
    # Increase OLTP sales by 2% every 5 seconds
    if n_intervals > 0:
        for i in range(len(df_oltp)):
            df_oltp.at[i, 'Quantity'] = float(df_oltp.at[i, 'Quantity'] * np.random.uniform(1.01, 1.03))
    
    # Filter data for selected product
    filtered_df_oltp = df_oltp[df_oltp['Product'] == selected_product]
    
    # OLTP bar chart
    oltp_fig = {
        'data': [
            go.Bar(
                x=filtered_df_oltp['Product'],
                y=filtered_df_oltp['Quantity'],
                marker=dict(color='blue'),
                name='Quantity'
            )
        ],
        'layout': go.Layout(
            title='Sales by Product (OLTP(Online Transaction Processing))',
            xaxis={'title': 'Product'},
            yaxis={'title': 'Quantity'}
        )
    }
    
    # OLAP bar chart
    olap_fig = {
        'data': [
            go.Bar(
                x=df_olap['Product'],
                y=df_olap['Total_Sales'],
                marker=dict(color='red'),
                name='Total_Sales'
            )
        ],
        'layout': go.Layout(
            title='Sales by Product (OLAP(Online Analytical Processing))',
            xaxis={'title': 'Product'},
            yaxis={'title': 'Total Sales'}
        )
    }
    
    # OLTP line chart
    oltp_line_fig = go.Scatter(
        x=df_oltp['Product'],
        y=df_oltp['Quantity'],
        mode='lines+markers',
        marker=dict(color='blue'),
        name='OLTP'
    )
    
    # OLAP line chart
    olap_line_fig = go.Scatter(
        x=df_olap['Product'],
        y=df_olap['Total_Sales'],
        mode='lines+markers',
        marker=dict(color='red'),
        name='OLAP'
    )
    
    # Combined line chart
    combined_fig = {
        'data': [oltp_line_fig, olap_line_fig],
        'layout': go.Layout(
            title='Sales by Product (OLTP(Online Transaction Processing) vs OLAP(Online Analytical Processing))',
            xaxis={'title': 'Product'},
            yaxis={'title': 'Sales'}
        )
    }
    
    return oltp_fig, olap_fig, combined_fig

if __name__ == '__main__':
    app.run_server(debug=True)
    