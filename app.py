from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import plotly.io as pio
import plotly.graph_objects as go

import json

from utils.dash import DashboardColors, get_formatted_references
from utils.rag import DocStore, DocSearch

# Plotly template
with open("assets/template.json", "r") as f:
    plotly_template = json.load(f)
pio.templates["plotly_template"] = go.layout.Template(plotly_template)
pio.templates.default = "plotly_template"

# Dash params
DASHBOARD_NAME = "Chat with data"

# Dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# Custom dash app tab and logo
app.title = DASHBOARD_NAME
app._favicon = "logo.png"

# Server
server = app.server

# Header
title = html.H1(f"{DASHBOARD_NAME}", style={"color": DashboardColors.white})

header = html.Div(
    title,
    style={
        "padding": "1rem",
        "background-color": DashboardColors.black,
        "width": "100%",
    },
    id="header",
)

# Content
input_content = html.Div(
    [
        html.H3("Ask your data"),
        dbc.Textarea(id="text-input", placeholder="Write your question here"),
        html.Br(),
        dcc.Loading(
            type="circle",
            color=DashboardColors.black,
            children=dbc.Button(
                "Submit",
                id="button-submit",
                color="primary",
                className="me-1",
                n_clicks=0,
                disabled=False,
            ),
        ),
    ]
)

output_content = [
    html.Hr(),
    html.H3("Answer"),
    html.Div(id="answer"),
    html.Br(),
    html.H3("References"),
    html.Div(id="references"),
]


CONTENT_STYLE = {"margin-left": "1rem", "margin-right": "1rem", "padding": "1rem"}
content = html.Div(
    [
        html.Div(input_content, id="input"),
        html.Div(output_content, id="output", style={"visibility": "hidden"}),
    ],
    id="page-content",
    style=CONTENT_STYLE,
)

# Layout
app.layout = html.Div([header, content])

# Create search instance
search = DocSearch()

@app.callback(
    [
        Output("output", "style"),
        Output("answer", "children"),
        Output("references", "children"),
        Output("button-submit", "children"),
    ],
    inputs=[Input("button-submit", "n_clicks")],
    state=[State("text-input", "value")],
    prevent_initial_call=True,
)
def ask_question(n_clicks, question):
    if n_clicks:
        answer, references = search.ask(question, k=25, thresold=0.6)
        answer_output = dcc.Markdown(f"__Answer__: {answer}")
        references_output = get_formatted_references(references)
        return [{"visibility": "visible"}, answer_output, references_output, "Submit"]
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)