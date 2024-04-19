from dash import dcc, html
import dash_design_kit as ddk
import pandas as pd

from constants import (
    performance,
    today_data,
    trips_gained,
    revenue_gained,
    total_rebalancing_cost,
    profit,
    neighborhood_list,
)
from utils.utils import recalculate_recs


def header(name, app):
    learn_more_menu = ddk.CollapsibleMenu(
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
            html.A(
                "Enterprise Demo", href="https://plotly.com/get-demo/", target="_blank"
            ),
            html.A(
                "Request Code", href="https://plotly.com/contact-us/", target="_blank"
            ),
        ],
    )

    plotly_logo = ddk.Logo(
        src=app.get_asset_url("images/dash-logo.png"),
        style={"height": 50},
    )
    plotly_link = html.A(plotly_logo, href="https://plotly.com/dash/", target="_blank")

    return ddk.Header(
        [
            plotly_link,
            ddk.Title(
                html.A(name, href=app.get_relative_path("/"), className="header-title"),
            ),
            ddk.Menu(
                [
                    dcc.Link(
                        "Overview", href=app.get_relative_path("/"), id="overview-link"
                    ),
                    # dcc.Link("Live View", href=app.get_relative_path("/live-view"), id="live-view-link"),
                    dcc.Link(
                        "Fleet Movement Planning",
                        href=app.get_relative_path("/fleet_movement_planning"),
                        id="fleet_movement_link",
                    ),
                    dcc.Link(
                        "Performance Tracking",
                        href=app.get_relative_path("/performance"),
                        id="performance_tracking_link",
                    ),
                    dcc.Link(
                        "Simulations",
                        href=app.get_relative_path("/simulation"),
                        id="simulation-link",
                    ),
                ],
                style={"display": "flex", "flex": "auto"},
            ),
            ddk.Menu(
                [learn_more_menu], className="no-highlight"
            ),  # archive_link, x, theme_toggle, x
        ],
        content_alignment="center",
    )


def get_performance_tracking_layout(neighborhood_selected=None):
    df = performance
    if neighborhood_selected:
        df = df.query("neighborhood == @neighborhood_selected")
        df = df.loc[
            :,
            [
                "monthname",
                "departures",
                "arrivals",
                "excess_arrivals",
                "effective_moves",
            ],
        ]
        df.columns = [
            "Month",
            "Departures",
            "Arrivals",
            "Excess Arrivals",
            "Effective Moves",
        ]

        df["Departures"] = df["Departures"].map("{:,.0f}".format)
        df["Arrivals"] = df["Arrivals"].map("{:,.0f}".format)
        df["Est. Revenue Gained"] = (df["Effective Moves"] * 2.02).map(
            "${:,.0f}".format
        )
        df["Excess Arrivals"] = df["Excess Arrivals"].map("{:,.0f}".format)
        df["Effective Moves"] = df["Effective Moves"].map("{:,.0f}".format)
    else:
        df = df.groupby("monthname").sum().reset_index()
        df = df.loc[
            :,
            [
                "monthname",
                "departures",
                "effective_moves",
            ],
        ]
        df.columns = [
            "Month",
            "Total Trips",
            "Effective Moves",
        ]
        df["Total Trips"] = df["Total Trips"].map("{:,.0f}".format)
        df["Est. Revenue Gained"] = (df["Effective Moves"] * 2.02).map(
            "${:,.0f}".format
        )
        df["Effective Moves"] = df["Effective Moves"].map("{:,.0f}".format)

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=months, ordered=True)
    df.sort_values(by=["Month"], inplace=True)

    return ddk.DataTable(
        df.to_dict("records"),
        [{"name": i, "id": i} for i in df.columns],
        id="performance-table",
        style_header={
            "backgroundColor": "#131416",
            "text-align": "center",
            "border": "0px",
            "font-size": "smaller",
            "font-weight": "bolder",
            "color": "white",
        },
        style_data={
            "color": "white",
            "backgroundColor": "inherit",
            "whiteSpace": "normal",
            "height": "auto",
            "text-align": "center",
            "border": "0px",
            "font-size": "medium",
            "color": "rgb(162, 170, 184)",
            "padding-top": "10px",
            "padding-bottom": "10px",
        },
        style_table={
            "padding-top": "20px",
            "padding-bottom": "20px",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "background-color": "rgb(38 38 38)",
            },
        ],
    )


def get_fleet_movement_layout(neighborhood_selected=None, store=None):

    df = today_data.set_index("code", drop=False)

    df = df.loc[df["neighborhood"].isin(neighborhood_selected)]
    if store:
        df = recalculate_recs(df)
        for key, val in store.items():
            if val > 0:
                df.at[int(key), "adjusted_adds"] = val
                df.at[int(key), "recommended_removals"] = 0
            else:
                df.at[int(key), "recommended_removals"] = -val
                df.at[int(key), "adjusted_adds"] = 0
        df["recommended_adds"] = df["adjusted_adds"]
        df.dropna(inplace=True)

    df = recalculate_recs(df)
    df["field_update"] = df["adjusted_adds"] - df["recommended_removals"]

    # if "Ville-Marie" in neighborhood_selected:
    #     import numpy as np
    #     np.where(df["neighborhood"].str.contains('Ville-Marie'), df['field_update'].div(10), df['field_update'])
    #     df["field_update"] = df["field_update"].astype(int)

    df_add = (
        df[df["adjusted_adds"] > 0]
        .sort_values(by="adjusted_adds", ascending=False)
        .head(10)
    )
    df_add = df_add.loc[:, ["code", "name", "field_update"]]
    df_add = df_add.rename(
        columns={"code": "Station Code", "name": "Location", "field_update": "Bikes"}
    )
    df_remove = (
        df[df["recommended_removals"] > 0]
        .sort_values(by="recommended_removals", ascending=False)
        .head(10)
    )
    df_remove = df_remove.loc[:, ["code", "name", "field_update"]]
    df_remove = df_remove.rename(
        columns={"code": "Station Code", "name": "Location", "field_update": "Bikes"}
    )

    remove_planning_table = ddk.DataTable(
        df_remove.to_dict("records"),
        [
            {"name": "Station Code", "id": "Station Code"},
            {"name": "Location", "id": "Location"},
            {
                "name": "Bikes",
                "id": "Bikes",
                "editable": True,
                "type": "numeric",
            },
        ],
        id="fleet-remove-table",
        style_header={
            "backgroundColor": "#131416",
            "text-align": "left",
            "border": "0px",
            "font-size": "smaller",
            "font-weight": "bolder",
        },
        style_data={
            "color": "white",
            "backgroundColor": "inherit",
            "whiteSpace": "normal",
            "height": "auto",
            "text-align": "left",
            "border": "0px",
            "font-size": "medium",
            "color": "rgb(162, 170, 184)",
            "padding-top": "10px",
            "padding-bottom": "10px",
        },
        style_table={
            "padding-left": "5%",
            "padding-right": "5%",
            "padding-top": "20px",
            "padding-bottom": "20px",
            "width": "42vw",
            "height": "30vh",
            "overflowY": "auto",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "background-color": "rgb(38 38 38)"},
            {"if": {"column_id": "Bikes"}, "color": "#ff2c6d"},
            {
                "if": {"column_id": ["Bikes", "Station Code"]},
                "text-align": "center",
            },
            {
                "if": {"column_id": "Location"},
                "padding-left": "10px",
            },
            {
                "if": {"state": "active"},  # 'active' | 'selected'
                "background-color": "inherit",
                "border": "1px solid #978bf2",
            },
        ],
        style_cell_conditional=[
            {"if": {"column_id": "Station Code"}, "width": "25%"},
            {"if": {"column_id": "Location"}, "width": "50%"},
            {"if": {"column_id": "Bikes"}, "width": "25%"},
        ],
        style_header_conditional=[
            {
                "if": {"column_id": ["Bikes", "Station Code"]},
                "text-align": "center",
            },
        ],
        # fill_width=False,
    )

    add_planning_table = ddk.DataTable(
        df_add.to_dict("records"),
        [
            {"name": "Station Code", "id": "Station Code"},
            {"name": "Location", "id": "Location"},
            {
                "name": "Bikes",
                "id": "Bikes",
                "editable": True,
                "type": "numeric",
            },
        ],
        id="fleet-add-table",
        style_header={"display": "none"},
        style_data={
            "color": "white",
            "backgroundColor": "inherit",
            "whiteSpace": "normal",
            "height": "auto",
            "text-align": "left",
            "border": "0px",
            "font-size": "medium",
            "color": "rgb(162, 170, 184)",
            "padding-top": "10px",
            "padding-bottom": "10px",
        },
        style_table={
            "padding-left": "5%",
            "padding-right": "5%",
            "padding-top": "20px",
            "padding-bottom": "20px",
            "width": "42vw",
            "height": "30vh",
            "overflowY": "auto",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "background-color": "rgb(38 38 38)"},
            {"if": {"column_id": "Bikes"}, "color": "#978bf2"},
            {
                "if": {"column_id": ["Bikes", "Station Code"]},
                "text-align": "center",
            },
            {
                "if": {"column_id": "Location"},
                "padding-left": "10px",
            },
            {
                "if": {"state": "active"},  # 'active' | 'selected'
                "background-color": "inherit",
                "border": "1px solid #978bf2",
            },
        ],
        style_cell_conditional=[
            {"if": {"column_id": "Station Code"}, "width": "25%"},
            {"if": {"column_id": "Location"}, "width": "50%"},
            {"if": {"column_id": "Bikes"}, "width": "25%"},
        ],
    )

    df_add["Action"] = "Add"
    df_remove["Action"] = "Remove"

    df_both = df_add.append(df_remove)
    df_both = df_both.reset_index()

    return (
        html.Div(
            [
                html.Span("Stations to remove bikes", style={"padding-left": "5%"})
                if len(df_remove) > 0
                else html.Span("No bikes to remove", style={"padding-left": "5%"}),
                remove_planning_table
                if len(df_remove) > 0
                else ddk.DataTable(id="fleet-remove-table", data=None),
                html.Br(),
                html.Span("Stations to add bikes", style={"padding-left": "5%"})
                if len(df_add) > 0
                else html.Span("No bikes to add", style={"padding-left": "5%"}),
                add_planning_table
                if len(df_add) > 0
                else ddk.DataTable(id="fleet-add-table", data=None),
            ]
        ),
        df_both,
    )


def get_kpis():
    return ddk.Row(
        [
            ddk.DataCard(
                value=f"{trips_gained:,.0f}",
                label="Est. Trips Gained",
                border_width="0px",
            ),
            ddk.DataCard(
                value=f"${revenue_gained:,.0f}",
                label="Est. Revenue Gained",
                border_width="0px",
            ),
            ddk.DataCard(
                value=f"${total_rebalancing_cost:,.0f}",
                label="Est. Rebalancing Cost",
                border_width="0px",
            ),
            ddk.DataCard(
                value=f"${profit:,.0f}", label="Est. Profit", border_width="0px"
            ),
        ]
    )


PERFORMANCE_REPORT_MODAL = html.Div(
    id="snapshot-modal-content",
    style={
        "width": "30%",
    },
    children=[
        html.P("Enter Report Name"),
        dcc.Input(
            id="modal-report-title",
            placeholder="Enter..",
        ),
        html.Div(style={"height": "30px"}),
        html.P("User Name (optional)"),
        dcc.Input(
            id="modal-report-username",
            placeholder="Enter..",
        ),
        html.Div(style={"height": "30px"}),
        html.P("Select Neighborhood (optional)"),
        dcc.Dropdown(neighborhood_list, id="modal-neighborhood"),
        html.Div(style={"height": "30px"}),
        html.Button("Submit", id="take-snapshot"),
    ],
)
