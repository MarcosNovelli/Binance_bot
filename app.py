import binance 
from config import client
from time import sleep
from functions import get_candlestick_data
import datetime as dt
import pandas as pd
from strategy_functions import SupplyAndDemand

ticker = 'BTCUSDT'


while True:
    # Need to request 179 candles from the past to binance creo que deberia borrar la mas reciente

    print(str((dt.datetime.now()))[:-7])

    # Hacer que espere hasta que sea divisble por 3600
    if not (dt.datetime.now()).timestamp() % 3600:

        print("{} Checking for trade opportunity...".format(str((dt.datetime.now()))[:-7]))

        df = get_candlestick_data(ticker)
        # print(df)

        # Check if any conditions are met and trade
        SD = SupplyAndDemand(df)
        
        DBD = SD.check_DBD()
        RBD = SD.check_RBD()
        RBR = SD.check_RBR()
        DBR = SD.check_DBR()

        # If conditions met, open trade with target and stop loss
        # if DBR or DBD or RBR or RBD:
        order = client.futures_create_order(symbol=ticker, quantity=0.01, side="BUY", type=client.ORDER_TYPE_LIMIT, price=2000, timeInForce="GTC" )
        client.futures_change_leverage(symbol=ticker, leverage=20)        
    
    sleep(1)