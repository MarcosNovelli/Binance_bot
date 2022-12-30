import binance 
from config import CLIENT
from time import sleep


def check_DBD(self):

    first_low = min(list(self.data.low.get(ago=-120, size=60)))
    second_low = min(list(self.data.low.get(ago=-60, size=60)))
    third_low = min(list(self.data.low.get(ago=-1, size=60)))

    # Detect DBD formation
    Dropbd = self.data.open[self.first_candle_open] > self.data.close[self.first_candle_close] and (self.data.close[self.first_candle_close] - first_low) < (self.data.open[self.first_candle_open] - self.data.close[self.first_candle_close])
    dBased = self.data.close[self.base_close] > self.data.open[self.base_open]
    dbDrop = self.data.open[self.third_candle_open] > self.data.close[self.third_candle_close] and self.data.close[self.third_candle_close] < second_low and (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close]) >= ((self.data.close[self.third_candle_close] - self.data.open[self.base_open]) * 2) and self.data.close[self.third_candle_close] < first_low and (self.data.close[self.third_candle_close] - third_low) < (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close])
    
    DBD = Dropbd and dBased and dbDrop
    
    self.trade_type = "DBD" if DBD else self.trade_type
    
    return DBD



while True:

    # Need to request X candles from the past to binance
    # Check if any conditions are met and trade
    

    
    sleep(60)