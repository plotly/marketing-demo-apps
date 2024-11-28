import dash
from dash import Input, Output, State, callback, ctx, dcc, html
import dash_design_kit as ddk
import dash_mantine_components as dmc
from snap import snap

import utils.figures as figs
import utils.components as comps
from constants import df_stations, neighborhood_list, neighborhoods

dash.register_page(__name__, title="Performance Tracking", path="/performance")


def layout():
    return html.Div(
        [
            ## KPIs
            ddk.Card(
                [ddk.CardHeader(title="Whole-market performance"), comps.get_kpis()],
                style={"display": "flex", "padding": "0px", "width": "unset"},
            ),
            ## MAP
            ddk.Card(
                [
                    ddk.CardHeader(title="Neighborhood Map"),
                    dmc.Select(
                        id="performance-map-dropdown",
                        clearable=True,
                        searchable=True,
                        data=[{"label": i, "value": i} for i in neighborhood_list],
                        placeholder="Select neighborhood",
                    ),
                    dmc.LoadingOverlay(
                        ddk.Graph(id="performance-map", clear_on_unhover=True),
                        overlayOpacity=0.75,
                        overlayColor="#1D2022",
                        loaderProps=dict(color="violet", variant="bars"),
                    ),
                ],
                width=40,
            ),
            ## TABLE
            ddk.Card(
                [
                    ddk.CardHeader(title="Performance Tracking"),
                    html.Div(id="performance-tracking"),
                ],
                width=60,
            ),
            ## REPORT
            comps.PERFORMANCE_REPORT_MODAL,
            ddk.Row(
                [
                    ddk.Modal(
                        id="snapshot-btn-modal",
                        children=[
                            html.Button(
                                "Generate Report",
                                id="take-snapshot-button",
                                n_clicks=0,
                            ),
                        ],
                        target_id="snapshot-modal-content",
                        hide_target=True,
                    ),
                    dcc.Link(
                        href=dash.get_relative_path("/reports-archive"),
                        children="Past Reports",
                    ),
                ],
                style={
                    "position": "relative",
                    "align-items": "center",
                    "justify-content": "flex-end",
                    "gap": "30px",
                },
            ),
        ]
    )


@callback(
    Output("performance-map-dropdown", "value"), Input("performance-map", "clickData")
)
def update_neighbourhood_dropdown(clickData):
    if clickData is not None:
        return clickData["points"][0]["location"]


@callback(
    Output("performance-map", "figure"),
    Output("performance-tracking", "children"),
    Input("performance-map-dropdown", "value"),
)
def update_location_map(neighborhood_selected):
    map = figs.performance_map(df_stations, neighborhoods, neighborhood_selected)
    performance_table = comps.get_performance_tracking_layout(neighborhood_selected)
    return map, performance_table


@callback(
    Output("snapshot-btn-modal", "expanded"),
    Output("url", "pathname"),
    Input("take-snapshot", "n_clicks"),
    State("modal-neighborhood", "value"),
    State("modal-report-title", "value"),
    State("modal-report-username", "value"),
    prevent_initial_call=True,
)
def save_snapshot(n_clicks, neighborhood, title, username):
    triggered = ctx.triggered_id
    if triggered == "take-snapshot" and n_clicks:
        try:
            report_layout = dash.page_registry["pages.snapshot"]["layout"]
            snapshot_id = snap.snapshot_save(report_layout(neighborhood=neighborhood))
            title = "Default Title" if not title else title
            snap.meta_update(snapshot_id, {"report-title": title})
            username = "Default User" if not username else username
            snap.meta_update(snapshot_id, {"report-creator": username})
            return False, dash.get_relative_path("/reports-archive")
        except Exception as e:
            import traceback

            traceback.print_exc()
            return True, dash.no_update
    return dash.no_update, dash.no_update
