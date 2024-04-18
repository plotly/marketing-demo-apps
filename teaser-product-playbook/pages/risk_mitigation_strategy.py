import dash_design_kit as ddk
from dash import html
import pandas as pd


def layout(product):

    # read in and filter data
    df_revprotect = pd.read_csv("data/2019RevProtect_V4.csv")

    drp = df_revprotect[df_revprotect["Product"] == product]
    stage = drp["Stage"].unique()
    year = drp["Year"].unique()
    ds_protected = []
    dp_protected = []
    fdp_protected = []

    for i in stage:
        stage_df = drp[drp["Stage"] == i]
        for y in year:
            year_df = stage_df[stage_df["Year"] == y]
            if i == "DS":
                ds_protected.append(
                    year_df["RevProtected"].sum() / year_df["TotalRev"].sum()
                )
            elif i == "DP":
                dp_protected.append(
                    year_df["RevProtected"].sum() / year_df["TotalRev"].sum()
                )
            elif i == "FDP":
                fdp_protected.append(
                    year_df["RevProtected"].sum() / year_df["TotalRev"].sum()
                )

    # Create Graphs
    # recommend using PX when data is in tidy format (ie all data is in 1 dataframe)
    rev_ds_fig = {"data": [{"type": "bar", "x": year, "y": ds_protected}]}
    rev_dp_fig = {"data": [{"type": "bar", "x": year, "y": dp_protected}]}
    rev_fdp_fig = {"data": [{"type": "bar", "x": year, "y": fdp_protected}]}

    risk_mitigation_content = html.Div(
        children=[
            ddk.Row(
                children=[
                    ddk.Card(
                        width=100 / 3,
                        children=[
                            ddk.CardHeader(title="% DS Revenue Protection"),
                            ddk.Graph(id="rev_ds_bar", figure=rev_ds_fig),
                        ],
                    ),
                    ddk.Card(
                        width=100 / 3,
                        children=[
                            ddk.CardHeader(title="% DP Revenue Protection"),
                            ddk.Graph(id="rev_ds_bar", figure=rev_dp_fig),
                        ],
                    ),
                    ddk.Card(
                        width=100 / 3,
                        children=[
                            ddk.CardHeader(title="% FDP Revenue Protection"),
                            ddk.Graph(id="rev_ds_bar", figure=rev_fdp_fig),
                        ],
                    ),
                ]
            ),
            ddk.Row(
                children=[
                    ddk.Card(
                        children=[
                            ddk.CardHeader(title="Risk Management Strategy"),
                            # html.Img(src=('assets/MitigationLevers/{}.png'.format(product)),
                            #     style={'width':'100%'})
                            html.P(
                                "Fusce mattis ante eu ante facilisis, a ornare justo sagittis. Curabitur in sem lacinia, feugiat nisl sit amet, lacinia ipsum. Quisque varius semper odio imperdiet tempus. Sed volutpat metus massa, et malesuada lacus vestibulum quis. Ut pulvinar leo justo, at bibendum quam laoreet sit amet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam vel nisl a quam dignissim commodo. Praesent aliquam, odio id placerat placerat, magna arcu tincidunt risus, id consectetur ligula enim quis diam. Vestibulum tincidunt, nibh quis dictum eleifend, metus lectus tristique lacus, dignissim dictum dolor felis eu odio. Mauris et ligula sed elit maximus gravida sed vel magna. Cras laoreet porttitor mi, ut aliquet augue sollicitudin vitae. Phasellus accumsan, lorem ut varius blandit, ex ipsum faucibus ante, vel condimentum ipsum urna non neque. "
                            ),
                        ]
                    )
                ]
            ),
        ]
    )
    return risk_mitigation_content
