import alpaca_trade_api as tradeapi
import time

class Portfolio:

    def __init__(self,backtest:bool=False):
        self.parser = ConfigParser()
        self.parser.read("config.ini")
        self.positions = {}
        self.buying_power = 0