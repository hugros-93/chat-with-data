from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import plotly.io as pio
import plotly.graph_objects as go

import os
import json
import base64

from utils.dash import (
    DashboardColors,
    get_formatted_references,
    get_formatted_data,
    get_header_buttons,
)
from utils.rag import DocStore

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

# Langchain Doc Store
store = DocStore()

# Header
title = html.H1(f"{DASHBOARD_NAME}", style={"color": DashboardColors.white})

header = html.Div(
    [
        dbc.Stack(
            [title, get_header_buttons()],
            direction="horizontal",
        )
    ],
    style={
        "padding": "1rem",
        "background-color": DashboardColors.black,
        "width": "100%",
    },
    id="header",
)

# Content
data_content = html.Div(id="data-content")

input_content = html.Div(
    [
        html.Hr(),
        html.H3("Question"),
        dbc.Textarea(id="text-input", placeholder="Write your question here"),
        html.Br(),
        dbc.Button(
            "Submit",
            id="button-submit",
            color="primary",
            className="me-1",
            n_clicks=0,
            disabled=False,
        ),
    ]
)

output_content = dcc.Loading(
    type="circle",
    color=DashboardColors.black,
    children=[
        html.Hr(),
        html.H3("Answer"),
        html.Div(id="answer"),
        html.Hr(),
        html.H3("References"),
        dcc.Markdown("_List of the top 5 references found in the data._"),
        html.Div(id="references"),
    ],
)


CONTENT_STYLE = {"margin-left": "1rem", "margin-right": "1rem", "padding": "1rem"}
content = html.Div(
    [
        html.Div(data_content),
        html.Div(input_content, id="input"),
        html.Div(output_content, id="output", style={"visibility": "hidden"}),
    ],
    id="page-content",
    style=CONTENT_STYLE,
)

# Layout
app.layout = html.Div([header, content])


# Callback load data
@app.callback(
    [
        Output("button-load-data", "value"),
        Output("output-load-data", "children"),
        Output("data-content", "children"),
    ],
    Input("upload-file", "contents"),
    Input("upload-file", "filename"),
)
def load_data(contents, filenames):
    if contents == None:
        print("> No data to load!")
        data_content = [html.H3("Data"), dcc.Markdown(f"_Please load data first..._")]
        return ["Load data", False, data_content]
    else:
        # Clean input files
        for filename in os.listdir("data/"):
            file_path = os.path.join("data/", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # Load files
        for i, filename in enumerate(filenames):
            _, content_string = contents[i].split(",")
            decoded = base64.b64decode(content_string)
            if ".pdf" not in filename:
                print(f"> {filename} is not a .pdf")
            else:
                # Save data
                print(f"> Saving {filename}")
                with open(f"data/{filename}", "wb") as f:
                    f.write(decoded)
        # Create store
        print(f"> Creating store")
        store.load()
        store.split()
        store.create_vector_db()
        # Load data
        print(f"> Loading data")
        db_summary = store.get_db_summary()
        data_content = [
            html.H3("Data"),
            dcc.Markdown(f"_Total of splits: {db_summary['number_splits']}_"),
            get_formatted_data(db_summary["sources"]),
        ]
        return ["Load data", True, data_content]


# Callback submit question
@app.callback(
    [
        Output("output", "style"),
        Output("answer", "children"),
        Output("references", "children"),
    ],
    inputs=[Input("button-submit", "n_clicks")],
    state=[State("text-input", "value")],
    prevent_initial_call=True,
)
def ask_question(n_clicks, question):
    if n_clicks:
        answer, references = store.ask(question, k=15, thresold=0.6)
        answer_output = dcc.Markdown(f"__Answer__: {answer}")
        references_output = get_formatted_references(references, limit=5)
        return [{"visibility": "visible"}, answer_output, references_output]
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
