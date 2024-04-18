import dash_design_kit as ddk
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html

from app import app

# Mapping of stage keys for categorical edits in sample dataset
stage_map = {"DS": "In Progress", "FDP": "Pre-production", "DP": "Post-production"}

DF = pd.read_csv("data/2019RevProtect_V4_renamed.csv")
## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Categorical.html
DF["Stage"] = pd.Categorical(DF["Stage"], list(DF["Stage"].unique()))
## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
DF = DF.sort_values("Stage")


marks = {year: str(year) for year in sorted(DF['Year'].unique())}

## Layouts
def control_card():
    return ddk.ControlCard(
        width=20,
        children=[
            ddk.CardHeader(title="Filters"),
            ddk.ControlItem(
                dcc.RangeSlider(
                    id="year-slider",
                    step=1,
                    min=DF["Year"].min(),
                    max=DF["Year"].max(),
                    marks={i: '{}'.format(i) for i in range(2019, 2023)},
                    value=[DF["Year"].min(), DF["Year"].max()],
                ),
                label="Year",
            ),
            ddk.ControlItem(
                dcc.Checklist(
                    id="filter-checklist",
                    options=[
                        {"label": i, "value": i}
                        for i in [
                            "Product",
                            "Region",
                            "Presentation",
                            "Site",
                        ]
                    ],
                    value=[],
                ),
                label="Filter By:",
            ),
            ddk.ControlItem(
                dcc.Dropdown(
                    id="product-dropdown",
                    value=DF["Product"].unique(),
                    multi=True,
                    options=[{"label": i, "value": i} for i in DF["Product"].unique()],
                ),
                label="Product",
                id="product-control",
                style={"display": "none"},
            ),
            ddk.ControlItem(
                dcc.Dropdown(
                    id="region-dropdown",
                    value=DF["Region"].unique(),
                    multi=True,
                    options=[{"label": i, "value": i} for i in DF["Region"].unique()],
                ),
                label="Region",
                id="region-control",
                style={"display": "none"},
            ),
            ddk.ControlItem(
                dcc.Dropdown(
                    id="presentation-dropdown",
                    value=DF["Presentation"].unique(),
                    multi=True,
                    options=[
                        {"label": i, "value": i} for i in DF["Presentation"].unique()
                    ],
                ),
                label="Presentation",
                id="presentation-control",
                style={"display": "none"},
            ),
            ddk.ControlItem(
                dcc.Dropdown(
                    id="site-dropdown",
                    value=DF["Site"].unique(),
                    multi=True,
                    options=[{"label": i, "value": i} for i in DF["Site"].unique()],
                ),
                label="Site",
                id="site-control",
                style={"display": "none"},
            ),
            ddk.ControlItem(
                html.Button(id="run-updt-btn", children="Submit and Update", n_clicks=0)
            ),
        ],
    )


def layout():
    page = html.Div(
        children=[
            ddk.Block(
                children=[
                    control_card(),
                    ddk.Block(
                        width=80,
                        children=[
                            ddk.Row(
                                children=[
                                    ddk.DataCard(
                                        id="stat1",
                                        width=100 / 4,
                                        value="68%",
                                        label="% Revenue Protection {}".format(
                                            stage_map["DS"]
                                        ),
                                        icon="",
                                    ),
                                    ddk.DataCard(
                                        id="stat2",
                                        width=100 / 4,
                                        value="77%",
                                        label="% Revenue Protection {}".format(
                                            stage_map["DP"]
                                        ),
                                        icon="",
                                    ),
                                    ddk.DataCard(
                                        id="stat3",
                                        width=100 / 4,
                                        value="39%",
                                        label="% Revenue Protection {}".format(
                                            stage_map["FDP"]
                                        ),
                                        icon="",
                                    ),
                                    ddk.DataCard(
                                        id="stat4",
                                        width=100 / 4,
                                        value=12,
                                        label="Products on Target",
                                        icon="",
                                    ),
                                ]
                            ),
                            ddk.Card(
                                width=100,
                                children=[
                                    ddk.CardHeader(
                                        title="Unprotected {} Revenue by Product, Site & Presentation".format(
                                            stage_map["FDP"]
                                        )
                                    ),
                                    html.Div(
                                        id="output-sankey", style={"height": "450px"}
                                    ),
                                ],
                            ),
                            ddk.Row(
                                children=[
                                    ddk.Card(
                                        width=100,
                                        children=[
                                            ddk.CardHeader(title="% Revenue Protected"),
                                            html.Div(
                                                id="output-heatmap-protected",
                                                style={"height": "450px"},
                                            ),
                                        ],
                                    )
                                ]
                            ),
                            ddk.Card(
                                width=100,
                                children=[
                                    ddk.CardHeader(title="Revenue By Product"),
                                    html.Div(
                                        id="output-bar-product",
                                        style={"height": "450px"},
                                    ),
                                ],
                            ),
                            ddk.Card(
                                width=100,
                                children=[
                                    ddk.CardHeader(
                                        title="Unprotected {} Revenue (USD M)".format(
                                            stage_map["FDP"]
                                        )
                                    ),
                                    html.Div(
                                        id="output-bar-presentation",
                                        style={"height": "450px"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            )
        ]
    )
    return page


## Graph helpers
def make_sankey_graph(labels, source, target, value):
    figure = go.Figure(
        go.Sankey(
            arrangement="snap",
            node={"label": labels, "pad": 10},  # 10 Pixels
            link={
                "source": source,
                "target": target,
                "value": value,
                "color": "#D1D1D1",
            },
        )
    )
    figure.update_layout(margin=dict(r=30))
    return ddk.Graph(figure=figure)


def make_bar_product_graph(product, totalrev, revunprotected):
    fig_bar_product = go.Figure()
    fig_bar_product.add_trace(
        go.Bar(
            x=product,
            y=totalrev,
            name="Total Revenue",
        )
    )
    fig_bar_product.add_trace(
        go.Bar(
            x=product,
            y=revunprotected,
            name="Unprotected Revenue",
        )
    )
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig_bar_product.update_layout(
        barmode="group", xaxis_tickangle=-45, hovermode="closest"
    )
    return fig_bar_product


## Callbacks
### This callback shows or hides the dropdowns
@app.callback(
    [
        Output("product-control", "style"),
        Output("region-control", "style"),
        Output("presentation-control", "style"),
        Output("site-control", "style"),
    ],
    [Input("filter-checklist", "value")],
)
def show_filters(filters):
    style_product = {"display": "None"}
    style_region = {"display": "None"}
    style_presentation = {"display": "None"}
    style_site = {"display": "None"}
    if "Product" in filters:
        style_product = {}
    if "Region" in filters:
        style_region = {}
    if "Presentation" in filters:
        style_presentation = {}
    if "Site" in filters:
        style_site = {}
    return style_product, style_region, style_presentation, style_site


# This callback updates heat maps, bar chart, pie chart, sankey, & stat cards
@app.callback(
    [
        Output("output-heatmap-protected", "children"),
        Output("output-bar-presentation", "children"),
        Output("output-sankey", "children"),
        Output("output-bar-product", "children"),
        Output("stat1", "value"),
        Output("stat2", "value"),
        Output("stat3", "value"),
        Output("stat4", "value"),
    ],
    [Input("run-updt-btn", "n_clicks")],
    [
        State("year-slider", "value"),
        State("product-dropdown", "value"),
        State("region-dropdown", "value"),
        State("presentation-dropdown", "value"),
        State("site-dropdown", "value"),
    ],
)
def filter_output(run_click, years, products, regions, presentations, sites):
    trp_ds = "N/A"
    trp_dp = "N/A"
    trp_fdp = "N/A"
    product_target = "N/A"
    filter_message = "Please make a valid selection"

    if (
        years == []
        or products == []
        or regions == []
        or presentations == []
        or sites == []
    ):
        heatmap_protected = filter_message
        bar_presentation = filter_message
        sankey = filter_message
        bar_product = filter_message
    else:
        year_list = list(range(years[0], years[1] + 1))
        # filter dataframe
        fdf = DF[
            DF["Year"].isin(year_list)
            & DF["Product"].isin(products)
            & DF["Region"].isin(regions)
            & DF["Presentation"].isin(presentations)
            & DF["Site"].isin(sites)
        ]

        stage = fdf["Stage"].unique()
        all_products = DF["Product"].unique()  # used in product sort order
        x = []
        y = []
        z_protected = []
        z_unprotected = []
        total_rev = []

        # Create Product Sort Order
        sort_stage = [stage_map["FDP"]]
        year_df = DF[DF["Year"].isin(year_list) & DF["Stage"].isin(sort_stage)]
        sort_df = pd.DataFrame(all_products, columns=["products"])
        sort_product_total_revs = []
        for i in all_products:
            product_df = year_df[year_df["Product"] == i]
            sort_product_total_rev = product_df["TotalRev"].sum()
            sort_product_total_revs.append(sort_product_total_rev)
        sort_df["total_rev_sum"] = sort_product_total_revs
        sort_df = sort_df.sort_values("total_rev_sum")

        fdf = fdf.sort_values("Product")
        ordered_product = fdf["Product"].unique()

        for i in stage:
            ## Filter dataframe by stage
            dfi = fdf[fdf["Stage"] == i]
            calc = dfi["RevProtected"].sum() / dfi["TotalRev"].sum()

            ## Calc Total Revenue Protected by stage
            if i == stage_map["DS"]:
                trp_ds = calc
            elif i == stage_map["DP"]:
                trp_dp = calc
            elif i == stage_map["FDP"]:
                # filtered dataframe for fdp stage
                fdf_fdp = dfi
                trp_fdp = calc

            divider = lambda x, y: None if y == 0 else x / y
            ## Filter stage dataframe by product
            ## (by stage because we're in a nested for loop) for heatmap
            for j in ordered_product:
                dfj = dfi[dfi["Product"] == j]
                x.append(i)
                y.append(j)
                total_rev_sum = dfj["TotalRev"].sum()
                total_rev.append(total_rev_sum)
                z_value_protected = divider(dfj["RevProtected"].sum(), total_rev_sum)
                z_value_unprotected = dfj["RevUnprotected"].sum()
                z_protected.append(z_value_protected)
                z_unprotected.append(z_value_unprotected)

        ## Create datacards based on calculated trp percents by stage
        ## Check if float to calc %, otherwise return 'n/a'
        if isinstance(trp_ds, float):
            trp_ds = str("{0:.0f}".format(trp_ds * 100)) + "%"
        if isinstance(trp_dp, float):
            trp_dp = str("{0:.0f}".format(trp_dp * 100)) + "%"
        if isinstance(trp_fdp, float):
            trp_fdp = str("{0:.0f}".format(trp_fdp * 100)) + "%"

        ### look at fdf - create column where actual - target. If not negative count
        count = 0
        for i in ordered_product:
            dfp = fdf[fdf["Product"] == i]
            diff = dfp["Actual"].sum() - dfp["Target"].sum()
            if diff >= 0:
                count = count + 1
        product_target = count

        heatmap_protected = ddk.Graph(
            figure={
                "data": [
                    {
                        "type": "heatmap",
                        "x": x,
                        "y": y,
                        "z": z_protected,
                        "hovertext": total_rev,
                        "zauto": False,
                        "zmin": 0,
                        "zmax": 1,
                    }
                ],
                "layout": {"xaxis": {"showgrid": False}, "yaxis": {"showgrid": False}},
            }
        )

        # start of FDP graphs
        if stage_map["FDP"] in fdf["Stage"].unique():
            products = fdf_fdp["Product"].unique().tolist()
            sites = fdf_fdp["Site"].unique().tolist()
            presentations = fdf_fdp["Presentation"].unique().tolist()
            secsites = fdf_fdp["SecSite"].unique().tolist()

            ## start of highest total FDP Rev table
            ## start of bar chart for unprotected rev by Presentation
            fig_bar = px.bar(
                fdf_fdp, x="Product", y="RevUnprotected", color="Presentation"
            )
            fig_bar.update_layout(xaxis={"categoryorder": "total descending"})
            bar_presentation = ddk.Graph(figure=fig_bar)

            ## start of sankey
            labels = products + sites + secsites + presentations
            source = []
            target = []
            value = []
            for prod in products:
                for s in sites:
                    source.append(labels.index(prod))
                    target.append(labels.index(s))
                    loop_fdf_fdp = fdf_fdp[
                        fdf_fdp["Product"].isin([prod]) & fdf_fdp["Site"].isin([s])
                    ]
                    value.append(loop_fdf_fdp["RevUnprotected"].sum())
            for s in sites:
                for sec in secsites:
                    source.append(labels.index(s))
                    target.append(labels.index(sec))
                    loop_fdf_fdp = fdf_fdp[
                        fdf_fdp["Site"].isin([s]) & fdf_fdp["SecSite"].isin([sec])
                    ]
                    value.append(loop_fdf_fdp["RevUnprotected"].sum())
            for sec in secsites:
                for p in presentations:
                    source.append(labels.index(sec))
                    target.append(labels.index(p))
                    loop_fdf_fdp = fdf_fdp[
                        fdf_fdp["SecSite"].isin([sec])
                        & fdf_fdp["Presentation"].isin([p])
                    ]
                    value.append(loop_fdf_fdp["RevUnprotected"].sum())

            sankey = make_sankey_graph(labels, source, target, value)

            # create dataframe out of fdf_fdp
            table_totalrev = []
            table_totalunprotectedrev = []

            for p in products:
                table_filter = fdf_fdp[fdf_fdp["Product"].isin([p])]
                table_totalrev.append(table_filter["TotalRev"].sum())
                table_totalunprotectedrev.append(table_filter["RevUnprotected"].sum())

            table_df = pd.DataFrame(products, columns=["Product"])
            table_df["TotalRev"] = table_totalrev
            table_df["RevUnprotected"] = table_totalunprotectedrev
            sorted_tdf = table_df.sort_values("TotalRev", ascending=False)
            sorted_tdf["TotalRev"] = sorted_tdf["TotalRev"].map("${:,.0f}".format)
            sorted_tdf["RevUnprotected"] = sorted_tdf["RevUnprotected"].map(
                "${:,.0f}".format
            )

            # DONE!!!! Start of Total Rev vs. Unprotected Rev by Product
            product = sorted_tdf["Product"].unique()
            totalrev = sorted_tdf["TotalRev"]
            revunprotected = sorted_tdf["RevUnprotected"]

            bar_product = ddk.Graph(
                figure=make_bar_product_graph(product, totalrev, revunprotected)
            )

        else:
            no_fdp_message = "{} revenue does not pertain to selected filters".format(
                stage_map["FDP"]
            )
            bar_presentation = no_fdp_message
            sankey = no_fdp_message
            bar_product = no_fdp_message
    return (
        heatmap_protected,
        bar_presentation,
        sankey,
        bar_product,
        trp_ds,
        trp_dp,
        trp_fdp,
        product_target,
    )
