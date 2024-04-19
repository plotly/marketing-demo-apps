import dash
from dash import Input, Output, State, callback, ctx, dcc, html
import dash_design_kit as ddk
import dash_mantine_components as dmc


import utils.figures as figs
from utils.components import get_fleet_movement_layout
from constants import df_stations, neighborhood_list, neighborhoods

dash.register_page(
    __name__, title="Fleet Movement Planning", path="/fleet_movement_planning"
)


def layout():
    return html.Div(
        [
            dcc.Store(id="field-update-mods", storage_type="memory", data={}),
            ddk.Row(
                [
                    ddk.Card(
                        [
                            ddk.CardHeader(title="Neighborhood Map"),
                            dmc.MultiSelect(
                                id="fleet-planning-map-dropdown",
                                clearable=True,
                                searchable=True,
                                data=[
                                    {"label": i, "value": i} for i in neighborhood_list
                                ],
                                placeholder="Select neighborhoods",
                            ),
                            dmc.LoadingOverlay(
                                ddk.Graph(
                                    id="fleet-planning-map", clear_on_unhover=True
                                ),
                                overlayOpacity=0.75,
                                overlayColor="#1D2022",
                                loaderProps=dict(color="violet", variant="bars"),
                            ),
                        ],
                        width=50,
                    ),
                    ddk.Card(
                        [
                            ddk.CardHeader(
                                title="Fleet Movement Planning",
                                children=html.Button(
                                    id="recalculate-button", children="Recalculate"
                                ),
                            ),
                            ddk.Block(
                                id="fleet-planning-planning",
                                children=[
                                    html.Div(
                                        "Select a neighborhood",
                                        style={
                                            "text-align": "center",
                                            "color": "#a2aab8",
                                            "font-size": "smaller",
                                            "position": "relative",
                                            "top": "40%",
                                            "transform": "translateY(-40%)",
                                        },
                                    ),
                                    ddk.DataTable(id="fleet-remove-table"),
                                    ddk.DataTable(id="fleet-add-table"),
                                ],
                            ),
                        ],
                        width=50,
                    ),
                ]
            ),
        ]
    )


@callback(
    Output("fleet-planning-map-dropdown", "value"),
    Input("fleet-planning-map", "clickData"),
    State("fleet-planning-map-dropdown", "value"),
)
def update_neighbourhood_dropdown(clickData, dropdown):
    if clickData is not None:
        if dropdown is not None:
            return dropdown + [clickData["points"][0]["location"]]
        return [clickData["points"][0]["location"]]


@callback(
    Output("fleet-planning-map", "figure"),
    Output("fleet-planning-planning", "children"),
    Output("field-update-mods", "data"),
    Input("fleet-planning-map-dropdown", "value"),
    Input("recalculate-button", "n_clicks"),
    State("fleet-add-table", "data"),
    State("fleet-remove-table", "data"),
    State("field-update-mods", "data"),
)
def show_neighborhood_data(
    neighborhood_selected, n_clicks, add_values, remove_values, store
):
    triggered_id = ctx.triggered_id
    if not neighborhood_selected:
        fig = figs.fleet_managment_map(df_stations, neighborhoods)
        return (
            fig,
            [
                html.Div(
                    "Select neighborhoods",
                    style={
                        "text-align": "center",
                        "color": "#a2aab8",
                        "font-size": "smaller",
                    },
                ),
                ddk.DataTable(id="fleet-remove-table"),
                ddk.DataTable(id="fleet-add-table"),
            ],
            store,
        )

    if triggered_id == "recalculate-button":
        indexes = dict([(str(val["Station Code"]), val["Bikes"]) for val in add_values])
        store.update(indexes)
        indexes = dict(
            [(str(val["Station Code"]), val["Bikes"]) for val in remove_values]
        )
        store.update(indexes)

    fleet_movement_layout, df_add_remove = get_fleet_movement_layout(
        neighborhood_selected, store
    )
    fig = figs.fleet_managment_map(
        df_stations, neighborhoods, df_add_remove, neighborhood_selected
    )
    return fig, fleet_movement_layout, store
