import dash
from dash import Input, Output, callback, dcc, html, no_update
import dash_design_kit as ddk
import dash_mantine_components as dmc

import utils.figures as figs
from constants import df, df_daily_usage, df_stations, neighborhood_list, neighborhoods

dash.register_page(__name__, title="Overview", path="/")


def layout():
    return html.Div(
        [
            ddk.Row(
                [
                    ddk.Card(
                        [
                            ddk.CardHeader(title="Neighborhood Map"),
                            dmc.Select(
                                id="overview-map-dropdown",
                                clearable=True,
                                searchable=True,
                                data=[
                                    {"label": i, "value": i} for i in neighborhood_list
                                ],
                                placeholder="Select neighborhood",
                            ),
                            dmc.LoadingOverlay(
                                ddk.Graph(id="overview-map", clear_on_unhover=True),
                                overlayOpacity=0.75,
                                overlayColor="#1D2022",
                                loaderProps=dict(color="violet", variant="bars"),
                            ),
                            dcc.Tooltip(
                                id="neighborhoods-map-tooltip", direction="bottom"
                            ),
                        ],
                        width=50,
                    ),
                    ddk.Card(
                        [
                            ddk.CardHeader(title="Data Overview and Exploration"),
                            dmc.SegmentedControl(
                                data=[
                                    {"value": "hour", "label": "Hour"},
                                    {"value": "weekday", "label": "Weekday"},
                                    {"value": "month", "label": "Month"},
                                    {"value": "year", "label": "Year"},
                                ],
                                color="dark",
                                value="hour",
                                fullWidth=True,
                                id="period-select",
                            ),
                            ddk.Graph(id="agg-activity"),
                        ],
                        width=50,
                    ),
                ]
            ),
            ddk.Card(
                [
                    ddk.CardHeader(title="Top Stations Statistics"),
                    dmc.SegmentedControl(
                        data=[
                            {"value": "fee", "label": "Fee"},
                            {"value": "number_of_rides", "label": "Number of Rides"},
                            {"value": "duration", "label": "Duration"},
                            {
                                "value": "number_of_round_trips",
                                "label": "Number of Round Trips",
                            },
                        ],
                        value="number_of_round_trips",
                        fullWidth=True,
                        id="top-stations-group-type",
                    ),
                    ddk.Graph(id="top-stations"),
                ],
            ),
        ]
    )


@callback(Output("overview-map-dropdown", "value"), Input("overview-map", "clickData"))
def update_neighbourhood_dropdown(clickData):
    if clickData is not None:
        return clickData["points"][0]["location"]


@callback(
    Output("overview-map", "figure"),
    Input("overview-map-dropdown", "value"),
)
def update_map(neighborhood_selected):
    return figs.overview_map(df_stations, neighborhoods, neighborhood_selected)


@callback(
    Output("neighborhoods-map-tooltip", "show"),
    Output("neighborhoods-map-tooltip", "bbox"),
    Output("neighborhoods-map-tooltip", "children"),
    Input("overview-map", "hoverData"),
)
def update_map_tooltip(hoverData):
    """
    On hover, show the tooltip with the neighborhood name, and a line graph of that neighborhood, showing number of rides per day.
    """
    if hoverData is None:
        return False, no_update, no_update

    hover_data = hoverData["points"][0]

    if "location" in hover_data:
        return False, no_update, no_update
        neighborhood = hover_data["location"]
        data = df_daily_usage.query("neighborhood == @neighborhood")

        ## TODO: add more information here
        return (
            True,
            hover_data["bbox"],
            ddk.Card(
                [
                    ddk.CardHeader(neighborhood),
                    ddk.Graph(figure=figs.daily_usage(data)),
                ],
                className="neighborhood-tooltip-card",
            ),
        )
    elif "customdata" in hover_data:
        depatutres_arrivals = hover_data["customdata"]
        neighborhood = depatutres_arrivals[0]

        ## TODO: add more information here
        return (
            True,
            hover_data["bbox"],
            ddk.Card(
                [
                    ddk.CardHeader(neighborhood),
                    ddk.Graph(
                        figure=figs.daily_arrivals_departures(depatutres_arrivals)
                    ),
                ],
                className="neighborhood-tooltip-card",
            ),
        )
    else:
        return False, no_update, no_update


@callback(
    Output("top-stations", "figure"),
    Input("top-stations-group-type", "value"),
)
def update_top_stations(group_type):
    return figs.map_top_stations(df, df_stations, group_type, 20)


@callback(
    Output("agg-activity", "figure"),
    Input("period-select", "value"),
    Input("overview-map-dropdown", "value"),
)
def update_aggregate_activity(period, neighborhood_selected):
    return figs.aggregated_activity(period, neighborhood_selected)
