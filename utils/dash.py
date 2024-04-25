from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


class DashboardColors:
    black = "black"
    white = "white"

    gray = "gray"
    background_gray = "#e4e6e6"

    green = "#00b050"
    light_green = "#90e990"
    yellow = "#ffc82f"
    orange = "#f37021"
    red = "#ff0000"

    palette_category = [
        "#1319cb",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    palette_green = [
        "#efffad",
        "#cbf266",
        "#99e866",
        "#66cc66",
        "#00b050",
        "#009933",
        "#00792b",
        "#004700",
    ]

    palette_blue = [
        "#e2f2ff",
        "#99ccff",
        "#6699ff",
        "#3366cc",
        "#253fc8",
        "#140a9a",
        "#0c065c",
        "#1b232a",
    ]


def get_formatted_references(references, limit=None):
    if limit == None:
        selected_references = references
    else:
        selected_references = references[:limit]
    references_output = html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(f'__Text__: _"{ref["text"]}"_'),
                    ]
                    + [
                        dcc.Markdown(f'__{m.capitalize()}__: {ref["metadata"][m]}')
                        for m in ref["metadata"]
                    ],
                    title=f"Reference #{i+1} (score: {round(ref['score'], 2)})",
                )
                for i, ref in enumerate(selected_references)
            ],
            start_collapsed=True,
        ),
    )
    return references_output


def get_formatted_data(dict_source):
    data_output = html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(f"__{m.capitalize()}__: {dict_source[source][m]}")
                        for m in dict_source[source]
                    ],
                    title=f"Source #{i+1}: {source}",
                )
                for i, source in enumerate(dict_source)
            ],
            start_collapsed=True,
        ),
    )
    return data_output


def get_header_buttons():
    return dbc.Col(
        html.Div(
            [
                dcc.Loading(
                    id="loading-state-load-data",
                    type="circle",
                    color=DashboardColors.green,
                    children=dcc.Upload(
                        dbc.Button(
                            "📥 Load data",
                            id="button-load-data",
                            color="primary",
                            className="me-1",
                            n_clicks=0,
                            disabled=False,
                        ),
                        id="upload-file",
                        multiple=True,
                    ),
                ),
                html.P(id="output-load-data"),
                dbc.Modal(
                    [
                        dbc.ModalBody("Data successfully loaded!"),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close",
                                id="button-modal-load-data",
                                className="ms-auto",
                                n_clicks=0,
                            )
                        ),
                    ],
                    id="modal-load-data",
                    is_open=False,
                ),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        ),
        width=True,
    )
