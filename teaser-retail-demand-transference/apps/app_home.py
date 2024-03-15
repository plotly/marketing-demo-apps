import dash
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_design_kit as ddk
import plotly.graph_objects as go

from utils.constants import SANKEY_COLORS, SANKEY_LINK_COLORS
from utils.helpers import HorizontalControlCard
from app import app, snap, generate_snapshot_layout

# Dataset
xls = pd.ExcelFile("./data/plotly_mockup_v3.xlsx")

# Scope
df_scope = pd.read_excel(xls, "Scope")
df_scope.dropna(axis=1, how="all")

# Certainity for bottom right graph
df_certainty = df_scope.loc[:, ["MCH_0", "Error", "Correlation", "Similarity"]]

# Uplift
df_uplift = pd.read_excel(xls, "Uplift_recommendation")

# T Matrices
df_T_Mat_juice = pd.read_excel(xls, "T_Mat_m10220202", index_col=0)
df_T_Mat_yogurt = pd.read_excel(xls, "T_Mat_m10220203", index_col=0)

df_T_Mat = {
    "M10220202 - Juices & Drinks-Refr": df_T_Mat_juice,
    "M10220203 - Yogurt": df_T_Mat_yogurt,
}

# Table Columns (Uplift Recommendation)
uplift_columns = [
    ("Article", "article_description"),
    ("Article Number", "article_number"),
    ("Scope", "banner"),
    ("Base Forecast", "Forecast"),
    ("Lift (units)", "Lifts (dummy)"),
]

# Feedback Preselection
feedback_sel = {
    "Good": "Results are good!",
    "Neutral": "Results are neutral!",
    "Bad": "Results are bad!",
}


def layout():
    layout = [
        html.Details(
            open=True,
            children=[
                html.Summary(
                    "Control Panel", style={"marginLeft": "5px", "marginRight": "5px"}
                ),
                html.Div(
                    [
                        ddk.Row(
                            [
                                ddk.ControlCard(
                                    width=40,
                                    orientation="horizontal",
                                    children=[
                                        ddk.CardHeader(title="Scope"),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="region-dropdown",
                                                options=[
                                                    {"label": i, "value": i}
                                                    for i in ["Ontario"]
                                                ],
                                                placeholder="Region ...",
                                                value="Ontario",
                                            ),
                                            label="Region",
                                            width=100 / 3,
                                        ),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="province-dropdown",
                                                options=[
                                                    {"label": item, "value": item,}
                                                    for item in df_scope[
                                                        "Region"
                                                    ].dropna()
                                                ],
                                                placeholder="Province ...",
                                                value="Ontario",
                                            ),
                                            width=100 / 3,
                                            label="Province",
                                        ),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="banner-dropdown",
                                                options=[
                                                    {"label": item, "value": item,}
                                                    for item in df_scope[
                                                        "Banner"
                                                    ].dropna()
                                                ],
                                                placeholder="Banner ...",
                                                value="Fortinos",
                                            ),
                                            width=100 / 3,
                                            label="Banner",
                                        ),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="mch1-dropdown",
                                                options=[
                                                    {
                                                        "label": "-".join(
                                                            item.split("-")[1:]
                                                        ),
                                                        "value": item,
                                                    }
                                                    for item in df_scope[
                                                        "MCH_1"
                                                    ].dropna()
                                                ],
                                                placeholder="MCH 1 ...",
                                                value=df_scope["MCH_1"]
                                                .dropna()
                                                .iloc[0],
                                            ),
                                            width=100,
                                            label="MCH 1",
                                        ),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="mch0-dropdown",
                                                options=[
                                                    {
                                                        "label": "-".join(
                                                            item.split("-")[1:]
                                                        ),
                                                        "value": item,
                                                    }
                                                    for item in df_scope[
                                                        "MCH_0"
                                                    ].dropna()
                                                ],
                                                value="M10220203 - Yogurt",
                                                placeholder="MCH 0 ...",
                                            ),
                                            width=100,
                                            label="MCH 0",
                                        ),
                                    ],
                                ),
                                ddk.ControlCard(
                                    width=35,
                                    children=[
                                        ddk.CardHeader(title="Transference Form"),
                                        ddk.ControlItem(
                                            dcc.Dropdown(
                                                id="transference-dropdown",
                                                options=[],
                                                placeholder="Transference ...",
                                                multi=True,
                                            ),
                                            width=100,
                                        ),
                                    ],
                                ),
                                ddk.ControlCard(
                                    width=25,
                                    orientation="horizontal",
                                    children=[
                                        ddk.CardHeader(title="Transference Adjustment"),
                                        HorizontalControlCard(
                                            children=[
                                                ddk.ControlItem(
                                                    dcc.Input(
                                                        id="trans-threshold-input",
                                                        type="number",
                                                        value=2,
                                                    ),
                                                    width=25,
                                                ),
                                                ddk.ControlItem(width=5),
                                                ddk.ControlItem(
                                                    html.P(
                                                        "Transference Threshold (%)",
                                                        style={"fontSize": "15px"},
                                                    )
                                                ),
                                            ],
                                        ),
                                        HorizontalControlCard(
                                            children=[
                                                ddk.ControlItem(
                                                    dcc.Input(type="number", value=80),
                                                    width=25,
                                                ),
                                                ddk.ControlItem(width=5),
                                                ddk.ControlItem(
                                                    html.P(
                                                        "Unit Sales (%)",
                                                        style={"fontSize": "15px"},
                                                    )
                                                ),
                                            ],
                                        ),
                                        HorizontalControlCard(
                                            children=[
                                                HorizontalControlCard(
                                                    children=[
                                                        ddk.ControlItem(
                                                            dcc.Dropdown(
                                                                options=[
                                                                    {
                                                                        "label": item,
                                                                        "value": item,
                                                                    }
                                                                    for item in [
                                                                        "High",
                                                                        "Medium",
                                                                        "Low",
                                                                    ]
                                                                ],
                                                                value="High",
                                                            ),
                                                            width=30,
                                                        ),
                                                        ddk.ControlItem(width=5),
                                                        ddk.ControlItem(
                                                            html.P(
                                                                "Model certainty",
                                                                style={
                                                                    "fontSize": "15px"
                                                                },
                                                            )
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                ),
            ],
        ),
        ddk.Row(
            [
                ddk.Card(
                    padding=20,
                    width=75,
                    children=[ddk.Graph(id="graph-sankey", style={"height": "90%"})],
                ),
                ddk.Block(
                    width=25,
                    children=[
                        ddk.Card(
                            children=[
                                ddk.CardHeader(title="Info Selected Transference"),
                                html.P(
                                    "Please click on an input node.",
                                    id="info-selected-click",
                                    style={"textAlign": "center"},
                                ),
                                ddk.DataTable(
                                    id="table-info",
                                    columns=[
                                        {"name": "Categories", "id": "categories",},
                                        {"name": "Value", "id": "value"},
                                    ],
                                    data=[
                                        {"categories": category, "value": " ",}
                                        for category in [
                                            "Market Share in MCHO",
                                            "Current On Hand",
                                            "Historical Fill Rate",
                                        ]
                                    ],
                                    style_table={"fontSize": "0.95em",},
                                    style_cell={
                                        "textAlign": "left",
                                        "height": "fitContent",
                                        "whiteSpace": "pre-line",
                                        "wordWrap": "break-word",
                                    },
                                ),
                            ],
                        ),
                        ddk.ControlCard(
                            children=[
                                ddk.CardHeader(title="Model Certainty"),
                                ddk.Block(id="block-model-certainty"),
                            ],
                        ),
                    ],
                ),
            ]
        ),
        ddk.Row(
            children=[
                ddk.Card(
                    width=75,
                    children=[
                        ddk.CardHeader(title="Uplift Recommendation"),
                        html.Div(
                            children=[
                                ddk.DataTable(
                                    id="table-uplift",
                                    columns=[
                                        {"name": item[0], "id": item[1]}
                                        for item in uplift_columns
                                    ]
                                    + [
                                        {
                                            "name": "Lifts (%)",
                                            "id": "Lifts (%)",
                                            "type": "numeric",
                                            "format": Format(
                                                precision=2,
                                                scheme=Scheme.fixed,
                                                symbol=Symbol.yes,
                                                symbol_suffix=u"%",
                                            ),
                                        }
                                    ],
                                    data=[{}],
                                    style_table={
                                        "fontSize": "0.95em",
                                        "height": "275px",
                                        "maxHeight": "275px",
                                        "overflowY": "scroll",
                                    },
                                    style_cell={
                                        "textAlign": "left",
                                        "height": "fitContent",
                                        "whiteSpace": "normal",
                                        "wordWrap": "breakWord",
                                    },
                                    export_format="xlsx",
                                    export_headers="display",
                                    filter_action="native",
                                    sort_action="native",
                                    row_selectable="multi",
                                    page_action="native",
                                    selected_rows=[],
                                ),
                            ]
                        ),
                    ],
                ),
                ddk.ControlCard(
                    width=25,
                    orientation="horizontal",
                    children=[
                        ddk.CardHeader(title="Feedback"),
                        ddk.ControlItem(
                            dcc.Input(id="snapshot-input"),
                            label="Report Name",
                            width=50,
                        ),
                        ddk.ControlItem(
                            dcc.Dropdown(
                                id="snapshot-dropdown",
                                options=[
                                    {"label": option, "value": option}
                                    for option in ["Good", "Neutral", "Bad"]
                                ],
                                value="Good",
                                placeholder="Select ...",
                            ),
                            label="Preselected Feedback",
                            width=50,
                        ),
                        ddk.ControlItem(
                            dcc.Textarea(
                                id="snapshot-textarea",
                                placeholder="Please enter feedback here ...",
                                style={"width": "100%"},
                            ),
                            width=100,
                            label="Feedback",
                        ),
                        ddk.ControlItem(
                            html.Button("Generate Report", id="snapshot-button"),
                            width=100,
                        ),
                        html.Div("", id="snapshot-status"),
                    ],
                ),
            ],
        ),
        dcc.Store(id="uplift-table-store"),
    ]
    return layout


# Update the MCH0 dropdown options when item selected in MCH1 dropdown
@app.callback(Output("mch0-dropdown", "options"), [Input("mch1-dropdown", "value")])
def update_mch0_options(mch1_sel):
    df_mch_0 = df_scope["MCH_0"].tolist()

    if mch1_sel == "M102202-Yogurt/Refrigerated Juice":
        return [
            {"label": "-".join(item.split("-")[1:]), "value": item}
            for item in df_mch_0[:2]
        ]
    else:
        return [
            {"label": "-".join(item.split("-")[1:]), "value": item}
            for item in df_mch_0[2:]
        ]


# Update the transference dropdown options when item selected in MCH0 dropdown
@app.callback(
    Output("transference-dropdown", "options"),
    [
        Input("mch0-dropdown", "value"),
        Input("mch1-dropdown", "value"),
        Input("region-dropdown", "value"),
        Input("province-dropdown", "value"),
        Input("banner-dropdown", "value"),
    ],
)
def update_transference_options(mch0_sel, mch1_sel, reg_sel, prov_sel, ban_sel):
    if all([mch0_sel, mch1_sel, reg_sel, prov_sel]):
        if mch0_sel in df_T_Mat.keys():
            df_T_Mat_sel = df_T_Mat[mch0_sel]
            # Relabel data and parse volume for hover labels, would be more efficient to do this
            # computation in initial dataset
            col_names = df_T_Mat_sel.columns.str.split("__")
            col_names = [col_data[1] for col_data in col_names]

            options_tup = list(zip(col_names, df_T_Mat_sel.index.tolist()))
            options = [{"label": item[0], "value": item[1]} for item in options_tup]
            return options
    return []


# Update the transference value when transference options are updated
@app.callback(
    Output("transference-dropdown", "value"),
    [Input("transference-dropdown", "options"),],
)
def update_transference_value(trans_options):
    if trans_options != []:
        return [
            trans_options[0]["value"],
            trans_options[1]["value"],
            trans_options[2]["value"],
        ]
    return dash.no_update


# Update the sankey graph
@app.callback(
    [Output("graph-sankey", "figure"), Output("uplift-table-store", "store")],
    [Input("transference-dropdown", "value"), Input("trans-threshold-input", "value"),],
    [
        State("mch0-dropdown", "value"),
        State("mch1-dropdown", "value"),
        State("region-dropdown", "value"),
        State("province-dropdown", "value"),
        State("banner-dropdown", "value"),
    ],
)
def update_sankey_graph(
    trans_sel, trans_thresh_input, mch0_sel, mch1_sel, reg_sel, prov_sel, ban_sel
):
    if all([mch0_sel, mch1_sel, reg_sel, prov_sel]):
        df_T_Mat_sel = df_T_Mat[mch0_sel].copy()
        df_T_Mat_sel.add_suffix(
            " "
        )  # Adding so Sankey graph can distinguish source and output nodes

        df_T_Mat_sel = df_T_Mat_sel.loc[trans_sel, :]

        # Filter based on Transference Threshhold
        df_T_Mat_sel = df_T_Mat_sel[df_T_Mat_sel > trans_thresh_input]
        # Relabel data and parse volume for hover labels, would be more efficient to do this
        # computation in initial dataset
        col_names = df_T_Mat_sel.columns.str.split("__")
        idx_names = df_T_Mat_sel.index.str.split("__")

        hover_names = [
            ["volume: {}{}".format(col_data[3].replace(" ", ""), col_data[2])]
            for col_data in col_names
        ]
        hover_names.extend(hover_names)

        # col_names = [col_data[1] for col_data in col_names]
        # idx_names = [idx_data[1] for idx_data in idx_names]
        col_labels = [col_data[1] for col_data in col_names]
        idx_labels = [idx_data[1] for idx_data in idx_names]

        col_codes = [col_data[0] for col_data in col_names]
        idx_codes = [idx_data[0] for idx_data in idx_names]

        col_names = ["{}-{}".format(col_data[0], col_data[1]) for col_data in col_names]
        idx_names = ["{}-{}".format(idx_data[0], idx_data[1]) for idx_data in idx_names]

        label = col_labels + idx_labels
        codes = col_codes + idx_codes

        # col_codes = [col_data[0] for col_data in col_names]
        # idx_codes = [idx_data[0] for idx_data in idx_names]
        # codes = col_codes + idx_codes

        # label = col_names + idx_names

        df_T_Mat_sel.index = idx_names
        df_T_Mat_sel.columns = col_names

        # Create sankey data
        source = []
        target = []
        value = []

        cols_len = df_T_Mat_sel.shape[0]
        rows_len = df_T_Mat_sel.shape[1]

        source_colors = SANKEY_LINK_COLORS
        target_colors = SANKEY_COLORS[:cols_len]

        for number in range(0, cols_len):
            source_val = [number + rows_len] * rows_len
            target_val = [itr for itr in range(0, rows_len)]

            source.extend(source_val)
            target.extend(target_val)

        for index, rows in df_T_Mat_sel.iterrows():
            value.extend(rows.tolist())

        fig = go.Figure(
            data=[
                go.Sankey(
                    arrangement="fixed",
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=label,
                        color=target_colors + source_colors,
                        customdata=codes,
                    ),
                    link=dict(
                        label=hover_names,
                        source=source,  # indices correspond to labels, eg A1, A2, A2, B1, ...
                        target=target,
                        value=value,
                    ),
                )
            ]
        )

        if ban_sel is None:
            title_text = "Displayed: {}".format(prov_sel)
        else:
            title_text = "Displayed: {} - {}".format(prov_sel, ban_sel)

        fig.update_layout(
            title_text=title_text,
            title_x=0.5,
            font_size=10,
            margin=dict(r=10),
            modebar={"orientation": "h"},
        )

        return fig, df_T_Mat_sel.to_json(date_format="iso", orient="split")
    return dash.no_update, dash.no_update


# Update the uplift table
@app.callback(
    [
        Output("table-uplift", "data"),
        Output("table-info", "data"),
        Output("info-selected-click", "children"),
    ],
    [Input("graph-sankey", "clickData")],
    [State("uplift-table-store", "store")],
)
def update_uplift_table(clickData, uplift_table_stored):
    if uplift_table_stored:
        df_T_Mat_sel = pd.read_json(uplift_table_stored, orient="split")

    table_info_data = [
        {"categories": "MCHO Market Share", "value": " ",},
        {"categories": "On Hand (Current)", "value": " ",},
        {"categories": "Historical Fill Rate", "value": " ",},
    ]

    if clickData is not None:

        # Get label of selected node
        try:
            selected_node = (
                clickData["points"][0]["customdata"]
                + "-"
                + clickData["points"][0]["label"]
            )
        except:
            # If this errors it means we clicked the sankey links
            raise dash.exceptions.PreventUpdate

        # If selected node is an output node or selected node is null do not fire. Tried to do if statement
        # on "label" existing in the selected_node dict with no success, hence why we have two PreventUpdates
        if selected_node == "" or selected_node not in df_T_Mat_sel.index:
            raise dash.exceptions.PreventUpdate

        selected_node = (
            clickData["points"][0]["customdata"] + "-" + clickData["points"][0]["label"]
        )

        # Find the output nodes connected to the selected input node and drop nan/0 values
        df_T_Mat_sel = df_T_Mat_sel.loc[[selected_node], :].dropna(axis=1)
        df_T_Mat_sel.loc[~(df_T_Mat_sel == 0).all(axis=1)]

        # Get article numbers
        selected_article_number = int(selected_node.split("-")[0])
        article_numbers = [int(column.split("-")[0]) for column in df_T_Mat_sel.columns]

        dff_uplift = df_uplift[df_uplift["article_number"].isin(article_numbers)].copy()

        # Check if article numbers are missing in uplift recommendation (this happens b/c we don't have full dataset)
        if len(dff_uplift["article_number"]) != len(article_numbers):
            dff_article_list = dff_uplift["article_number"].tolist()
            missing_vals = list(set(article_numbers) - set(dff_article_list))
            print(
                "Missing article numbers {} from Uplift Recommendation.".format(
                    missing_vals
                )
            )

        # Check if dataframe filter returns empty dataframe, this can happen
        # if the uplift dataset is missing data in the transference matrix
        # Ex: Danone Oikos 0% - Cherry
        if dff_uplift.empty:
            print("Missing article numbers for input node: ", selected_article_number)
            return dash.no_update, dash.no_update, dash.no_update

        table_info_data[0]["value"] = round(
            dff_uplift.iloc[0]["Market share in MCH0"], 5
        )
        table_info_data[1]["value"] = dff_uplift.iloc[0]["Current On Hand (dummy)"]
        table_info_data[2]["value"] = dff_uplift.iloc[0]["Historical Fill Rate (dummy)"]

        dff_uplift["article_number"] = dff_uplift["article_number"].apply(
            lambda x: abs(hash(str(x)))
        )

        return (
            dff_uplift.to_dict("records"),
            table_info_data,
            "-".join(selected_node.split("-")[1:]),
        )
    return [{}], table_info_data, "Please select a node."


# Update block model certainty
@app.callback(
    Output("block-model-certainty", "children"),
    [Input("mch0-dropdown", "value"), Input("graph-sankey", "clickData")],
)
def update_uplift_table(mch0_sel, clickData):
    if mch0_sel is None:
        return html.P("Please select a MCH_0")
    else:
        df_scope_filtered = df_scope[df_scope["MCH_0"] == mch0_sel]

        return html.Div(
            [
                html.P(mch0_sel, style={"textAlign": "center"}),
                html.P(
                    ["Error (mock): ", html.Span("+12%", style={"color": "green"})],
                    style={"textAlign": "center"},
                ),
                html.P(
                    ["Correlation (mock): ", html.Span("-10%", style={"color": "red"})],
                    style={"textAlign": "center"},
                ),
                html.P(
                    [
                        "Similarity (mock): ",
                        html.Span("+15%", style={"color": "green"}),
                    ],
                    style={"textAlign": "center"},
                ),
            ]
        )


# Prepopulate feedback box
@app.callback(
    Output("snapshot-textarea", "value"), [Input("snapshot-dropdown", "value")]
)
def prepopulate_textarea(preselection):
    return feedback_sel[preselection]


# Snapshot
@app.callback(
    [Output("url", "pathname"), Output("snapshot-status", "children")],
    [Input("snapshot-button", "n_clicks")],
    [
        State("snapshot-textarea", "value"),
        State("table-uplift", "data"),
        State("table-uplift", "selected_rows"),
        State("snapshot-input", "value"),
    ],
)
def take_snapshot(snapshot_click, feedback, table_data, selected_rows, report_name):
    if selected_rows == []:
        return dash.no_update, "Error: Please select uplift data in uplift table."

    if snapshot_click:
        uplift_data = [table_data[i] for i in selected_rows]
        snapshot_id = snap.snapshot_save_async(
            generate_snapshot_layout, feedback, uplift_data
        )
        snap.meta_update(snapshot_id, {"snapshot_name": report_name})
        print("snapshot meta updated")
    return app.get_relative_path("/archive"), ""
