import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Product Summary"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Product Playbook utilizes 2019 2nd Pass LRS and August PC. \
                                    Supply Gaps occur in the DP Stage. \
                                    Supply Gaps occur in the FDP Stage.  \
                                    Revenue Protected in DS Stage is 100% from 2019-2023. \
                                    Revenue Protected in DP Stage drops from 98.1% in 2019 to 97.7% in 2023. \
                                    Revenue Protected in FDP Stage drops to a low of 88.8% in 2022. \
                                    Risk Mitigation Strategy includes Increasing Inventory and Diversification.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["General Information"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Revenue (in USD millions)",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "391",
                                                        "544",
                                                        "1,219",
                                                        "1,695",
                                                        "2,207",
                                                    ],
                                                    marker={
                                                        "color": "#0A223B",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="US",
                                                ),
                                                go.Bar(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "165",
                                                        "208",
                                                        "301",
                                                        "385",
                                                        "442",
                                                    ],
                                                    marker={
                                                        "color": "#113963",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="EU",
                                                ),
                                                go.Bar(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "044",
                                                        "081",
                                                        "160",
                                                        "273",
                                                        "521",
                                                    ],
                                                    marker={
                                                        "color": "#1C60A7",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="JAPAC",
                                                ),
                                                go.Bar(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "051",
                                                        "086",
                                                        "128",
                                                        "175",
                                                        "200",
                                                    ],
                                                    marker={
                                                        "color": "#919191",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="ICON",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 8],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Total Revenue Growth",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "651",
                                                        "919",
                                                        "1,808",
                                                        "2,527",
                                                        "3,370",
                                                    ],
                                                    line={"color": "#1C60A7"},
                                                    mode="lines",
                                                    name="Total Revenue",
                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                title="",
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                width=340,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0277108433735,
                                                    "y": -0.142606516291,
                                                    "orientation": "h",
                                                },
                                                margin={
                                                    "r": 20,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                xaxis={
                                                    "autorange": True,
                                                    "linecolor": "rgb(0, 0, 0)",
                                                    "linewidth": 1,
                                                    "range": [2019, 2023],
                                                    "showgrid": False,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                },
                                                yaxis={
                                                    "autorange": False,
                                                    "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                    "mirror": False,
                                                    "nticks": 4,
                                                    "range": [0, 4000],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "ticklen": 10,
                                                    "ticks": "outside",
                                                    "title": "in USD millions",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                    "zerolinewidth": 4,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "FDP Units (in thousands)",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-3",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=[
                                                        "2019",
                                                        "2020",
                                                        "2021",
                                                        "2022",
                                                        "2023",
                                                    ],
                                                    y=[
                                                        "5,790",
                                                        "8,933",
                                                        "13,423",
                                                        "18,792",
                                                        "26,994",
                                                    ],
                                                    marker={
                                                        "color": "#1C60A7",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="FDP",
                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 8],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
