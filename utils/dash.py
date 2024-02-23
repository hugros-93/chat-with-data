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


def get_formatted_references(references):
    references_output = html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(f'__Text__: _"{ref["text"]}"_'),
                        dcc.Markdown(f'__Source__: {ref["source"]}'),
                        dcc.Markdown(f'__Page__: {ref["page"]}'),
                    ],
                    title=f"Reference #{i+1} (score: {round(ref['score'], 2)})",
                )
                for i, ref in enumerate(references)
            ],
            start_collapsed=True,
        ),
    )
    return references_output
