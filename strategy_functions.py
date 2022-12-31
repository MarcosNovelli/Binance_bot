class SupplyAndDemand:

    def __init__(self, df):

        self.df = df

        # Para usar como indice en un slice
        self.MinusOne_candle_open = 0
        self.MinusOne_candle_close = 59
        self.first_candle_open = 60
        self.first_candle_close = 119 
        self.second_candle_open = 120
        self.second_candle_close = 179
        self.third_candle_open = 180
        self.third_candle_close = 239

        self.minus_one_low = min(list(df.get("Low"))[0:59])
        self.first_low = min(list(df.get('Low'))[59:119])
        self.second_low = min(list(df.get('Low'))[119:179])
        self.third_low = min(list(df.get('Low'))[179:239])


    # Ver que capaz tenga que crear las funciones de la estrategia como una clase, para poder acceder a todas las variables mas facil
    def check_DBD(self):

        # Detect DBD formation
        Dropbd = self.df.get('Open')[self.first_candle_open] > self.df.get('Close')[self.first_candle_close] and (self.df.get('Close')[self.first_candle_close] - self.first_low) < (self.df.get('Open')[self.first_candle_open] - self.df.get("Close")[self.first_candle_close])
        dBased = self.df.get("Close")[self.second_candle_close] > self.df.get("Open")[self.second_candle_open]
        dbDrop = self.df.get("Open")[self.third_candle_open] > self.df.get("Close")[self.third_candle_close] and self.df.get("Close")[self.third_candle_close] < self.second_low and (self.df.get("Open")[self.third_candle_open] - self.df.get("Close")[self.third_candle_close]) >= ((self.df.get("Close")[self.third_candle_close] - self.df.get("Open")[self.second_candle_open]) * 2) and self.df.get("Close")[self.third_candle_close] < self.first_low and (self.df.get("Close")[self.third_candle_close] - self.third_low) < (self.df.get("Open")[self.third_candle_open] - self.df.get("Close")[self.third_candle_close])
        
        DBD = Dropbd and dBased and dbDrop
        
        return DBD
    
    def check_RBD(self):
        
        # Detect RBD formation
        Rallybd = self.df.get("Close")[self.second_candle_close] > self.df.get("Close")[0] # el 0 es -240
        rBased = self.df.get("Open")[self.second_candle_open] < self.df.get("Close")[self.second_candle_close]
        rbDrop = self.df.get("Close")[self.third_candle_close] < self.df.get("Open")[self.third_candle_open] and (self.df.get("Open")[self.third_candle_open] - self.df.get("Close")[self.third_candle_close]) >= ((self.df.get("Close")[self.second_candle_close] - self.df.get("Open")[self.second_candle_open]) * 1.5) and self.df.get("Close")[self.third_candle_close] < self.second_low and self.df.get("Close")[self.third_candle_close] < self.first_low and self.df.get("Close")[self.third_candle_close] < self.minus_one_low and (self.df.get("Close")[self.third_candle_close] - self.third_low) * 1.15 < (self.df.get("Close")[self.third_candle_open] - self.df.get("Close")[self.third_candle_close])
        
        RBD = Rallybd and rBased and rbDrop

        return RBD