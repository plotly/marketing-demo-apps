import json, math

import numpy as np
import pandas as pd


def get_code_to_neighbor_mappings():
    df_stations = pd.read_csv("data/stations.csv", index_col=0)
    neighborhood_mapping = dict(df_stations[["code", "neighborhood"]].values)
    name_mapping = dict(df_stations[["code", "name"]].values)
    lat_mapping = dict(df_stations[["code", "latitude"]].values)
    lon_mapping = dict(df_stations[["code", "longitude"]].values)
    return neighborhood_mapping, name_mapping, lat_mapping, lon_mapping


def prepare_data():
    ### final
    neighborhoods = json.load(open("data/limadmin.json", encoding="utf-8"))

    df_stations = pd.read_csv("data/stations.csv", index_col=0)

    all_stations = pd.unique(df_stations["code"])

    neighborhood_list = pd.unique(df_stations["neighborhood"])
    ### not done - save the final  version and then load just that, no need to do this data prep every time
    df = pd.read_csv(
        "data/OD_2019-10.csv", nrows=100_00
    )  # TODO: remove nrows, it's here for speed during development
    # TODO : load all data at once, and then be sure to sort out all the possible issues it causes with the (line) charts, groupings, slowness etc..
    ## DATA SOURCE : https://www.kaggle.com/datasets/jackywang529/bixi-montreal-bikeshare-data
    mapping, _, _, _ = get_code_to_neighbor_mappings()
    df["neighborhood"] = df["start_station_code"].map(mapping)

    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    df["year"] = df["start_date"].dt.year
    df["month"] = df["start_date"].dt.month_name()
    df["weekday"] = df["start_date"].dt.day_name()
    df["hour"] = df["start_date"].dt.hour

    month_to_season = dict(
        zip(
            range(1, 13),
            [
                "winter",
                "winter",
                "spring",
                "spring",
                "spring",
                "summer",
                "summer",
                "summer",
                "fall",
                "fall",
                "fall",
                "winter",
            ],
        )
    )
    df["season"] = df["start_date"].dt.month.map(month_to_season)

    def calculate_fee(row):
        if row["is_member"]:
            if row["duration_sec"] >= 2700:
                return (
                    round((row["duration_sec"] - 2700) / 60) * 0.1
                )  # fee per min after 45 min
            else:
                return 0
        else:
            initial_fee = 1
            fee_per_min = round(row["duration_sec"] / 60) * 0.15
            return initial_fee + fee_per_min

    df["fee"] = df.apply(lambda x: calculate_fee(x), axis=1)
    df = df[
        df["start_station_code"].isin(all_stations)
        & df["end_station_code"].isin(all_stations)
    ]

    departures = (
        df.groupby("start_station_code")["start_date"]
        .count()
        .reset_index(name="count_departure")
    )
    arrivals = (
        df.groupby("end_station_code")["start_date"]
        .count()
        .reset_index(name="count_arrival")
    )
    df["is_member_str"] = df["is_member"].map({0: "No", 1: "Yes"})

    df_stations = pd.merge(
        df_stations, departures, left_on="code", right_on="start_station_code"
    ).drop(columns=["start_station_code"])
    df_stations = pd.merge(
        df_stations, arrivals, left_on="code", right_on="end_station_code"
    ).drop(columns=["end_station_code"])

    ## daily usage for each neighborhood
    df_daily_usage = df
    df_daily_usage["date"] = df_daily_usage["start_date"].dt.date
    df_daily_usage = (
        df_daily_usage.groupby(["date", "start_station_code"])["duration_sec"]
        .agg(["count"])
        .reset_index()
    )
    df_daily_usage["date"] = pd.to_datetime(df_daily_usage["date"])
    df_daily_usage["season"] = df_daily_usage["date"].dt.month.map(month_to_season)
    df_daily_usage = pd.merge(
        df_daily_usage,
        df_stations[["neighborhood", "code"]],
        left_on="start_station_code",
        right_on="code",
        how="left",
    ).drop(["start_station_code", "code"], axis=1)
    df_daily_usage = (
        df_daily_usage.groupby(["date", "neighborhood"])["count"]
        .agg(["sum"])
        .reset_index()
    )

    return df, df_stations, neighborhoods, neighborhood_list, df_daily_usage


def rental_stats(df, neighborhood=None):
    if neighborhood:
        df = df.loc[df["neighborhood"] == neighborhood]
    data = df.groupby("is_member")["duration_sec"].agg(["count", "sum"])
    not_member_times_rented, not_member_total_duration = data.iloc[0][["count", "sum"]]
    member_times_rented, member_total_duration = data.iloc[1][["count", "sum"]]

    total_rentals = member_times_rented + not_member_times_rented
    total_duration = member_total_duration + not_member_total_duration

    rental_non_members_rate = (
        not_member_times_rented / total_rentals * 100
    )  # rental rate for non members
    duration_non_members_rate = (
        not_member_total_duration / total_duration * 100
    )  # duration rate for non members

    rental_members_rate = (
        member_times_rented / total_rentals * 100
    )  # rental rate for members
    duration_members_rate = (
        member_total_duration / total_duration * 100
    )  # duration rate for members

    return (
        not_member_times_rented,
        member_times_rented,
        not_member_total_duration,
        member_total_duration,
        rental_non_members_rate,
        duration_non_members_rate,
        rental_members_rate,
        duration_members_rate,
    )


def normalize_data(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def get_arrow_char(lats, lons):
    if lats[0] > lats[1]:
        if lons[0] > lons[1]:
            return "↙"
        else:
            return "↘"
    else:
        if lons[0] > lons[1]:
            return "↖"
        else:
            return "↗"


def zoom_center(
    lons: tuple = None,
    lats: tuple = None,
    lonlats: tuple = None,
    format: str = "lonlat",
    projection: str = "mercator",
    width_to_height: float = 2.0,
):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434

    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    lonlats: tuple, optional, gps locations
    format: str, specifying the order of longitud and latitude dimensions,
        expected values: 'lonlat' or 'latlon', only used if passed lonlats
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.

    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys

    """
    if lons is None and lats is None:
        if isinstance(lonlats, tuple):
            lons, lats = zip(*lonlats)
        else:
            raise ValueError("Must pass lons & lats or lonlats")

    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        "lon": round((maxlon + minlon) / 2, 6),
        "lat": round((maxlat + minlat) / 2, 6),
    }

    # longitudinal range by zoom level (20 to 1) in degrees, if centered at equator
    lon_zoom_range = np.array(
        [
            0.0007,
            0.0014,
            0.003,
            0.006,
            0.012,
            0.024,
            0.048,
            0.096,
            0.192,
            0.3712,
            0.768,
            1.536,
            3.072,
            6.144,
            11.8784,
            23.7568,
            47.5136,
            98.304,
            190.0544,
            360.0,
        ]
    )

    if projection == "mercator":
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2) - 2
    else:
        raise NotImplementedError(f"{projection} projection is not implemented")

    return zoom, center


def get_today_data():
    today_data = pd.read_csv("data/sept_20_recommendations.csv")
    return today_data


def get_hourly_data():
    # hourly_data = pd.read_csv("data/hourly_station_trips_2019.csv")

    ##Df Created
    # hourly_data['station_code'] = pd.to_numeric(hourly_data['station_code'], errors = 'coerce', downcast="integer")

    # hourly_data.dropna(subset = ['station_code'], inplace=True)
    # neighbor_mapping, name_mapping, lat_mapping, lon_mapping = get_code_to_neighbor_mappings()
    # hourly_data['neighborhood'] = hourly_data['station_code'].astype(int).map(neighbor_mapping)
    # hourly_data['lat'] = hourly_data['station_code'].astype(int).map(lat_mapping)
    # hourly_data['lon'] = hourly_data['station_code'].astype(int).map(lon_mapping)
    # hourly_data['name'] = hourly_data['station_code'].astype(int).map(name_mapping)
    # hourly_data['hour'] = pd.to_datetime(hourly_data['hour'])
    # hourly_data['year'] = hourly_data['hour'].dt.year
    # hourly_data['month'] = hourly_data['hour'].dt.month_name()
    # hourly_data['weekday'] = hourly_data['hour'].dt.day_name()
    # hourly_data['hour'] = hourly_data['hour'].dt.hour
    # hourly_data.to_csv("data/hourly_data.csv", index=False)

    # return hourly_data

    hourly_data = pd.read_csv("data/hourly_station_trips_2019.csv")

    # Df Created

    hourly_data["station_code"] = pd.to_numeric(
        hourly_data["station_code"], errors="coerce", downcast="integer"
    )

    hourly_data.dropna(subset=["station_code"], inplace=True)
    (
        neighbor_mapping,
        name_mapping,
        lat_mapping,
        lon_mapping,
    ) = get_code_to_neighbor_mappings()
    hourly_data["neighborhood"] = (
        hourly_data["station_code"].astype(int).map(neighbor_mapping)
    )
    hourly_data["lat"] = hourly_data["station_code"].astype(int).map(lat_mapping)
    hourly_data["lon"] = hourly_data["station_code"].astype(int).map(lon_mapping)
    hourly_data["name"] = hourly_data["station_code"].astype(int).map(name_mapping)
    hourly_data["hour"] = pd.to_datetime(hourly_data["hour"])
    hourly_data["year"] = hourly_data["hour"].dt.year
    hourly_data["month"] = hourly_data["hour"].dt.month_name()
    hourly_data["weekday"] = hourly_data["hour"].dt.day_name()
    hourly_data["hour"] = hourly_data["hour"].dt.hour

    return hourly_data


# get_hourly_data()


def recalculate_recs(recommendations):
    total_removals = recommendations["recommended_removals"].sum()
    total_adds = recommendations["recommended_adds"].sum()

    # Represent each location's additions as a proportion of all planned additions
    recommendations["proportional_adds"] = (
        recommendations["recommended_adds"] / total_adds
        if total_adds
        else recommendations["recommended_adds"]
    )

    # Scale by total bikes available due to removals; round to nearest int
    # There will be some rounding error here, and the total will not add up to the exact number of bikes.
    recommendations["adjusted_adds"] = (
        (recommendations["proportional_adds"] * total_removals).round().astype(int)
    )
    return recommendations


def calculate_truckloads(bikes, capacity):
    return math.ceil(bikes / capacity)


def process_performance_data():
    performance = pd.read_csv("data/Monthly_Performance_Neighborhood.csv")
    od_2019 = pd.read_csv("data/OD_2019-10.csv")
    truck_capacity = 30
    truckload_cost = 30
    avg_trip_rev = od_2019.duration_sec.mean() * 0.0025
    performance["Revenu Gained"] = performance["effective_moves"] * avg_trip_rev

    trips_gained = performance["effective_moves"].sum()

    revenue_gained = trips_gained * avg_trip_rev

    monthly_truckloads = (
        performance.groupby("date")
        .sum()["effective_moves"]
        .apply(lambda x: calculate_truckloads(x, truck_capacity))
    )
    total_truckloads = monthly_truckloads.sum()
    total_rebalancing_cost = total_truckloads * truckload_cost

    profit = revenue_gained - total_rebalancing_cost
    return performance, trips_gained, revenue_gained, total_rebalancing_cost, profit
