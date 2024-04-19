import dash, os, redis
from dash import html
import dash_design_kit as ddk
from datetime import datetime

from utils.components import get_performance_tracking_layout, get_kpis


redis_instance = redis.StrictRedis.from_url(
    os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"), decode_responses=True
)
REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")

dash.register_page(__name__)


def footer(client):
    standard_footer = ddk.PageFooter(
        [
            html.Span(
                "Produced by {} -- Permission required for redistribution".format(
                    client
                ),
                className="note-1",
            ),
        ],
        display_page_number=True,
    )
    return standard_footer


def section_page(title, client, bg_color="var(--accent)"):
    section = ddk.Page(
        [
            html.Div(
                title,
                style={
                    "marginTop": "2in",
                    "fontSize": "40px",
                    "fontWeight": "bold",
                    "text-align": "center",
                },
            ),
            footer(client),
        ],
        style={"backgroundColor": bg_color, "color": "#fff"},
    )

    return section


def layout(title="Overview Data", client=None, neighborhood=None):
    # sample dataset

    # The set of pages in the report
    children = [
        ddk.Page(
            [
                ddk.Block(
                    [
                        html.Img(
                            src=dash.get_asset_url("images/dash-logo.png"),
                            style={
                                "height": "auto",
                                "width": "350px",
                                "marginTop": "2.7in",
                            },
                        ),
                        html.H2("Overview Data", style={"fontWeight": "bold"}),
                        html.H3(
                            datetime.now().strftime("%B %d, %Y"),
                            style={"margin-top": "1em"},
                        ),
                    ],
                    style={"text-align": "center"},
                ),
            ],
            style={"backgroundColor": "var(--accent)"},
        ),
        ddk.Page(
            children=[
                html.Div(
                    f"Whole Market Performance",
                    style={
                        "fontSize": "40px",
                        "fontWeight": "bold",
                        "text-align": "center",
                    },
                ),
                html.Div(children=get_kpis()),
                html.Div(
                    f"Performance Table for {neighborhood}",
                    style={
                        "fontSize": "40px",
                        "fontWeight": "bold",
                        "text-align": "center",
                    },
                )
                if neighborhood
                else html.Div(
                    f"Performance Table",
                    style={
                        "marginTop": "2in",
                        "fontSize": "40px",
                        "fontWeight": "bold",
                        "text-align": "center",
                    },
                ),
                html.Div(children=get_performance_tracking_layout(neighborhood)),
            ],
        ),
    ]
    return ddk.Report(display_page_numbers=True, children=children)
