import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def generate_GFSI_line_chart(ticker):
    df = pd.read_csv("data/fsi.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    fig = px.line(
        df,
        x="Date",
        y=ticker,
        title="OFR Financial Stress Index History",
    )
    return fig


def GFSI_options():
    df = pd.read_csv("data/fsi.csv")
    return [{"label": col, "value": col} for col in df.columns[1:]]


def SP_options():
    df = pd.read_csv("data/sp500_2022_2024.csv")["TICKER"].unique()

    return [{"label": col, "value": col} for col in df]


def generate_herfindahl_hirschman_index():
    df = pd.read_csv("data/sp500_2022_2024.csv")

    df = (
        df.groupby("DAY").agg({"WEIGHT": lambda x: round(sum(x**2), 2)}).reset_index()
    )
    df["DAY"] = pd.to_datetime(df["DAY"], format="%d-%b-%y")
    df = df.sort_values(by="DAY")

    fig = px.line(
        df,
        x="DAY",
        y="WEIGHT",
        title="Herfindahl-Hirschman Index, S&P 500",
    )
    return fig


def generate_SP_500_stocks(stocks, weighted_stocks):
    df = pd.read_csv("data/sp500_2022_2024.csv")

    df = df[df["TICKER"].isin(stocks)]
    if weighted_stocks == "Weighted":
        df["PRICE"] = df["PRICE"] * df["WEIGHT"]

    # Convert DAY to datetime and sort
    df["DAY"] = pd.to_datetime(df["DAY"], format="%d-%b-%y")
    df = df.sort_values("DAY")
    fig = px.line(
        df,
        x="DAY",
        y="PRICE",
    )
    fig.update_layout(
        legend=dict(orientation="v", yanchor="top", xanchor="left", x=1.02, y=1)
    )
    return fig
