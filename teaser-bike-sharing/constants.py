import utils.utils as utils
import os

df, df_stations, neighborhoods, neighborhood_list, df_daily_usage = utils.prepare_data()

(
    not_member_times_rented,
    memnber_times_rented,
    not_member_total_duration,
    member_total_duration,
    rental_non_members_rate,
    duration_non_members_rate,
    rental_members_rate,
    duration_members_rate,
) = utils.rental_stats(df)

hourly_data = utils.get_hourly_data()
today_data = utils.get_today_data()

(
    performance,
    trips_gained,
    revenue_gained,
    total_rebalancing_cost,
    profit,
) = utils.process_performance_data()
AGGRID_LICENCE = os.environ.get("AGGRID_ENTERPRISE")
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")
