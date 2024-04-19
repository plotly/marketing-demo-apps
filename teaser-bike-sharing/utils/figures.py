import copy
from statistics import mean

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from constants import MAPBOX_ACCESS_TOKEN, hourly_data, performance

from utils.utils import (
    get_arrow_char,
    normalize_data,
    process_performance_data,
    zoom_center,
)

# MAPBOX STYLE - carto-darkmatter, carto-positron, open-street-map, stamen-terrain, stamen-toner, stamen-watercolor, white-bg


def aggregated_activity(time, neighborhood=None):
    """
    Depending on the selection 'rental_rates_type', a bar chart will be generated with the hour/weekday/month/year grouping, further grouped by their membership.
    If 'membership' is selected we create a slightly different chart that displays the number of rentals/duration of rentals per membership type.
    """
    data = hourly_data

    if neighborhood:
        data = data.loc[data["neighborhood"] == neighborhood]
    xaxis = None

    data = data.groupby([time]).agg({"departures": ["sum"], "arrivals": ["sum"]})
    data.columns = ["Departures", "Arrivals"]
    data = data.reset_index()
    xaxis = {
        "hour": {"categoryorder": "array", "categoryarray": list(range(0, 24))},
        "weekday": {
            "categoryorder": "array",
            "categoryarray": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
        },
        "month": {
            "categoryorder": "array",
            "categoryarray": [
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
            ],
        },
        "year": {"type": "category"},
    }
    xaxis = xaxis[time]
    fig = px.bar(data, x=time, y=["Departures", "Arrivals"])
    fig.update_layout(xaxis=xaxis)
    fig.update_yaxes(title="Count")

    fig.update_xaxes(title=None)
    fig.update_traces(hovertemplate="Hour %{x} - %{value} <br>")
    fig.update_layout(legend_title="")

    return fig


def overview_map(data_stations, data_neighborhoods_json, neighborhood_selected=None):

    df = performance.groupby("neighborhood").sum().reset_index()
    data = pd.merge(data_stations, df, how="outer", on="neighborhood")
    data.rename(columns={"excess_arrivals": "Excess Arrivals"}, inplace=True)

    if not neighborhood_selected:

        fig = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods_json,
            locations="neighborhood",
            featureidkey="properties.NOM",
            center={"lat": 45.5517, "lon": -73.7073},
            color="Excess Arrivals",
            zoom=9,
            custom_data=["neighborhood", "Excess Arrivals"],
        )
        fig.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br><br>Excess Arrivals: %{customdata[1]:,}",
        )
    else:
        data = hourly_data.query("neighborhood == @neighborhood_selected")
        data = data.groupby(["station_code"]).agg(
            {
                "departures": ["sum"],
                "arrivals": ["sum"],
                "lat": "median",
                "lon": "median",
                "name": "first",
            }
        )
        data["size"] = abs(data["arrivals"] - data["departures"])
        data["count"] = data["arrivals"] - data["departures"]

        data["sign"] = data["count"].apply(
            lambda x: "More Arrivals"
            if x > 0
            else ("More Departures" if x < 0 else "Equal")
        )
        data["color"] = data["sign"].map(
            {
                "More Departures": "var(--colorway-0)",
                "More Arrivals": "var(--colorway-1)",
                "Equal": "var(--colorway-2)",
            }
        )

        data = data.dropna().reset_index()
        data.columns = data.columns.droplevel(1)
        zoom, center = zoom_center(lats=data["lat"], lons=data["lon"])
        fig = px.scatter_mapbox(
            data_frame=data,
            lat=data["lat"],
            lon=data["lon"],
            size=data["size"],
            color=data["sign"],
            zoom=zoom,
            center=center,
            color_discrete_map={
                "More Departures": "var(--colorway-0)",
                "More Arrivals": "var(--colorway-1)",
                "Equal": "var(--colorway-2)",
            },
            custom_data=["name", "departures", "arrivals"],
        )
        fig.update_traces(hovertemplate="", hoverinfo="none")

        fig.update_layout(coloraxis_showscale=False)

        ## remove the selected neighborhood from the map
        data = data_stations.query("neighborhood != @neighborhood_selected")
        data_neighborhoods = copy.deepcopy(data_neighborhoods_json)
        features = [
            neighborhood
            for neighborhood in data_neighborhoods["features"]
            if neighborhood["properties"]["NOM"] != neighborhood_selected
        ]
        data_neighborhoods["features"] = features

        fig_neighborhoods = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods,
            opacity=0.25,
            locations="neighborhood",
            featureidkey="properties.NOM",
            custom_data=["name"],
        )

        fig_neighborhoods.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br>",
        )
        fig.add_trace(fig_neighborhoods.data[0])
        fig.update_layout(legend_title="")
    return fig


def fleet_managment_map(
    data_stations,
    data_neighborhoods_json,
    df_add_remove=None,
    neighborhood_selected=None,
):

    if not neighborhood_selected:
        df = performance.groupby("neighborhood").sum().reset_index()
        data = pd.merge(data_stations, df, how="outer", on="neighborhood")
        data.rename(columns={"excess_arrivals": "Excess Arrivals"}, inplace=True)

        fig = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods_json,
            locations="neighborhood",
            featureidkey="properties.NOM",
            center={"lat": 45.5517, "lon": -73.7073},
            color="Excess Arrivals",
            zoom=9,
            custom_data=["neighborhood", "Excess Arrivals"],
        )
        fig.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br><br>Excess Arrivals: %{customdata[1]:,}",
        )
    else:
        data = pd.merge(
            data_stations,
            df_add_remove,
            how="inner",
            left_on="name",
            right_on="Location",
        )
        data.rename(columns={"excess_arrivals": "Excess Arrivals"}, inplace=True)
        data["Bikes"] = data["Bikes"].abs()
        data["color"] = data["Action"].map(
            {"Remove": "var(--colorway-1)", "Add": "var(--colorway-0)"}
        )

        zoom, center = zoom_center(lats=data["latitude"], lons=data["longitude"])
        fig = px.scatter_mapbox(
            data_frame=data,
            lat=data["latitude"],
            lon=data["longitude"],
            size=data["Bikes"],
            color=data["Action"],
            zoom=zoom,
            center=center,
            color_discrete_map={
                "Add": "var(--colorway-0)",
                "Remove": "var(--colorway-1)",
            },
            custom_data=["name", "Bikes", "Action", "color"],
        )
        fig.update_traces(
            hoverinfo="name",
            hovertemplate="<b>%{customdata[0]}</b><br><br><span style='color:%{customdata[3]}'>%{customdata[2]} %{customdata[1]} bikes </span> <extra></extra>",
        )

        ## remove the selected neighborhood from the map
        data = data_stations.query("neighborhood not in @neighborhood_selected")
        data_neighborhoods = copy.deepcopy(data_neighborhoods_json)
        features = [
            neighborhood
            for neighborhood in data_neighborhoods["features"]
            if neighborhood["properties"]["NOM"] != neighborhood_selected
        ]
        data_neighborhoods["features"] = features

        fig_neighborhoods = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods,
            opacity=0.25,
            locations="neighborhood",
            featureidkey="properties.NOM",
            custom_data=["name"],
        )

        fig_neighborhoods.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br>",
        )
        fig.add_trace(fig_neighborhoods.data[0])
        fig.update_layout(legend_title="")
    return fig


def performance_map(data_stations, data_neighborhoods_json, neighborhood_selected=None):

    if not neighborhood_selected:
        df = process_performance_data()[0]
        df = df.groupby("neighborhood").sum().reset_index()
        data = pd.merge(data_stations, df, how="outer", on="neighborhood")
        data.rename(columns={"effective_moves": "Effective Moves"}, inplace=True)
        data["Est. Revenue Gained"] = data["Effective Moves"] * 2.02

        fig = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods_json,
            locations="neighborhood",
            featureidkey="properties.NOM",
            center={"lat": 45.5517, "lon": -73.7073},
            color="Est. Revenue Gained",
            zoom=9,
            custom_data=["neighborhood", "Est. Revenue Gained"],
            color_continuous_scale=["var(--colorway-0)", "var(--colorway-1)"],
        )
        fig.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br><br>Est. Revenue Gained: $%{customdata[1]:,.0f}",
        )
    else:
        data = hourly_data.query("neighborhood == @neighborhood_selected")
        data = data.groupby(["station_code"]).agg(
            {
                "departures": ["sum"],
                "arrivals": ["sum"],
                "lat": "median",
                "lon": "median",
                "name": "first",
            }
        )
        data["size"] = abs(data["arrivals"] + data["departures"])
        data["count"] = data["arrivals"] - data["departures"]
        data["sign"] = data["count"].apply(
            lambda x: "More Arrivals"
            if x > 0
            else ("More Departures" if x < 0 else "Equal")
        )
        data["color"] = data["sign"].map(
            {
                "More Departures": "var(--colorway-0)",
                "More Arrivals": "var(--colorway-1)",
                "Equal": "var(--colorway-2)",
            }
        )

        data = data.dropna().reset_index()
        data.columns = data.columns.droplevel(1)
        zoom, center = zoom_center(lats=data["lat"], lons=data["lon"])
        fig = px.scatter_mapbox(
            data_frame=data,
            lat=data["lat"],
            lon=data["lon"],
            size=data["size"],
            color=data["sign"],
            zoom=zoom,
            center=center,
            color_discrete_map={
                "More Departures": "var(--colorway-0)",
                "More Arrivals": "var(--colorway-1)",
                "Equal": "var(--colorway-2)",
            },
            custom_data=["name", "departures", "arrivals", "color"],
        )
        fig.update_traces(
            hoverinfo="name",
            hovertemplate="<b style='color:%{customdata[3]}'>%{customdata[0]}</b> <br>Departures: %{customdata[1]} <br>Arrivals: %{customdata[2]} <extra></extra>",
        )

        ## remove the selected neighborhood from the map
        data = data_stations.query("neighborhood != @neighborhood_selected")
        data_neighborhoods = copy.deepcopy(data_neighborhoods_json)
        features = [
            neighborhood
            for neighborhood in data_neighborhoods["features"]
            if neighborhood["properties"]["NOM"] != neighborhood_selected
        ]
        data_neighborhoods["features"] = features

        fig_neighborhoods = px.choropleth_mapbox(
            data,
            geojson=data_neighborhoods,
            opacity=0.25,
            locations="neighborhood",
            featureidkey="properties.NOM",
            custom_data=["name"],
        )

        fig_neighborhoods.update_traces(
            hoverinfo="name",
            hovertemplate="%{customdata[0]}<br>",
        )
        fig_neighborhoods.update_layout(
            showlegend=False
        )  ## TODO: does not hide the legend of this trace, other places too

        fig.add_trace(fig_neighborhoods.data[0])
        fig.update_layout(legend_title="")
    return fig


def daily_usage(data):
    """
    Creates a time series chart displayed on hover on the neighborhood map.
    """
    return px.line(data, x="date", y="sum")


def daily_arrivals_departures(data):
    """
    Creates a pie chart displayed on hover on the neighborhood map.
    """
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Departures", "Arrivals"], values=[data[1], data[2]], hole=0.3
            )
        ]
    )

    fig.update_traces(
        marker=dict(colors=["var(--colorway-0)", "var(--colorway-1)"]), hoverinfo="skip"
    )
    fig.update_layout(
        width=250,
        height=250,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def map_top_stations(data, data_stations, group_type, number_of_stations=10):
    """
    Depending on the selection 'group_type' data will be grouped by the corresponding grouping.
    And then map is created displaying the top 'number_of_stations' stations.
    """
    if group_type == "fee":
        data = (
            data.groupby(["start_station_code"])
            .agg({"start_station_code": "count", "duration_sec": "sum", "fee": "sum"})
            .rename(
                columns={
                    "start_station_code": "num_of_rides",
                    "duration_sec": "tot_duration",
                }
            )
            .reset_index()
            .sort_values(by=["fee"], ascending=False)
            .head(number_of_stations)
        )
    elif group_type == "number_of_rides":
        data = (
            data.groupby(["start_station_code"])
            .agg({"start_station_code": "count", "duration_sec": "sum"})
            .rename(
                columns={
                    "start_station_code": "num_of_rides",
                    "duration_sec": "tot_duration",
                }
            )
            .reset_index()
            .sort_values(by=["num_of_rides"], ascending=False)
            .head(number_of_stations)
        )
    elif group_type == "duration":
        data = (
            data.groupby(["start_station_code"])
            .agg({"start_station_code": "count", "duration_sec": "sum"})
            .rename(
                columns={
                    "start_station_code": "num_of_rides",
                    "duration_sec": "tot_duration",
                }
            )
            .reset_index()
            .sort_values(by=["tot_duration"], ascending=False)
            .head(number_of_stations)
        )
    elif group_type == "number_of_round_trips":
        data = (
            data.groupby(["start_station_code", "end_station_code"])
            .agg({"start_station_code": "count", "duration_sec": "sum"})
            .rename(
                columns={
                    "start_station_code": "num_of_rides",
                    "duration_sec": "tot_duration",
                }
            )
            .query("start_station_code == end_station_code")
            .reset_index()
            .sort_values(by=["num_of_rides"], ascending=False)
            .head(number_of_stations)
        )

    ## merge with stations data to get lat/lon/name
    data = pd.merge(
        data, data_stations, left_on="start_station_code", right_on="code"
    ).drop(columns=["start_station_code"])

    ## depending on the group_type, create different hover_text and departure_marker_size
    ## departure_marker_size - * 20 size seems good and base + 5 to make the smallest marker more visible
    if group_type == "fee":
        hover_text = data.apply(
            lambda x: x["name"]
            + "<br><br>"
            + "$"
            + str(round(x["fee"], 1))
            + "<extra></extra>",
            axis=1,
        )
        departure_marker_size = (normalize_data(data["fee"]) * 20) + 5
    elif group_type == "number_of_rides":
        departure_marker_size = (normalize_data(data["num_of_rides"]) * 20) + 5
        hover_text = data.apply(
            lambda x: x["name"]
            + "<br><br>"
            + f"{x['num_of_rides']:,}"
            + "<extra></extra>",
            axis=1,
        )
    elif group_type == "duration":
        hover_text = data.apply(
            lambda x: x["name"]
            + "<br><br>"
            + str(round(x["tot_duration"] / 3600, 2))
            + " hours"
            + "<br>"
            + f"{x['num_of_rides']:,}"
            + " rides"
            + "<extra></extra>",
            axis=1,
        )
        departure_marker_size = (normalize_data(data["tot_duration"]) * 20) + 5
    elif group_type == "number_of_round_trips":
        departure_marker_size = (normalize_data(data["num_of_rides"]) * 20) + 5
        hover_text = data.apply(
            lambda x: x["name"]
            + "<br><br>"
            + f"{x['num_of_rides']:,}"
            + "<extra></extra>",
            axis=1,
        )

    fig = go.Figure(
        go.Scattermapbox(
            lat=data["latitude"],
            lon=data["longitude"],
            hovertemplate=hover_text,
            mode="markers",
            marker=dict(
                size=departure_marker_size,
                color="blue",
            ),
            name=None,
        )
    )

    ## TODO read me
    ## stuff above generates map with only DEPARTURE stations (merge on start_station_code)
    ## here I made a code that adds DESTINATION station (merge on end_station_code) to the map
    ## as well as a line between the two stations
    ## as well as an arrow poiting from the departure station to the destination station
    ## I removed this because it did not fit into the overview page map, but it might be useful somewhere else
    ## to use it somewhere else you will need to merge
    ## data = pd.merge(data, data_stations, left_on="end_station_code", right_on="code").drop(columns=["end_station_code"])
    ## and sort out suffixes so that the code works
    if group_type in []:
        fig.add_trace(
            go.Scattermapbox(
                lat=data["latitude"],
                lon=data["longitude"],
                mode="markers",
                marker=dict(
                    size=departure_marker_size,
                    color="green",
                ),
                name="Destination",
            )
        )

        for idx, row in data.iterrows():
            lats = [row["latitude"], row["latitude"]]
            lons = [row["longitude"], row["longitude"]]

            ## add LINE between departure and destination stations
            fig.add_trace(
                go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode="lines",
                    line=dict(
                        width=1,
                        color="black",
                    ),
                    showlegend=False,
                )
            )

            ## add ARROW direction from departure to destination station
            halfway = [mean(lats), mean(lons)]
            fig.add_trace(
                go.Scattermapbox(
                    mode="text",
                    lat=[halfway[0]],
                    lon=[halfway[1]],
                    text=get_arrow_char(lats, lons),
                    textfont=dict(size=30, color="red"),
                    showlegend=False,
                )
            )

    fig.update_layout(
        hovermode="closest",
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center={"lat": 45.504156, "lon": -73.580417},
            zoom=10.5,
            style="carto-darkmatter",
        ),
        margin=dict(r=0, t=0, l=0, b=0),
    )
    return fig


def simulating_new_locations_map(data, number_of_stations=25):
    """
    Creates a map with info where to create new locations.
    Also returns a data for the table.
    """

    df = pd.DataFrame(data["data"], columns=data["columns"]).head(number_of_stations)

    ## create hover_text and departure_marker_size for the markers
    departure_marker_size = (normalize_data(len(df) - df["priority"]) * 20) + 5
    hover_text = df.apply(
        lambda x: f"Out of {len(df)} locations, this location is prioririty:<br><br> {int(x['priority'])} <extra></extra>",
        axis=1,
    )

    fig = go.Figure(
        go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            hovertemplate=hover_text,
            mode="markers",
            marker=dict(
                size=departure_marker_size,
                color="blue",
            ),
            name=None,
        )
    )

    fig.update_layout(
        hovermode="closest",
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center={"lat": 45.504156, "lon": -73.580417},
            zoom=10.5,
            style="carto-darkmatter",
        ),
        margin=dict(r=0, t=0, l=0, b=0),
    )

    ## transform df into table data
    table_data = df.to_dict("records")
    table_cols = [{"headerName": i.capitalize(), "field": i} for i in df.columns]

    return fig, table_data, table_cols


def simulating_new_parking_slots_map(data, data_stations, additional_capacity):
    """
    Creates a map with info where to add more parking slots.
    Also returns a data for the table.
    """

    ## This arbitrarily selects top 30 stations to be used for adding new stations
    data = (
        data.groupby(["start_station_code"])
        .agg({"start_station_code": "count", "duration_sec": "sum"})
        .rename(
            columns={
                "start_station_code": "num_of_rides",
                "duration_sec": "tot_duration",
            }
        )
        .reset_index()
        .sort_values(by=["num_of_rides"], ascending=False)
        .head(30)
    )
    data = pd.merge(
        data, data_stations, left_on="start_station_code", right_on="code"
    ).drop(columns=["start_station_code"])

    ## arbitrarily say that 33% of the current parking slots capacity should be added to make it more efficient
    data["needed_additional_capacity"] = (data["capacity"] * 0.33).astype(int)

    ## following code selects stations until the 'needed_additional_capacity' adds up to the user-selected 'additional_capacity'
    data["cumsum"] = data["needed_additional_capacity"].cumsum()
    df = data.query("cumsum <= @additional_capacity")
    if df.empty:
        df = data.iloc[0].to_frame().T
        df["needed_additional_capacity"] = additional_capacity
    else:
        second_to_last_index = df.index[-1]
        second_to_last_value = data.iloc[second_to_last_index]["cumsum"]

        last_data_point = data.iloc[second_to_last_index + 1]
        last_data_point["needed_additional_capacity"] = (
            additional_capacity - second_to_last_value
        )

        df = pd.concat([df, last_data_point.to_frame().T])

    df = df[["name", "needed_additional_capacity", "longitude", "latitude"]]

    ## priority is used to determine the size of the marker
    df["priority"] = df.index.values + 1

    ## create hover_text and departure_marker_size for the markers
    departure_marker_size = (normalize_data(len(df) - df["priority"]) * 20) + 5
    hover_text = df.apply(
        lambda x: f"Out of {len(df)} locations, this location is prioririty {int(x['priority'])}, and requires <br><br> {x['needed_additional_capacity']} new parking slots <extra></extra>",
        axis=1,
    )

    fig = go.Figure(
        go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            hovertemplate=hover_text,
            mode="markers",
            marker=dict(
                size=departure_marker_size,
                color="blue",
            ),
            name=None,
        )
    )

    fig.update_layout(
        hovermode="closest",
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center={"lat": 45.504156, "lon": -73.580417},
            zoom=10.5,
            style="carto-darkmatter",
        ),
        margin=dict(r=0, t=0, l=0, b=0),
    )

    ## transform df into table data
    table_data = df.to_dict("records")
    table_cols = [{"headerName": i.capitalize(), "field": i} for i in df.columns]

    return fig, table_data, table_cols
