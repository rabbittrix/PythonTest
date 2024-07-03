import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Criando um DataFrame fictício
np.random.seed(42)
data = {
    'Feature 1': np.random.randn(100),
    'Feature 2': np.random.randn(100),
    'Feature 3': np.random.randn(100),
    'target': np.random.choice([0, 1], 100),
    'Group': np.random.choice(['A', 'B', 'C'], size=100)
}
df = pd.DataFrame(data)

def detect_bias(df):
    """Detect views in relation to the group"""
    bias_report = {}
    for group in df['Group'].unique():
        group_df = df[df['Group'] == group]
        bias_report[group] = group_df['target'].mean()
    return bias_report

def mitigate_bias(df):
    """Mitigate bias by changing the target"""
    target_mean = df['target'].mean()
    new_df = df.copy()
    for group in df['Group'].unique():
        group_data = df[df['Group'] == group]
        group_mean = group_data['target'].mean()
        adjustment = target_mean - group_mean
        new_df.loc[new_df['Group'] == group, 'target'] = group_data['target'] + adjustment
    return new_df

# Start the app layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Global Regulations for AI Bias'),
    dcc.Graph(id='bias_graph'),
    html.Button('Mitigate Bias', id='mitigate-bias', n_clicks=0),
    html.Div(id='bias-report')
])

@app.callback(
    Output('bias_graph', 'figure'),
    Output('bias-report', 'children'),
    Input('mitigate-bias', 'n_clicks')
)

def update_bias(n_clicks):
    global df
    if n_clicks > 0:
        df = mitigate_bias(df)
        
    bias_report = detect_bias(df)
    fig = px.histogram(df, x='target', histfunc='avg', title='Average Target by Group', color='Group')
    
    report = [html.H3('Bias Report')] + [html.P(f'{group}: {round(bias, 2)}') for group, bias in bias_report.items()]
    
    return fig, report

if __name__ == '__main__':
    app.run_server(debug=True)
