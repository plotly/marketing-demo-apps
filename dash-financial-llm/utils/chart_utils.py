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

    df["DAY"] = pd.to_datetime(df["DAY"], format="%d-%b-%y")
    df = df.sort_values("DAY")

    colors = px.colors.qualitative.Plotly

    traces = []
    for i, ticker in enumerate(stocks):
        stock_data = df[df["TICKER"] == ticker]
        color = colors[
            i % len(colors)
        ]  #cycle through colors if more stocks than colors
        trace = go.Scatter(
            x=stock_data["DAY"],
            y=stock_data["PRICE"],
            mode="lines",
            name=ticker,
            line=dict(color=color),
        )
        traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=f"S&P 500 Stock Prices {'(Weighted)' if weighted_stocks == 'Weighted' else ''}",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Date",
        yaxis_title="Price",
    )
    return fig
