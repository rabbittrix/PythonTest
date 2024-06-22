import openai
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

# Configure OpenAI API key
openai.api_key = "sk-"  # Replace with your OpenAI API key

# Function to generate SEO content used GPT
def generate_seo_content(keywords, tone, length):
    prompt = f"Write a SEO optmized article about {keywords} in a {tone} tone. The article should be {length} words long."
    response = openai.Completion.create(
        model="gpt-4-turbo",
        prompt=prompt,
        max_tokens=length,
    )
    return response.choices[0].text

# Configure Dash app
app= dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("SEO Content Generator with LLM"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Keywords:"),
            dcc.Input(id="keywords", type="text", placeholder="Enter keywords...", className="form-control")
        ], width=6),
        dbc.Col([
            dbc.Label("Tone of the Article:"),
            dcc.Input(id="tone", type="text", placeholder="Enter the desired tone...", className="form-control")
        ], width=6)
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Length of the Article (number of words):"),
            dcc.Input(id="length", type="number", placeholder="Enter the length...", className="form-control")
        ], width=6)
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Button("Generate Content", id="generate-button", color="primary", className="me-2")
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            html.H4("Generated Content:"),
            html.Div(id="generated-content", className="border p-3")
        ])
    ])
])

@app.callback(
    Output("generated-content", "children"),
    [Input("generate-button", "n_clicks")],
    [State("keywords", "value"), State("tone", "value"), State("length", "value")]
)

def update_output(n_clicks, keywords, tone, length):
    if n_clicks is None or keywords is None or tone is None or length is None:
        return ""
    content = generate_seo_content(keywords, tone, length)
    return content

if __name__ == "__main__":
    app.run_server(debug=True)