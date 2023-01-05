from strategy import SupplyAndDemand
import binance 
from config import client
from time import sleep
from data_functions import get_candlestick_data
from order_functions import create_main_order, set_stop_loss, set_target
import datetime as dt
import pandas as pd

ticker = 'BTCUSDT'
quantity = 0.01
stop = 0.0005
target = 0.00005

in_trade = False
stop_loss = 0
take_profit = 0

LONG = 1
SHORT = 0

while True:
    
    minutes = int(str((dt.datetime.now()))[-12:-10])
    seconds = int(str((dt.datetime.now()))[-9:-7])
    print(str((dt.datetime.now()))[:-7])

    # Ejecutar el primer minuto de cada hora (cuando las velas anteriores estan completas)
    if minutes == 0 and seconds == 0 and not in_trade:

        print("{} Checking for trade opportunity...".format(str((dt.datetime.now()))[:-7]))

        df = get_candlestick_data(ticker)

        #Check if any conditions are met and trade
        SD = SupplyAndDemand(df)

        DBD = SD.check_DBD()
        RBD = SD.check_RBD()
        RBR = SD.check_RBR()
        DBR = SD.check_DBR()

        trade_type = "DBD" if DBD else "DBR" if DBR else "RBR" if RBR else "RBD"

        # If conditions met, open trade with target and stop loss
        if DBD or RBD:
            print("{} Detected".format(trade_type))

            # Create main order
            create_main_order(ticker, quantity, "SELL")
            main_order_price = client.futures_account_trades(symbol=ticker)[-1]['price']
            in_trade = True

            # Set take profit and stop loss
            stop_loss = set_stop_loss(ticker, quantity, main_order_price, stop, SHORT)
            take_profit = set_target(ticker, quantity, main_order_price, target, SHORT)
        
        if RBR or DBR:
            print("{} Detected".format(trade_type))

            # Create main order
            create_main_order(ticker, quantity, "BUY")
            main_order_price = client.futures_account_trades(symbol=ticker)[-1]['price']
            in_trade = True

            stop_loss = set_stop_loss(ticker, quantity, main_order_price, LONG)
            take_profit = set_target(ticker, quantity, main_order_price, LONG)

    sleep(1)
    
    # Check on positions every 15 seconds 
    if not seconds % 15 and in_trade:

        # Check if target or stop has been hit
        all_trades = client.futures_account_trades(symbol=ticker)
        if stop_loss['orderId'] == all_trades[-1]['orderId']:
            print("Stop Reached -- Exiting trade")
            client.futures_cancel_order(symbol=ticker, orderId=take_profit['orderId'])
            in_trade = False

        elif take_profit['orderId'] == all_trades[-1]['orderId']:
            print("Target reached -- Exiting trade")
            client.futures_cancel_order(symbol=ticker, orderId=stop_loss['orderId'])
            in_trade = False
        else:
            print("{} Positions in place".format(str((dt.datetime.now()))[:-7]))
