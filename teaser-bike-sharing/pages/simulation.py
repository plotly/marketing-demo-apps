import dash
from dash import html, dcc, callback, Input, Output, State
import dash_design_kit as ddk
import dash_ag_grid as dag
import pandas as pd

import utils.figures as figs
from constants import df, df_stations, AGGRID_LICENCE
from data.model_data import best_new_locations

dash.register_page(__name__, title="Simulation", path="/simulation")


def layout():
    return html.Div(
        [
            ddk.Card(
                [
                    ddk.CardHeader("Adding New Locations"),
                    ddk.Block(
                        [
                            ddk.Graph(id="simulation-new-locations"),
                        ],
                        width=50,
                    ),
                    ddk.Block(
                        [
                            dcc.Slider(
                                id="new-locations-slider",
                                min=1,
                                max=25,
                                value=15,
                                step=1,
                                marks={1: {"label": "1"}, 25: {"label": "25"}},
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            dag.AgGrid(
                                id="new-locations-table",
                                licenseKey=AGGRID_LICENCE,
                                columnSize="sizeToFit",
                                rowSelection="single",
                            ),
                            html.Button("Download CSV", id="new-locations-csv"),
                            dcc.Download(id="download-new-locations-csv"),
                        ],
                        width=50,
                    ),
                ]
            ),
            ddk.Card(
                [
                    ddk.CardHeader(title="Adding Parking Spots to Existing Locations"),
                    ddk.Block(
                        [
                            dcc.Slider(
                                id="parking-slots-slider",
                                min=1,
                                max=200,
                                value=50,
                                step=1,
                                marks={
                                    1: {"label": "1"},
                                    100: {"label": "100"},
                                    200: {"label": "200"},
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            dag.AgGrid(
                                id="more-parking-slots-table",
                                licenseKey=AGGRID_LICENCE,
                                columnSize="sizeToFit",
                                rowSelection="single",
                            ),
                            html.Button("Download CSV", id="more-parking-slots-csv"),
                            dcc.Download(id="download-more-parking-slots-csv"),
                        ],
                        width=50,
                    ),
                    ddk.Block(
                        [
                            ddk.Graph(id="simulation-more-parking-slots"),
                        ],
                        width=50,
                    ),
                ],
                className="simulation-row",
            ),
        ],
        className="simulation-container",
    )


@callback(
    Output("simulation-new-locations", "figure"),
    Output("new-locations-table", "rowData"),
    Output("new-locations-table", "columnDefs"),
    Output("simulation-more-parking-slots", "figure"),
    Output("more-parking-slots-table", "rowData"),
    Output("more-parking-slots-table", "columnDefs"),
    Input("parking-slots-slider", "value"),
    Input("new-locations-slider", "value"),
)
def run_both_simulations(additional_capacity, new_locations):
    (
        location_fig,
        location_table_data,
        location_table_cols,
    ) = figs.simulating_new_locations_map(best_new_locations, new_locations)
    (
        parking_fig,
        parking_table_data,
        parking_table_cols,
    ) = figs.simulating_new_parking_slots_map(df, df_stations, additional_capacity)
    return (
        location_fig,
        location_table_data,
        location_table_cols,
        parking_fig,
        parking_table_data,
        parking_table_cols,
    )


@callback(
    Output("download-new-locations-csv", "data"),
    Input("new-locations-csv", "n_clicks"),
    State("new-locations-table", "rowData"),
    State("new-locations-table", "columnDefs"),
    prevent_initial_call=True,
)
def download_new_parking_locations_csv(n_clicks, rows, columns):
    df = pd.DataFrame(rows, columns=[c["field"] for c in columns])
    return dcc.send_data_frame(df.to_csv, "Dash_new_parking_locations.csv", index=False)


@callback(
    Output("download-more-parking-slots-csv", "data"),
    Input("more-parking-slots-csv", "n_clicks"),
    State("more-parking-slots-table", "rowData"),
    State("more-parking-slots-table", "columnDefs"),
    prevent_initial_call=True,
)
def download_additional_parking_slots_csv(n_clicks, rows, columns):
    df = pd.DataFrame(rows, columns=[c["field"] for c in columns])
    return dcc.send_data_frame(
        df.to_csv, "Dash_additional_parking_slots.csv", index=False
    )
