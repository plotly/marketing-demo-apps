import pandas as pd
import yfinance as yf
from datetime import datetime


def get_sp500_tickers():
    # Get sp500 tickers using wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)
    df = table[0]
    return df["Symbol"].tolist()


def generate_sp500_data():
    print("Fetching S&P 500 tickers...")
    tickers = get_sp500_tickers()

    print("Fetching data for S&P 500 stocks...")
    start_date = "2022-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    all_data = []

    for ticker in tickers:
        print(f"Processing {ticker}...")
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if not hist.empty:
            hist["TICKER"] = f"{ticker}"
            hist["WEIGHT"] = 0
            hist = hist.reset_index()
            hist = hist.rename(columns={"Date": "DAY", "Close": "PRICE"})
            all_data.append(hist[["DAY", "TICKER", "PRICE", "WEIGHT"]])

    print("Combining all stock data...")
    df = pd.concat(all_data, ignore_index=True)

    print("Calculating weights...")
    df["DAY"] = pd.to_datetime(df["DAY"])

    # Fetch shares outstanding for each stock
    shares_outstanding = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        shares = stock.info.get("sharesOutstanding")
        if shares:
            shares_outstanding[f"{ticker}"] = shares

    # Calculate market cap using shares outstanding
    df["MARKET_CAP"] = df.apply(
        lambda row: row["PRICE"] * shares_outstanding.get(row["TICKER"], 0), axis=1
    )

    df["TOTAL_MARKET_CAP"] = df.groupby("DAY")["MARKET_CAP"].transform("sum")
    df["WEIGHT"] = (df["MARKET_CAP"] / df["TOTAL_MARKET_CAP"]) * 100

    df = df.sort_values(["DAY", "TICKER"])
    df["DAY"] = df["DAY"].dt.strftime("%d-%b-%y").str.upper()

    print("Saving data to CSV...")
    df[["DAY", "TICKER", "PRICE", "WEIGHT"]].to_csv(
        "data/sp500_2022_2024.csv", index=False
    )

    print("Data generation complete. File saved as 'sp500_2022_2024.csv'")


if __name__ == "__main__":
    generate_sp500_data()
