import dash_design_kit as ddk
import requests
from datetime import datetime

GOV_URL = "https://analytics.usa.gov/data/"

GOV_AGENCIES = [
    "live",
    "agency-international-development",
    "agriculture",
    "commerce",
    "defense",
    "education",
    "energy",
    "health-human-services",
    "homeland-security",
    "housing-urban-development",
    "justice",
    "labor",
    "state",
    "transportation",
    "veterans-affairs",
    "interior",
    "treasury",
    "environmental-protection-agency",
    "executive-office-president",
    "general-services-administration",
    "national-aeronautics-space-administration",
    "national-archives-records-administration",
    "national-science-foundation",
    "nuclear-regulatory-commission",
    "office-personnel-management",
    "postal-service",
    "small-business-administration",
    "social-security-administration",
]

GOV_OPTIONS = [
    {"label": val.replace("-", " ").replace("live", "All").title(), "value": val}
    for val in GOV_AGENCIES
]


def load_json(url=None):
    r = requests.get(url)
    return r.json()


def get_figure(dept="live"):
    df = ddk.datasets.us_cities()

    cities = load_json(
        "https://analytics.usa.gov/data/" + dept + "/top-cities-realtime.json"
    )["data"]

    cities_dict = {item["city"]: item["active_visitors"] for item in cities}

    # strip whitespace so city names match usa.gov data
    df["name"] = df["name"].str.strip()
    # filter by cities that have traffic data
    df = df[df["name"].isin(list(cities_dict))]

    df["visitors"] = df["name"].map(cities_dict)
    df["text"] = (
        df["name"]
        + "<br> Visitors: "
        + df["visitors"]
        + "<br>Population "
        + (df["pop"] / 1e6).astype(str)
        + " million"
    )
    limits = [(0, 30), (30, 100), (110, 200), (210, 500), (500, 1000)]
    cities = []
    scale = 2

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0] : lim[1]]
        city = dict(
            type="scattergeo",
            locationmode="USA-states",
            lon=df_sub["lon"],
            lat=df_sub["lat"],
            text=df_sub["text"],
            visitors=df_sub["visitors"],
            marker=dict(
                size=df_sub["visitors"].astype(int) / scale,
                # sizeref = 2. * max(df_sub['pop']/scale) / (25 ** 2),
                line=dict(width=0.5, color="rgb(40,40,40)"),
                sizemode="area",
            ),
            name="{0} - {1}".format(lim[0] * 10, lim[1] * 10),
        )
        cities.append(city)

    layout = dict(
        showlegend=True,
        height=240,
        geo=dict(
            scope="usa",
            projection=dict(type="albers usa"),
            showland=True,
            landcolor="rgb(217, 217, 217)",
            subunitwidth=1,
            countrywidth=1,
        ),
    )
    fig = dict(data=cities, layout=layout)
    return fig


def load_json(url=None):
    r = requests.get(url)
    return r.json()


def get_active_users(dept="live"):
    users = load_json(GOV_URL + dept + "/realtime.json")["data"][0]["active_visitors"]
    return format(int(users), ",")


def get_monthly_traffic(dept="live", stat="users"):
    total = load_json(GOV_URL + dept + "/top-traffic-sources-30-days.json")["totals"][
        stat
    ]
    return format(int(total), ",")


def format_hour(hour):
    d = datetime.strptime(hour, "%H")
    return d.strftime("%I %p").lstrip("0").replace(" 0", " ")


def get_visits_today(dept="live"):
    data = load_json(GOV_URL + dept + "/today.json")["data"]
    return dict(x=[(d["hour"]) for d in data], y=[d["visits"] for d in data])


def truncate_title(title):
    return (title[:30] + "...") if len(title) > 30 else title


def get_top_downloads(dept="live"):
    data = load_json(GOV_URL + dept + "/top-downloads-yesterday.json")["data"]
    return dict(
        y=[truncate_title(d["page_title"]) for d in data[:20]],
        x=[d["total_events"] for d in data[:20]],
    )


def get_top_domains(dept="live", days="7"):
    data = load_json(GOV_URL + dept + "/top-domains-" + days + "-days.json")["data"]
    return dict(y=[d["domain"] for d in data[:20]], x=[d["visits"] for d in data[:20]])


def get_top_pages(dept="live"):
    data = load_json(GOV_URL + dept + "/top-pages-realtime.json")["data"]
    return dict(
        y=[truncate_title(d["page_title"]) for d in data[:20]],
        x=[d["active_visitors"] for d in data[:20]],
    )
