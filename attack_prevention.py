<<<<<<< HEAD
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import random
import matplotlib.pyplot as plt
import io

app = dash.Dash(__name__)

# Function to generate random data for graphs
def generate_random_data():
    categories = ['Requests', 'Attacks Detected', 'Vulnerabilities']
    data = {category: random.randint(1, 100) for category in categories}
    return data

app.layout = html.Div([
    html.H1("Security Analysis Dashboard"),
    html.Div(id='output-container-button'),
    dcc.Input(id='input-box', type='text', placeholder='Enter URL'),
    html.Button('Check', id='button'),
    html.Div(id='output-text'),
    html.Div(id='graphs-container', children=[
        dcc.Graph(id='requests-graph', config={'displayModeBar': False}),
        dcc.Graph(id='attacks-graph', config={'displayModeBar': False}),
        dcc.Graph(id='vulnerabilities-graph', config={'displayModeBar': False}),
    ], style={'display': 'flex'}),
    html.Div(id='ip-discover-map')
])

@app.callback(
    [Output('output-text', 'children'),
     Output('requests-graph', 'figure'),
     Output('attacks-graph', 'figure'),
     Output('vulnerabilities-graph', 'figure'),
     Output('ip-discover-map', 'children')],
    [Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')]
)
def update_output(n_clicks, value):
    if n_clicks is None:
        return '', {'data': []}, {'data': []}, {'data': []}, html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2687.1969349604373!2d2.352222715954948!3d48.85661430877223!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47e66e1f06e2b70f%3A0x40b82c3688c9460!2sEiffel%20Tower!5e0!3m2!1sen!2sfr!4v1622497890782!5m2!1sen!2sfr", width='100%', height='600')

    # Random analysis generation
    analysis = {
        'URL': value,
        'DDoS Attack': random.choice(['Yes', 'No']),
        'Phishing': random.choice(['Yes', 'No']),
        'Date/Time': '2024-05-30 13:45:00'  # Adding date and time of attacks
    }

    # Construction of data for graphs
    random_data = generate_random_data()

    # Construction of graphics
    graphs = []
    for category in random_data:
        plt.figure(figsize=(5, 3))
        plt.plot(category, random_data[category], marker='o')
        plt.title(category)
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.grid(True)
        plt.tight_layout()
        graph_bytes = io.BytesIO()
        plt.savefig(graph_bytes, format='png')
        plt.close()
        graph_bytes.seek(0)
        graph = {'data': [{'x': [category], 'y': [random_data[category]]}], 'layout': {'title': category, 'hovermode': 'closest'}}
        graphs.append(graph)

    # Construction of the analysis table
    table = html.Table([
        html.Tr([html.Th(key), html.Td(str(value))]) for key, value in analysis.items()
    ])

    # Construction of the Discover IP map
    ip_locations = [
        {'lat': 48.8566, 'lng': 2.3522, 'city': 'Paris', 'country': 'France', 'attack': random.choice([True, False]), 'ip': '192.168.1.1'},
        {'lat': 52.5200, 'lng': 13.4050, 'city': 'Berlin', 'country': 'Germany', 'attack': random.choice([True, False]), 'ip': '192.168.1.2'},
        {'lat': 41.9028, 'lng': 12.4964, 'city': 'Rome', 'country': 'Italy', 'attack': random.choice([True, False]), 'ip': '192.168.1.3'},
        {'lat': 51.5074, 'lng': 0.1278, 'city': 'London', 'country': 'United Kingdom', 'attack': random.choice([True, False]), 'ip': '10.8.0.234'},
        {'lat': 40.7128, 'lng': -74.0060, 'city': 'New York', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '10.10.8.98'},
        {'lat': 34.0522, 'lng': -118.2437, 'city': 'Los Angeles', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '196.168.0.34'},
        {'lat': 37.7749, 'lng': -122.4194, 'city': 'San Francisco', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '196.168.0.38'},
        {'lat': 35.6895, 'lng': 139.6917, 'city': 'Tokyo', 'country': 'Japan', 'attack': random.choice([True, False]), 'ip': '118.115.56.8'},
        {'lat': 31.2304, 'lng': 121.4737, 'city': 'Shanghai', 'country': 'China', 'attack': random.choice([True, False]), 'ip': '235.249.2.1'},
        {'lat': 37.5665, 'lng': 126.9780, 'city': 'Seoul', 'country': 'South Korea', 'attack': random.choice([True, False]), 'ip': '49.58.254.1'},
        {'lat': 38.7223, 'lng': -9.1393, 'city': 'Lisboa', 'country': 'Portugal', 'attack': random.choice([True, False]), 'ip': '192.168.1.4'},
        {'lat': 40.4168, 'lng': -3.7038, 'city': 'Madrid', 'country': 'Spain', 'attack': random.choice([True, False]), 'ip': '192.168.1.5'},
        {'lat': 55.7558, 'lng': 37.6176, 'city': 'Moscow', 'country': 'Russia', 'attack': random.choice([True, False]), 'ip': '192.168.1.6'},
        {'lat': 61.9241, 'lng': 25.7482, 'city': 'Helsinki', 'country': 'Finland', 'attack': random.choice([True, False]), 'ip': '192.168.1.7'},
        {'lat': 20.5937, 'lng': 78.9629, 'city': 'New Delhi', 'country': 'India', 'attack': random.choice([True, False]), 'ip': '192.168.1.8'}
    ]
    markers = []
    for location in ip_locations:
        if location['attack']:
            marker = {
                'position': {'lat': location['lat'], 'lng': location['lng']},
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'animation': 'BOUNCE',
                'infobox': f"<b>City:</b> {location['city']}<br><b>Country:</b> {location['country']}<br><b>Attacker's IP:</b> {location['ip']}"
            }
        else:
            marker = {
                'position': {'lat': location['lat'], 'lng': location['lng']},
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'animation': 'DROP',
                'infobox': f"<b>City:</b> {location['city']}<br><b>Country:</b> {location['country']}<br><b>Attacker's IP:</b> {location['ip']}"
            }
        markers.append(marker)

    ip_discover_map = html.Div([
        html.Iframe(
            srcDoc=f'''<html>
                <head>
                    <style>body {{ margin: 0; padding: 0; }}</style>
                </head>
                <body>
                    <div id="map" style="height: 600px; width: 100%;"></div>
                    <script>
                        function initMap() {{
                            var map = new google.maps.Map(document.getElementById('map'), {{
                                zoom: 3,
                                center: {{lat: 50, lng: 10}}
                            }});
                            var markers = {markers};
                            var infowindow = new google.maps.InfoWindow();
                            markers.forEach(function(marker) {{
                                var newMarker = new google.maps.Marker({{
                                    position: marker.position,
                                    map: map,
                                    icon: marker.icon,
                                    animation: google.maps.Animation.DROP
                                }});
                                google.maps.event.addListener(newMarker, 'click', function() {{
                                    infowindow.setContent(marker.infobox);
                                    infowindow.open(map, newMarker);
                                }});
                            }});
                        }}
                    </script>
                    <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
                </body>
            </html>'''.replace('YOUR_API_KEY', 'AIzaSyCSxZ8cNMClnXIl8tNxInhZftWLlUBHk94'),
            style={'border-width': '0', 'width': '100%', 'height': '600px'}
        )
    ])

    return table, graphs[0], graphs[1], graphs[2], ip_discover_map

if __name__ == '__main__':
    app.run_server(port=5000, debug=True)
=======
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import random
import matplotlib.pyplot as plt
import io

app = dash.Dash(__name__)

# Function to generate random data for graphs
def generate_random_data():
    categories = ['Requests', 'Attacks Detected', 'Vulnerabilities']
    data = {category: random.randint(1, 100) for category in categories}
    return data

app.layout = html.Div([
    html.H1("Security Analysis Dashboard"),
    html.Div(id='output-container-button'),
    dcc.Input(id='input-box', type='text', placeholder='Enter URL'),
    html.Button('Check', id='button'),
    html.Div(id='output-text'),
    html.Div(id='graphs-container', children=[
        dcc.Graph(id='requests-graph', config={'displayModeBar': False}),
        dcc.Graph(id='attacks-graph', config={'displayModeBar': False}),
        dcc.Graph(id='vulnerabilities-graph', config={'displayModeBar': False}),
    ], style={'display': 'flex'}),
    html.Div(id='ip-discover-map')
])

@app.callback(
    [Output('output-text', 'children'),
     Output('requests-graph', 'figure'),
     Output('attacks-graph', 'figure'),
     Output('vulnerabilities-graph', 'figure'),
     Output('ip-discover-map', 'children')],
    [Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')]
)
def update_output(n_clicks, value):
    if n_clicks is None:
        return '', {'data': []}, {'data': []}, {'data': []}, html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2687.1969349604373!2d2.352222715954948!3d48.85661430877223!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47e66e1f06e2b70f%3A0x40b82c3688c9460!2sEiffel%20Tower!5e0!3m2!1sen!2sfr!4v1622497890782!5m2!1sen!2sfr", width='100%', height='600')

    # Random analysis generation
    analysis = {
        'URL': value,
        'DDoS Attack': random.choice(['Yes', 'No']),
        'Phishing': random.choice(['Yes', 'No']),
        'Date/Time': '2024-05-30 13:45:00'  # Adding date and time of attacks
    }

    # Construction of data for graphs
    random_data = generate_random_data()

    # Construction of graphics
    graphs = []
    for category in random_data:
        plt.figure(figsize=(5, 3))
        plt.plot(category, random_data[category], marker='o')
        plt.title(category)
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.grid(True)
        plt.tight_layout()
        graph_bytes = io.BytesIO()
        plt.savefig(graph_bytes, format='png')
        plt.close()
        graph_bytes.seek(0)
        graph = {'data': [{'x': [category], 'y': [random_data[category]]}], 'layout': {'title': category, 'hovermode': 'closest'}}
        graphs.append(graph)

    # Construction of the analysis table
    table = html.Table([
        html.Tr([html.Th(key), html.Td(str(value))]) for key, value in analysis.items()
    ])

    # Construction of the Discover IP map
    ip_locations = [
        {'lat': 48.8566, 'lng': 2.3522, 'city': 'Paris', 'country': 'France', 'attack': random.choice([True, False]), 'ip': '192.168.1.1'},
        {'lat': 52.5200, 'lng': 13.4050, 'city': 'Berlin', 'country': 'Germany', 'attack': random.choice([True, False]), 'ip': '192.168.1.2'},
        {'lat': 41.9028, 'lng': 12.4964, 'city': 'Rome', 'country': 'Italy', 'attack': random.choice([True, False]), 'ip': '192.168.1.3'},
        {'lat': 51.5074, 'lng': 0.1278, 'city': 'London', 'country': 'United Kingdom', 'attack': random.choice([True, False]), 'ip': '10.8.0.234'},
        {'lat': 40.7128, 'lng': -74.0060, 'city': 'New York', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '10.10.8.98'},
        {'lat': 34.0522, 'lng': -118.2437, 'city': 'Los Angeles', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '196.168.0.34'},
        {'lat': 37.7749, 'lng': -122.4194, 'city': 'San Francisco', 'country': 'United States', 'attack': random.choice([True, False]), 'ip': '196.168.0.38'},
        {'lat': 35.6895, 'lng': 139.6917, 'city': 'Tokyo', 'country': 'Japan', 'attack': random.choice([True, False]), 'ip': '118.115.56.8'},
        {'lat': 31.2304, 'lng': 121.4737, 'city': 'Shanghai', 'country': 'China', 'attack': random.choice([True, False]), 'ip': '235.249.2.1'},
        {'lat': 37.5665, 'lng': 126.9780, 'city': 'Seoul', 'country': 'South Korea', 'attack': random.choice([True, False]), 'ip': '49.58.254.1'},
        {'lat': 38.7223, 'lng': -9.1393, 'city': 'Lisboa', 'country': 'Portugal', 'attack': random.choice([True, False]), 'ip': '192.168.1.4'},
        {'lat': 40.4168, 'lng': -3.7038, 'city': 'Madrid', 'country': 'Spain', 'attack': random.choice([True, False]), 'ip': '192.168.1.5'},
        {'lat': 55.7558, 'lng': 37.6176, 'city': 'Moscow', 'country': 'Russia', 'attack': random.choice([True, False]), 'ip': '192.168.1.6'},
        {'lat': 61.9241, 'lng': 25.7482, 'city': 'Helsinki', 'country': 'Finland', 'attack': random.choice([True, False]), 'ip': '192.168.1.7'},
        {'lat': 20.5937, 'lng': 78.9629, 'city': 'New Delhi', 'country': 'India', 'attack': random.choice([True, False]), 'ip': '192.168.1.8'}
    ]
    markers = []
    for location in ip_locations:
        if location['attack']:
            marker = {
                'position': {'lat': location['lat'], 'lng': location['lng']},
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'animation': 'BOUNCE',
                'infobox': f"<b>City:</b> {location['city']}<br><b>Country:</b> {location['country']}<br><b>Attacker's IP:</b> {location['ip']}"
            }
        else:
            marker = {
                'position': {'lat': location['lat'], 'lng': location['lng']},
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'animation': 'DROP',
                'infobox': f"<b>City:</b> {location['city']}<br><b>Country:</b> {location['country']}<br><b>Attacker's IP:</b> {location['ip']}"
            }
        markers.append(marker)

    ip_discover_map = html.Div([
        html.Iframe(
            srcDoc=f'''<html>
                <head>
                    <style>body {{ margin: 0; padding: 0; }}</style>
                </head>
                <body>
                    <div id="map" style="height: 600px; width: 100%;"></div>
                    <script>
                        function initMap() {{
                            var map = new google.maps.Map(document.getElementById('map'), {{
                                zoom: 3,
                                center: {{lat: 50, lng: 10}}
                            }});
                            var markers = {markers};
                            var infowindow = new google.maps.InfoWindow();
                            markers.forEach(function(marker) {{
                                var newMarker = new google.maps.Marker({{
                                    position: marker.position,
                                    map: map,
                                    icon: marker.icon,
                                    animation: google.maps.Animation.DROP
                                }});
                                google.maps.event.addListener(newMarker, 'click', function() {{
                                    infowindow.setContent(marker.infobox);
                                    infowindow.open(map, newMarker);
                                }});
                            }});
                        }}
                    </script>
                    <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
                </body>
            </html>'''.replace('YOUR_API_KEY', 'YOUR_API_KEY'),
            style={'border-width': '0', 'width': '100%', 'height': '600px'}
        )
    ])

    return table, graphs[0], graphs[1], graphs[2], ip_discover_map

if __name__ == '__main__':
    app.run_server(port=5000, debug=True)
>>>>>>> 251b21666802cc6ece58ddad28c7650ebf4a7fd9
