from dash import html, dcc, dash_table
import dash_design_kit as ddk
import plotly.express as px

import pandas as pd

import random
import requests


def layout(product):
    ## Load and filter the data
    df_revenue = pd.read_csv("data/Revenue_Dash.csv").sort_values(by="Year")
    df_revenue_line = pd.read_csv("data/Revenue_Line_Dash.csv").sort_values(by="Year")
    df_volume = pd.read_csv("data/Volume_Dash.csv").sort_values(by="Year")
    df_geninfo = pd.read_csv("data/Gen_Info_Dash.csv")

    df_rev_filter = df_revenue.loc[df_revenue["Product"] == product]
    df_rev_line_filter = df_revenue_line.loc[df_revenue_line["Product"] == product]
    df_vol_filter = df_volume.loc[df_volume["Product"] == product]
    df_geninfo_filter = df_geninfo.loc[df_geninfo["Product"] == product].drop(
        "Product", axis=1
    )

    ## GRAPHS
    ### Create revenue bar graph
    ### https://plot.ly/python/bar-charts/
    rev_bar_fig = px.bar(
        df_rev_filter, x="Year", y="Revenue", color="Region"
    ).update_layout(xaxis={"dtick": 1})
    ### Create revenue line graph
    ### https://plot.ly/python/line-charts/
    rev_line_fig = px.line(
        df_rev_line_filter, x="Year", y="Revenue", color="Presentation"
    )
    rev_line_fig.update_layout(xaxis={"dtick": 1})
    ## The overlap of the line here is due to a Region having multiple
    ## date points for different Presentations, to resolve this we can
    ## group by presentations as above.

    ### Create supply bar graph
    ### https://plot.ly/python/bar-charts/
    sup_bar_fig = px.bar(df_vol_filter, x="Year", y="Volume").update_layout(
        xaxis={"dtick": 1}
    )

    ### Create supply line graph
    ### https://plot.ly/python/line-charts/

    sup_line_fig = px.line(
        df_vol_filter,
        x="Year",
        y="Volume",
    )
    sup_line_fig.update_layout(xaxis={"dtick": 1})

    words = open("data/nouns.txt", "r").readlines()

    r_title = lambda: random.choice(words).title()
    r = lambda: random.choice(words).lower()

    selected_words = [r_title(), r_title()]

    product_summary_content = html.Div(
        children=[
            # all content in section below is product specific
            # callback added in app.py file to trigger page update
            # to product that is selected from drop down
            ddk.Row(
                children=[
                    ddk.Card(
                        children=[
                            ddk.Block(
                                width=100,
                                children=html.H4(product + " 2019 Product Playbook"),
                                style={
                                    "text-align": "center",
                                    "background-color": "#1c60a7",
                                    "color": "white",
                                }
                                # add blue background color, add title and summary in white
                                # ensure height is sized correctly, center writing in card
                            ),
                            ddk.Card(
                                children=[
                                    ddk.Block(
                                        width=50,
                                        style={"padding-right": 10},
                                        children=[
                                            ddk.CardHeader(title="General Information"),
                                            ddk.DataTable(
                                                id="geninfo-table",
                                                columns=[
                                                    {"name": i, "id": i}
                                                    for i in df_geninfo_filter.columns
                                                ],
                                                data=df_geninfo_filter.to_dict(
                                                    "records"
                                                ),
                                                style_cell={"textAlign": "left"},
                                                style_header={"display": "none"},
                                            ),
                                        ],
                                    ),
                                    ddk.Block(
                                        width=50,
                                        style={"padding-left": 10},
                                        children=[
                                            ddk.CardHeader(title="Product Summary"),
                                            html.P(
                                                "{0} is a {1} {2} Factor ({3}{4}F) inhibitor approved to treat {5} diseases across {6} and {7}.".format(
                                                    r_title(),
                                                    selected_words[0],
                                                    selected_words[1],
                                                    selected_words[0][0],
                                                    selected_words[1][0],
                                                    r(),
                                                    r(),
                                                    r(),
                                                )
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            ddk.Row(
                children=[
                    ddk.Block(
                        width=100,
                        children=[
                            ddk.Row(
                                children=[
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            ddk.CardHeader(
                                                title="FDP Revenue By Region"
                                            ),
                                            ddk.Graph(
                                                id="revenue-bar", figure=rev_bar_fig
                                            ),
                                        ],
                                    ),
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            ddk.CardHeader(
                                                title="FDP Revenue By Presentation"
                                            ),
                                            ddk.Graph(
                                                id="revenue-line", figure=rev_line_fig
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                            ddk.Row(
                                children=[
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            ddk.CardHeader(
                                                title="Supply By Presentation"
                                            ),
                                            ddk.Graph(
                                                id="volume-bar", figure=sup_bar_fig
                                            ),
                                        ],
                                    ),
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            ddk.CardHeader(
                                                title="Supply By Presentation"
                                            ),
                                            ddk.Graph(
                                                id="volume-line", figure=sup_line_fig
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    )
                ]
            ),
        ]
    )

    return product_summary_content
