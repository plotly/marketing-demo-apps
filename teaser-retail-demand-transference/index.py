from dash import dcc, html, Input, Output
import dash_design_kit as ddk

import os
import json

from app import app, snap
from apps import app_home, app_archive

# Header
def header():
    learn_more_menu = ddk.CollapsibleMenu(
        title="Learn More",
        default_open=False,
        children=[
            html.A(
                "Low-code Design",
                href="https://plotly.com/dash/design-kit/",
                target="_blank",
            ),
            html.A(
                "Snapshot Engine",
                href="https://plotly.com/dash/snapshot-engine/",
                target="_blank",
            ),
            html.A(
                "Enterprise Demo", href="https://plotly.com/get-demo/", target="_blank"
            ),
            html.A(
                "Request Code", href="https://plotly.com/contact-us/", target="_blank"
            ),
        ],
    )
    return ddk.Header(
        style={"background": "var(--accent)"},
        children=[
            ddk.Title(
                "Retail Demand Transference", style={"color": "var(--accent_negative)"}
            ),
            ddk.Menu(
                children=[
                    dcc.Link(
                        "Home",
                        href=app.get_relative_path("/"),
                        style={"color": "var(--accent_negative)"},
                    ),
                    dcc.Link(
                        "Archive",
                        href=app.get_relative_path("/archive"),
                        style={"color": "var(--accent_negative)"},
                    ),
                    learn_more_menu,
                ]
            ),
        ],
    )


def view_snapshot(snapshot_id):
    # Take snapshot content from redis by ID
    snapshot_content = snap.snapshot_get(snapshot_id)
    return snapshot_content


app.layout = ddk.App(
    children=[
        header(),
        dcc.Location(id="url", refresh=False),
        ddk.Block(id="page-content"),
    ]
)

server = app.server


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:
        return app_home.layout()
    elif page_name == "archive":
        return app_archive.layout()
    elif page_name.startswith("snapshot-"):
        return view_snapshot(page_name)
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
