import dash
import dash_bootstrap_components as dbc
from dash import html
from dash_extensions.enrich import Dash, Output, Input, State
import dash_daq as daq

# Create example app NFT staking
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# CSS Customization for the theme dark Orange e Gyroscope Effect
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #333;
                color: #FFA500;
            }
            .card {
                background-color: #444;
                border: 1px solid #FFA500;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: transform 0.1s ease-in-out;
                transform: perspective(600px) rotateY(0deg) rotateX(0deg);
            }
            .card:hover {
                transform: perspective(600px) rotateY(20deg) rotateX(20deg);
            }
            .card img {
                width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
# Create layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("NFT Staking Dashboard", className="text-center my-4")),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardImg(src=f"/assets/nft{i}.png", top=True),
                className="mb-4 card",
            ) for i in range(1, 9)
        ], width=3) for _ in range(2)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                daq.ToggleSwitch(
                    id='staking-toggle',
                    label='Stake NFTs',
                    color='#FFA500',
                    labelPosition='top'
                ),
                html.Div(id='staking-status', className='mt-2')
            ])
        ], width=12, className="text-center")
    ])
], fluid=True)
    
# Callback to interact
@app.callback(
    Output("staking-status", "children"),
    Input("staking-toggle", "value")
)

def staking_status(value):
    if value:
        return "Staking NFTs Activated"
    else:
        return "Staking NFTs Deactivated"
        
# Execute the app
if __name__ == "__main__":
    app.run_server(port=8080, debug=True)
