class SupplyAndDemand:

    def __init__(self, df):

        self.df = df

        # Para usar como indice en un slice
        self.MinusTwo_candle_open = 0
        self.MinusTwo_candle_close = 59

        self.MinusOne_candle_open = 60
        self.MinusOne_candle_close = 119

        self.first_candle_open = 120
        self.first_candle_close = 179 

        self.second_candle_open = 180
        self.second_candle_close = 239

        self.third_candle_open = 240
        self.third_candle_close = 299

        self.minus_one_low = min(list(df.get('Low'))[59:119])
        self.first_low = min(list(df.get('Low'))[119:179])
        self.second_low = min(list(df.get('Low'))[179:239])
        self.third_low = min(list(df.get('Low'))[239:299])

        self.first_high = max(list(df.get('High'))[119:179])
        self.second_high = max(list(df.get('High'))[179:239])
        self.third_high = max(list(df.get('High'))[239:299])

        print(self.first_high)
        print(self.second_high)
        print(self.third_high)

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

    def check_RBR(self):

        # Detect RBR formation
        Rallybr = self.df.get("Open")[self.first_candle_open] < self.df.get("Close")[self.first_candle_close] and self.df.get("Close")[self.first_candle_close] > self.df.get("Close")[self.MinusOne_candle_close] and (self.second_high - self.df.get("Open")[self.second_candle_open]) * 1.5 + 0.0001 > (self.first_high - self.df.get("Close")[self.first_candle_close])
        rBaser = self.df.get("Open")[self.second_candle_open] > self.df.get("Close")[self.second_candle_close]
        rbRally = (self.third_high - self.df.get("Close")[self.third_candle_close]) < (self.df.get("Close")[self.third_candle_close] - self.df.get("Open")[self.third_candle_open]) and self.df.get("Close")[self.third_candle_close] > self.second_high and (self.df.get("Close")[self.third_candle_close] - self.df.get("Open")[self.third_candle_open]) >= self.df.get("Close")[self.third_candle_close] * 0.005

        RBR = Rallybr and rBaser and rbRally
    
        return RBR

    def check_DBR(self):

        # Detect DBR formation
        Dropbr = self.df.get("Open")[self.first_candle_open] > self.df.get("Close")[self.first_candle_close] or self.df.get("Open")[self.MinusOne_candle_open] > self.df.get("Close")[self.first_candle_close] or self.df.get("Open")[self.MinusTwo_candle_open] > self.df.get("Close")[self.first_candle_close] # Ver de cambiar todo a AND
        dBaser = self.df.get("Open")[self.second_candle_open] > self.df.get("Close")[self.second_candle_close] and self.second_high < self.df.get("Close")[self.third_candle_close] and (self.second_high - self.df.get("Open")[self.second_candle_open]) < (self.df.get("Open")[self.second_candle_open] - self.df.get("Close")[self.second_candle_close])
        dbRally = self.df.get("Close")[self.third_candle_close] > self.df.get("Open")[self.second_candle_open] and (self.df.get("Close")[self.third_candle_close] - self.df.get("Open")[self.third_candle_open]) >= ((self.df.get("Open")[self.second_candle_open] - self.df.get("Close")[self.second_candle_close]) * 1.5) and (self.third_high - self.df.get("Close")[self.third_candle_close]) * 2 < (self.df.get("Close")[self.third_candle_close] - self.df.get("Open")[self.third_candle_open])        
        
        DBR = Dropbr and dBaser and dbRally
                
        return DBR