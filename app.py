import binance 
from config import client
from time import sleep
from functions import get_candlestick_data
import datetime as dt
import pandas as pd

ticker = 'BTCUSDT'

# while True:
# 10740 segundos
    # Need to request 179 candles from the past to binance
df = get_candlestick_data(ticker)
    # Check if any conditions are met and trade


print(df)

# sleep(60)