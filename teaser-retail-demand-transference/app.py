import os

import celery
import dash
from dash import html, dcc
import dash_design_kit as ddk
import dash_snapshots
import datetime
import redis

# os.environ["REDIS_URL"] = os.getenv("REDIS_URL", os.getenv("EXTERNAL_REDIS_URL"))


app = dash.Dash(__name__)
app.title = "Retail Demand Transference"
app.config["suppress_callback_exceptions"] = True

# Snapshot Engine
os.environ["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
os.environ["SNAPSHOT_DATABASE_URL"] = os.environ.get(
    "REDIS_URL", "redis://127.0.0.1:6379"
)

snap = dash_snapshots.DashSnapshots(app)

# Celery
celery_instance = snap.celery_instance

# Generate Unique Snapshot ID
@celery_instance.task
@snap.snapshot_async_wrapper(save_pdf=True)
def generate_snapshot_layout(feedback, uplift_data):
    uplift_columns = [
        ("Article", "article_description"),
        ("Article Number", "article_number"),
        ("Scope", "banner"),
        ("Base Forecast", "Forecast"),
        ("Lift (units)", "Lifts (dummy)"),
    ]

    report_header = html.Div(
        [
            html.H2(
                "Transference Report",
                style={
                    "display": "inline-block",
                    "float": "right",
                    "color": "var(--text)",
                    "font-family": "var(--font_family_header)",
                    "letter-spacing": "2px",
                    "line-height": "65px",
                },
            )
        ],
        style={"border-bottom": "1px solid grey", "height": "100px"},
    )
    report_footer = ddk.PageFooter(
        [html.Span("Confidential, do not share", className="report-footer-left")]
    )

    # notes_container = html.Div(id="snapshot-note-container", children=note)

    page = ddk.Report(
        display_page_numbers=True,
        children=[
            ddk.Page(
                [
                    report_header,
                    ddk.Card(
                        type="flat",
                        style={
                            "background-color": "var(--report_background_page)",
                            "font-size": "14px",
                            "marginBottom": "0px",
                        },
                        children=[
                            ddk.CardHeader("Study Details"),
                            ddk.Block(
                                [
                                    ddk.DataTable(
                                        columns=[
                                            {"name": name, "id": column_id}
                                            for name, column_id in uplift_columns
                                        ],
                                        style_cell={"textAlign": "left"},
                                        css=[
                                            {
                                                "selector": "td",
                                                "rule": "background-color: var(--report_background_page) !important;",
                                            }
                                        ],
                                        data=uplift_data,
                                    )
                                ]
                            ),
                            ddk.Block(
                                style={
                                    "backgroundColor": "var(--report_background_page)",
                                    "font-size": "14px",
                                    "marginTop": "50px",
                                },
                                children=[
                                    ddk.CardHeader("Uplift Feedback"),
                                    html.P(
                                        """{}""".format(feedback),
                                        style={
                                            "text-align": "justify",
                                            "font-size": "var(--report_font_size)",
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                    report_footer,
                ]
            )
        ],
    )
    return page
