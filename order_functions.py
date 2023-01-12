from config import client, discord_address, discord_authorization
import requests

def send_message_to_ds(message:str):
    payload = {
        "content": message
    }

    header = {
        "authorization": discord_authorization
    }

    r = requests.post(discord_address, data=payload, headers=header)


def create_main_order(ticker, quantity, side):
    
    main_order = client.futures_create_order(symbol=ticker, quantity=quantity, side=side, type=client.ORDER_TYPE_MARKET)
    client.futures_change_leverage(symbol=ticker, leverage=20)
    print("Main order created")
    send_message_to_ds("Main order created")


    return main_order

def set_stop_loss(ticker, quantity, main_order_price, stop, main_trade_side):

    price = (float(str((float(main_order_price) * (1 - stop)))[:6])) if main_trade_side else (float(str((float(main_order_price) * (1 + stop)))[:6]))

    stop_loss = client.futures_create_order(
        symbol=ticker,
        quantity=quantity,
        side="BUY",
        type='STOP_MARKET',
        stopPrice=price)

    print("Stop Loss in place")
    send_message_to_ds("Stop Loss in place")

    return stop_loss

def set_target(ticker, quantity, main_order_price, target, main_trade_side):
    
    price = (float(str((float(main_order_price) * (1 + target)))[:6])) if main_trade_side else (float(str((float(main_order_price) * (1 - target)))[:6]))

    take_profit = client.futures_create_order(
        symbol=ticker, 
        quantity=quantity, 
        side="BUY", 
        type=client.ORDER_TYPE_LIMIT, 
        price=price, 
        timeInForce="GTC")

    print("Take Profit in place")
    send_message_to_ds("Take Profit in place")

    return take_profit