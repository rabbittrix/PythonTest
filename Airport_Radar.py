import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#list of airports with radar data and their respective ICAO codes
airports = [
    {'label': 'Lisbon Airport (LPPT/LIS)', 'value': 'LPPT'},
    {'label': 'Madrid Airport (LEMD/MAD)', 'value': 'LEMD'},
    {'label': 'Paris Charles de Gaulle Airport (LFPG/CDG)', 'value': 'LFPG'},
    {'label': 'Berlin Brandenburg Airport (EDDB/BER)', 'value': 'EDDB'},
    {'label': 'Rome Fiumicino Airport (LIRF/FCO)', 'value': 'LIRF'},
    {'label': 'Amsterdam Airport Schiphol (EHAM/AMS)', 'value': 'EHAM'},
    {'label': 'Vienna International Airport (LOWW/VIE)', 'value': 'LOWW'},
    {'label': 'Brussels Airport (EBBR/BRU)', 'value': 'EBBR'},
    {'label': 'Copenhagen Airport (EKCH/CPH)', 'value': 'EKCH'},
    {'label': 'Dublin Airport (EIDW/DUB)', 'value': 'EIDW'},
]

mock_audio_urls = {
    'LPPT': 'assets/AudioAeroporto.mp3',
    'LEMD': 'assets/AudioAeroporto.mp3',
    'LFPG': 'assets/AudioAeroporto.mp3',
    'EDDB': 'assets/AudioAeroporto.mp3',
    'LIRF': 'assets/AudioAeroporto.mp3',
    'EHAM': 'assets/AudioAeroporto.mp3',
    'LOWW': 'assets/AudioAeroporto.mp3',
    'EBBR': 'assets/AudioAeroporto.mp3',
    'EKCH': 'assets/AudioAeroporto.mp3',
    'EIDW': 'assets/AudioAeroporto.mp3',
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Airport Radar Livestream with ATC Communications", className="text-center")
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='airport-dropdown',
                        options=airports,
                        value='LPPT',  # Default to Lisbon Airport
                        className='mb-4',
                    ),
                    width=6
                ),
            ],
            justify='center'
        ),
        dbc.Row(
            [
                dbc.Col(html.Img(id='radar-image', src='', style={'width': '100%', 'height': '500px'}), width=12),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Audio(id='atc-audio', controls=True, style={'width': '100%'}), width=12),
            ],
            className='mt-4'
        )
    ],
    fluid=True,
    className="p-4 bg-dark text-white"
)
       
@app.callback(
    Output('radar-image', 'src'),
    Output('atc-audio', 'src'),
    Input('airport-dropdown', 'value')
)

def update_content(airport_code):
    if airport_code not in mock_audio_urls:
        airport_code = 'LPPT'  # Default to Lisbon Airport

    radar_image_url = f"/assets/{airport_code}.png"
    atc_stream_url = mock_audio_urls.get(airport_code, 'assets/AudioAeroporto.mp3')

    return radar_image_url, atc_stream_url
    
if __name__ == '__main__':
    app.run_server(debug=True)