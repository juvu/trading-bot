import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import time
import datetime

symbol = 'FUV'
stop_loss_percent = 0.15
take_profit_percent = 0.2
num_of_shares = 2000
api = tradeapi.REST(
    'PKUFEOFDZG3TUEMVMHEN',
    'ICTpmj6x6xws9y3HX3jJwjpV5qm7ySaJjHVC9bGx',
    'https://paper-api.alpaca.markets'
    )
df = pd.read_csv('data/'+symbol+'.txt')
df = df.set_index(df['timestamp'].values)
status = "normal"

def buy(status,api,symbol,quantity,take_pro=0,stop_los=0):
    if status=="short":
        print(api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        ))
    if status=="normal":
        print(api.submit_order(
            symbol=symbol,
            side='buy',
            type='market',
            qty=quantity,
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(
                limit_price=take_pro,
            ),
            stop_loss=dict(
                stop_price=stop_los,
                limit_price=stop_los,
            )
        ))

def sell(status,api,symbol,quantity,take_pro=0,stop_los=0):
    if status=="long":
        print(api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        ))
    if status=="normal":
        print(api.submit_order(
            symbol=symbol,
            side='sell',
            type='market',
            qty=quantity,
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(
                limit_price=take_pro,
            ),
            stop_loss=dict(
                stop_price=stop_los,
                limit_price=stop_los,
            )
        ))
def request_data(api,symbol)->bool:
    global df
    barset = api.get_barset(symbol, '5Min',limit=1)
    bars = barset[symbol]
    last_index = df.tail(1)['timestamp'].values[0]
    print(last_index,bars[0].t.isoformat())
    if bars[0].t.isoformat() != last_index:
        fd = open("data/"+symbol+".txt","a+")
        fd.write("%s,%.3f,%.3f,%.3f,%.3f,%ld\n" % 
        (bars[0].t.isoformat(),bars[0].o,bars[0].c,bars[0].h,bars[0].l,bars[0].v))
        print("{},{},{},{},{},{}".format(bars[0].t.isoformat(),bars[0].o,bars[0].c,bars[0].h,bars[0].l,bars[0].v))
        fd.close()
        df = pd.read_csv('data/'+symbol+'.txt')
        df = df.set_index(df['timestamp'].values)
        print(df.tail(1))
        return True
    return False

def get_status(api)->str:
    orders = api.list_orders()
    if len(orders)==0:
        return 'normal'
    else:
        if orders[0].side == 'buy':
            return 'long'
        else:
            return 'short'


while True:
    clock = api.get_clock()
    if clock.is_open:
        if request_data(api,symbol):
            print(df.tail(1))
            ShortEMA = df.close.ewm(span=12,adjust=False).mean()
            LongEMA = df.close.ewm(span=26,adjust=False).mean()
            MACD = ShortEMA - LongEMA
            signal = MACD.ewm(span=9,adjust=False).mean()
            diff = MACD-signal
            status = get_status(api)
            # entry long and look for exit long
            if status == "long":
                if (diff[-2] < 0 and diff[-1] > 0):
                    sell(status,api,symbol,num_of_shares)
            # entry short and look for exit short
            if status == "short":
                if (diff[-2] > 0 and diff[tf] < 0):
                    buy(status,api,symbol,num_of_shares)
            # not holding any position
            if status == "normal":
                # see a buy signal
                if diff[-2] > 0 and diff[-1] < 0:
                    stop_loss = df['close'][tf]*(1-stop_loss_percent)
                    take_profit = df['close'][tf]*(1+take_profit_percent)
                    buy(status,api,symbol,num_of_shares,take_profit,stop_loss)
                # see a sell signal
                if diff[-2]< 0 and diff[-1] > 0:
                    stop_loss = df['close'][-1]*(1+stop_loss_percent)
                    take_profit = df['close'][-1]*(1-take_profit_percent)
                    sell(status,api,symbol,num_of_shares,take_profit,stop_loss)
    else:
        print("Market is closed")
    time.sleep(5)