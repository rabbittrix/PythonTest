import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import pdfplumber
from docx import Document
from langdetect import detect
from textblob import TextBlob
import base64
import io
import json
import csv

# Inicialização do app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Layout do app
app.layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Upload File", href="#")),
                dbc.NavItem(dbc.NavLink("Download File", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More tools", header=True),
                        dbc.DropdownMenuItem("Settings"),
                        dbc.DropdownMenuItem("Help"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ],
            brand="Editor e Criador de Contratos",
            brand_href="#",
            color="orange",
            dark=True,
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Div(
                                        ['Drag and Drop or ', html.A('Select Files')]
                                    ),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                    multiple=False
                                ),
                                html.Div(id='output-file-upload'),
                                html.Div(id='language-detection'),
                                html.Div(id='text-correction'),
                            ],
                            width=3,
                            style={'backgroundColor': '#2c2c2c'}
                        ),
                        dbc.Col(
                            [
                                dcc.Textarea(
                                    id='text-editor',
                                    style={'width': '100%', 'height': '90vh', 'backgroundColor': '#333', 'color': 'white'},
                                    value=''
                                )
                            ],
                            width=9,
                        ),
                    ]
                ),
            ],
            fluid=True,
        ),
    ]
)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df.to_csv(index=False)
        elif 'json' in filename:
            data = json.load(io.StringIO(decoded.decode('utf-8')))
            return json.dumps(data, indent=2)
        elif 'txt' in filename:
            return decoded.decode('utf-8')
        elif 'docx' in filename:
            doc = Document(io.BytesIO(decoded))
            return '\n'.join([para.text for para in doc.paragraphs])
        elif 'pdf' in filename:
            pdf = pdfplumber.open(io.BytesIO(decoded))
            return '\n'.join([page.extract_text() for page in pdf.pages])
    except Exception as e:
        return str(e)

@app.callback(
    Output('text-editor', 'value'),
    Output('language-detection', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return '', ''
    
    text = parse_contents(contents, filename)
    try:
        lang = detect(text)
    except:
        lang = "Could not detect language"
    return text, f"Detected language: {lang}"

@app.callback(
    Output('text-correction', 'children'),
    Input('text-editor', 'value')
)
def correct_text(text):
    if text:
        blob = TextBlob(text)
        corrected_text = str(blob.correct())
        return f"Corrected text: {corrected_text[:200]}..."  # Displaying only a snippet for demo
    return "No text to correct"

if __name__ == '__main__':
    app.run_server(debug=True)
