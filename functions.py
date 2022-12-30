import datetime as dt
from config import client
import pandas as pd

def get_candlestick_data(ticker):
    klines = client.get_historical_klines(ticker, client.KLINE_INTERVAL_1MINUTE, limit=179 )

    # Create dataframe with all candlestick info
    df = pd.DataFrame(klines)

    # Remove unnecesary info
    df = df.iloc[:,0:6]

    df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df["Adj_Close"] = df["Close"]

    df.Open      = df.Open.astype("float")
    df.High      = df.High.astype("float")
    df.Low       = df.Low.astype("float")
    df.Close     = df.Close.astype("float")
    df.Volume    = df.Volume.astype("float")

    df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.Date]

    return df