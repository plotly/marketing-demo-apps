import dash
import dash_design_kit as ddk
from dash import Input, Output, html, dcc

import data

app = dash.Dash(__name__)
app.title = "USA Gov. Analytics"
server = app.server

app.layout = ddk.App(
    show_editor=True,
    children=[
        ddk.Header(
            [
                ddk.Logo(src=app.get_relative_path("/assets/logo.png")),
                ddk.Title("USA Government Website Analytics"),
                dcc.Dropdown(
                    id="gov-agency",
                    style={"min-width": "150px"},
                    placeholder="Select a Department...",
                    options=data.GOV_OPTIONS,
                ),
                ddk.Menu([html.A("USA.Gov", href="https://usa.gov")]),
            ]
        ),
        ddk.Card(
            margin=0,
            width=30,
            children=[
                ddk.CardHeader(title="Most Popular"),
                dcc.Tabs(
                    children=[
                        dcc.Tab(
                            label="Top Domains (Past Week)",
                            children=[
                                ddk.Graph(
                                    id="top-domains-weekly",
                                    figure={
                                        "data": [
                                            {
                                                "y": data.get_top_domains()["y"],
                                                "x": data.get_top_domains()["x"],
                                                "type": "bar",
                                                "orientation": "h",
                                                "transforms": [
                                                    {
                                                        "type": "sort",
                                                        "target": "y",
                                                        "order": "descending",
                                                    }
                                                ],
                                            }
                                        ],
                                        "layout": {
                                            "height": 900,
                                            "xaxis": {"type": "log"},
                                            "margin": {"pad": 10, "l": 100},
                                        },
                                    },
                                    config={"downloadable": True},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Top Domains (Past Month)",
                            children=[
                                ddk.Graph(
                                    id="top-domains-monthly",
                                    figure={
                                        "data": [
                                            {
                                                "y": data.get_top_domains(days="30")[
                                                    "y"
                                                ],
                                                "x": data.get_top_domains(days="30")[
                                                    "x"
                                                ],
                                                "type": "bar",
                                                "orientation": "h",
                                                "transforms": [
                                                    {
                                                        "type": "sort",
                                                        "target": "y",
                                                        "order": "descending",
                                                    }
                                                ],
                                            }
                                        ],
                                        "layout": {
                                            "height": 900,
                                            "xaxis": {"type": "log"},
                                            "margin": {"pad": 10, "l": 100},
                                        },
                                    },
                                    config={"downloadable": True},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Top Pages (Now)",
                            children=[
                                ddk.Graph(
                                    id="top-pages",
                                    figure={
                                        "data": [
                                            {
                                                "y": data.get_top_pages()["y"],
                                                "x": data.get_top_pages()["x"],
                                                "type": "bar",
                                                "orientation": "h",
                                                "transforms": [
                                                    {
                                                        "type": "sort",
                                                        "target": "y",
                                                        "order": "descending",
                                                    }
                                                ],
                                            }
                                        ],
                                        "layout": {
                                            "height": 900,
                                            "xaxis": {"type": "log"},
                                        },
                                    },
                                    config={"downloadable": True},
                                )
                            ],
                        ),
                    ]
                ),
            ],
        ),
        ddk.Block(
            width=70,
            children=[
                ddk.Row(
                    [
                        ddk.DataCard(
                            id="people_live",
                            label="people on government sites right now",
                            icon="tv",
                            value=data.get_active_users(),
                            width=50,
                        ),
                        ddk.DataCard(
                            id="visits_month",
                            label="total visits (past month)",
                            icon="eye",
                            value=data.get_monthly_traffic(stat="visits"),
                            width=50,
                        ),
                    ]
                ),
                ddk.SectionTitle("Traffic Breakdown"),
                ddk.Card(
                    width=50,
                    children=[
                        ddk.CardHeader(
                            title="Visits Today",
                            fullscreen=True,
                            modal=True,
                            modal_config={"width": 80, "height": 80},
                        ),
                        ddk.Graph(
                            id="visits-today",
                            figure={
                                "data": [
                                    {
                                        "x": data.get_visits_today()["x"][1:],
                                        "y": data.get_visits_today()["y"][1:],
                                        "type": "bar",
                                        "name": "Closed",
                                    }
                                ],
                                "layout": {"height": 240},
                            },
                            config={"downloadable": True},
                        ),
                    ],
                ),
                ddk.Card(
                    width=50,
                    children=[
                        ddk.CardHeader(
                            title="Location of Visitors",
                            fullscreen=True,
                            modal=True,
                            modal_config={"width": 80, "height": 80},
                        ),
                        ddk.Graph(id="visitor-locations", figure=data.get_figure()),
                    ],
                ),
                ddk.Card(
                    width=100,
                    children=[
                        ddk.CardHeader(
                            fullscreen=True,
                            modal=True,
                            modal_config={"width": 80, "height": 80},
                            title="Top Downloads (Yesterday)",
                        ),
                        ddk.Graph(
                            id="top-downloads",
                            figure={
                                "data": [
                                    {
                                        "y": data.get_top_downloads()["y"],
                                        "x": data.get_top_downloads()["x"],
                                        "type": "bar",
                                        "orientation": "h",
                                        "transforms": [
                                            {
                                                "type": "sort",
                                                "target": "y",
                                                "order": "descending",
                                            }
                                        ],
                                    }
                                ],
                                "layout": {
                                    "height": 900,
                                    "xaxis": {
                                        "type": "log",
                                    },
                                    "margin": {"pad": 10, "l": 100},
                                },
                            },
                            config={"downloadable": True},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Data Card callbacks


@app.callback(Output("people_live", "value"), [Input("gov-agency", "value")])
def update_people_card_number(value):
    return data.get_active_users(dept=(value or "live"))


@app.callback(Output("people_live", "label"), [Input("gov-agency", "value")])
def update_people_card_dept(value):
    label = (
        (value or "all")
        .replace("-", " ")
        .title()
        .replace("Live", "all")
        .replace("All", "all")
    )
    return "people on {} sites right now".format((label or "all"))


@app.callback(Output("visits_month", "value"), [Input("gov-agency", "value")])
def update_monthly_visits_card(value):
    return data.get_monthly_traffic(dept=(value or "live"), stat="visits")


# Graph callbacks


@app.callback(Output("visits-today", "figure"), [Input("gov-agency", "value")])
def update_visits_today(value):
    return {
        "data": [
            {
                "x": data.get_visits_today(dept=(value or "live"))["x"][1:],
                "y": data.get_visits_today(dept=(value or "live"))["y"][1:],
                "type": "bar",
                "name": "Closed",
            }
        ],
    }


@app.callback(Output("top-downloads", "figure"), [Input("gov-agency", "value")])
def update_visits_today(value):
    return {
        "data": [
            {
                "y": data.get_top_downloads(dept=(value or "live"))["y"],
                "x": data.get_top_downloads(dept=(value or "live"))["x"],
                "type": "bar",
                "orientation": "h",
                "transforms": [{"type": "sort", "target": "y", "order": "descending"}],
            }
        ],
        "layout": {
            "height": 484,
            "xaxis": {
                "type": "log",
            },
            "margin": {"pad": 10, "l": 100},
        },
    }


@app.callback(Output("visitor-locations", "figure"), [Input("gov-agency", "value")])
def update_visits_today(value):
    return data.get_figure(dept=(value or "live"))


@app.callback(Output("top-domains-weekly", "figure"), [Input("gov-agency", "value")])
def update_top_domains_weekly(value):
    return {
        "data": [
            {
                "y": data.get_top_domains(dept=(value or "live"))["y"],
                "x": data.get_top_domains(dept=(value or "live"))["x"],
                "type": "bar",
                "orientation": "h",
                "transforms": [{"type": "sort", "target": "y", "order": "descending"}],
            }
        ],
        "layout": {
            "height": 900,
            "xaxis": {"type": "log"},
            "margin": {"pad": 10, "l": 100},
        },
    }


@app.callback(Output("top-domains-monthly", "figure"), [Input("gov-agency", "value")])
def update_top_domains_monthly(value):
    return {
        "data": [
            {
                "y": data.get_top_domains(days="30", dept=(value or "live"))["y"],
                "x": data.get_top_domains(days="30", dept=(value or "live"))["x"],
                "type": "bar",
                "orientation": "h",
                "transforms": [{"type": "sort", "target": "y", "order": "descending"}],
            }
        ],
        "layout": {
            "height": 900,
            "xaxis": {"type": "log"},
            "margin": {"pad": 10, "l": 100},
        },
    }


@app.callback(Output("top-pages", "figure"), [Input("gov-agency", "value")])
def update_top_pages(value):
    return {
        "data": [
            {
                "y": data.get_top_pages(dept=(value or "live"))["y"],
                "x": data.get_top_pages(dept=(value or "live"))["x"],
                "type": "bar",
                "orientation": "h",
                "transforms": [{"type": "sort", "target": "y", "order": "descending"}],
            }
        ],
        "layout": {"height": 900, "xaxis": {"type": "log"}},
    }


if __name__ == "__main__":
    app.run_server(debug=True)
