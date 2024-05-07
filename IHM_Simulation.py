import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import datetime

# Mock data
mock_production_data = [
    {"batch_id": 1, "chocolate_type": "Milk Chocolate", "quantity": 100, "material_used": 200, "waste": 10},
    {"batch_id": 2, "chocolate_type": "Dark Chocolate", "quantity": 150, "material_used": 250, "waste": 15},
    {"batch_id": 3, "chocolate_type": "White Chocolate", "quantity": 120, "material_used": 220, "waste": 12}
]

# Create a DataFrame from mock data
df_production = pd.DataFrame(mock_production_data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Chocolate Production Simulator"),
    html.Div(id='batch-info'),
    html.Button('Refresh', id='refresh-button', n_clicks=0),
    html.Div(id='batch-list-control'),
    dcc.Input(id='rejection-reason', type='text', placeholder='Rejection Reason'),
    html.Button('Reject', id='reject-button', n_clicks=0),
])

# Define callback to update batch information when refresh button is clicked
@app.callback(
    [Output('batch-info', 'children'), Output('batch-list-control', 'children')],
    [Input('refresh-button', 'n_clicks'), Input('reject-button', 'n_clicks')],
    [State('rejection-reason', 'value')]
)
def update_batch_list_and_control_production(refresh_clicks, reject_clicks, rejection_reason):
    if dash.callback_context.triggered[0]['prop_id'] == 'reject-button.n_clicks':
        if rejection_reason:
            # Reject the batch
            return f"Batch rejected due to: {rejection_reason}", []
        else:
            return "", []

    # Get current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a list of batch statuses
    batch_statuses = []
    for index, row in df_production.iterrows():
        batch_id = row['batch_id']
        chocolate_type = row['chocolate_type']
        quantity = row['quantity']
        material_used = row['material_used']
        waste = row['waste']
        batch_status = html.Div([
            html.P(f"Batch: {batch_id} - Type: {chocolate_type} - Quantity: {quantity}"),
            html.P(f"Material Used: {material_used} - Waste: {waste}"),
            html.P(f"Status: In Production"),
            html.P(f"Last Updated: {current_time}")
        ], style={'background-color': 'lightgreen'})
        batch_statuses.append(batch_status)

    return "", batch_statuses

if __name__ == '__main__':
    app.run_server(debug=True)
