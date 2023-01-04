import binance 
from config import client
from time import sleep
from data_functions import get_candlestick_data
import datetime as dt
import pandas as pd
from strategy_functions import SupplyAndDemand

ticker = 'BTCUSDT'
quantity = 0.01
stop = 0.0005
target = 0.00005

in_trade = False
stop_loss = 0
target = 0


while True:
    
    minutes = int(str((dt.datetime.now()))[-12:-10])
    seconds = int(str((dt.datetime.now()))[-9:-7])
    print(str((dt.datetime.now()))[:-7])

    # Ejecutar el primer minuto de cada hora (cuando las velas anteriores estan completas)
    if minutes == 8 and seconds == 0:

        print("{} Checking for trade opportunity...".format(str((dt.datetime.now()))[:-7]))

        df = get_candlestick_data(ticker)
        print(df)

        #Check if any conditions are met and trade
        SD = SupplyAndDemand(df)

        DBD = True #SD.check_DBD()
        RBD = SD.check_RBD()
        RBR = SD.check_RBR()
        DBR = SD.check_DBR()

        # If conditions met, open trade with target and stop loss
        if DBD or RBD:
            print("Trade Found")
            # Order management

            # Create main order and set leverage
            main_order = client.futures_create_order(symbol=ticker, quantity=quantity, side="SELL", type=client.ORDER_TYPE_MARKET)
            client.futures_change_leverage(symbol=ticker, leverage=20, )
            main_order_price = client.futures_account_trades(symbol=ticker)[-1]['price']

            in_trade = True

            # Set take profit and stop loss
            stop_loss = client.futures_create_order(symbol=ticker, quantity=quantity, side="BUY", type='STOP_MARKET', stopPrice=(float(str((float(main_order_price) * (1 + stop)))[:6])))
            target = client.futures_create_order(symbol=ticker, quantity=quantity, side="BUY", type=client.ORDER_TYPE_LIMIT, price=(float(str((float(main_order_price) * (1 - target)))[:6])), timeInForce="GTC")

    sleep(1)
    
    # Check on positions every 30 seconds (ver si capaz no es mucho tiempo)
    if seconds == 30 and in_trade:

        # Check if target or stop has been hit
        all_trades = client.futures_account_trades(symbol=ticker)
        if stop_loss['orderId'] == all_trades[-1]['orderId']:
            print("Stop Reached")
            client.futures_cancel_order(symbol=ticker, orderId=target['orderId'])
            in_trade = False
            break

        if target['orderId'] == all_trades[-1]['orderId']:
            print("Target reached")
            client.futures_cancel_order(symbol=ticker, orderId=stop_loss['orderId'])
            in_trade = False
            break