import dash_design_kit as ddk
import dash_html_components as html

import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv"
)


def layout(product):
    ### Test for SC Map Table
    df_scmap = pd.read_csv("data/SCMAP_Dash.csv")
    df_scmap_filter = df_scmap[df_scmap["Product"] == product]

    fig = px.density_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Magnitude",
        radius=10,
        center=dict(lat=0, lon=180),
        zoom=2,
        mapbox_style="stamen-terrain",
        height=600,
    )
    fig.update_layout(margin=dict(r=100))
    page = html.Div(
        children=[
            ddk.Card(
                width=100,
                children=[
                    ddk.CardHeader(title="Supply Chain Map"),
                    ddk.Graph(figure=fig),
                ],
            ),
            ddk.Card(
                [
                    ddk.CardHeader(title="Table of Data"),
                    ddk.DataTable(
                        id="scmap-table",
                        columns=[{"name": i, "id": i} for i in df_scmap_filter.columns],
                        style_cell={"textAlign": "left"},
                        data=df_scmap_filter.to_dict("records"),
                    ),
                ]
            ),
            ddk.Card(children=["Supply Chain Map - comments section"]),
        ]
    )

    return page
