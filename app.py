import binance 
from config import client
from time import sleep
from functions import get_candlestick_data
import datetime as dt
import pandas as pd
from strategy_functions import SupplyAndDemand

ticker = 'BTCUSDT'



# while True:
    # Need to request 179 candles from the past to binance creo que deberia borrar la mas reciente

# Hacer que espere hasta que sea divisble por 3600
if (dt.datetime.now()).timestamp() % 3600:

    print("Checking for trade opportunity...")




    df = get_candlestick_data(ticker)
    print(df)


    # Check if any conditions are met and trade
    SD = SupplyAndDemand(df)
    
    DBD = SD.check_DBD()
    RBD = SD.check_RBD()
    
    print(DBD)
    print(RBD)


    

    # sleep(60)