import dash
import dash_html_components as html
import dash_design_kit as ddk
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from app import app

import pages

server = app.server

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
        html.A("Enterprise Demo", href="https://plotly.com/get-demo/", target="_blank"),
        html.A("Request Code", href="https://plotly.com/contact-us/", target="_blank"),
    ],
)

# Overall app layout
app.layout = ddk.App(
    show_editor=True,
    children=[
        dcc.Location(id="url", refresh=False),
        ddk.Header(
            [
                dcc.Link(
                    href=app.get_relative_path("/"),
                    style={"height": "100%", "width": "auto"},
                    children=ddk.Logo(
                        src=app.get_asset_url("Plotly_logo-b.png"),
                        style={"maxHeight": "70px", "width": "auto"},
                    ),
                ),
                ddk.Menu(
                    children=[
                        dcc.Link("Product Revenue", href=app.get_relative_path("/")),
                        dcc.Link(
                            "Product Playbook",
                            href=app.get_relative_path("/product-playbook"),
                        ),
                        learn_more_menu,
                    ]
                ),
            ]
        ),
        html.Div(id="overall-content", children=[]),
    ],
)


# Callback to determine page content based on selected dcc.link
@app.callback(Output("overall-content", "children"), [Input("url", "pathname")])
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:
        return pages.home.layout()
    elif page_name == "product-playbook":
        return pages.product_playbook.layout()
    else:
        return "404 not found"


# debug is always false on deploy
if __name__ == "__main__":
    app.run_server(debug=True)
