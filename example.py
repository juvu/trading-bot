import alpaca_trade_api as tradeapi
import time
from configparser import ConfigParser

api = tradeapi.REST(
    'PKITO2MPSV11FWXDBTZP',
    'JSRZPdFv8RrNK0hZhCkJMIBMGovrECJyx8kXL935',
    'https://paper-api.alpaca.markets'
    )

t = 0
price = 0
print(api.list_orders())
print(api.submit_order(
    symbol='AAPL',
    qty=3,
    side='buy',
    type='market',
    time_in_force='gtc'
))
# position = api.get_position('AAPL')
# print(position)
# price = position.avg_entry_price
# while True:
#     # Get daily price data for AAPL over the last 5 trading days.
#     barset = api.get_barset('AAPL', '1Min',limit=1)
#     aapl_bars = barset['AAPL']

#     # See how much AAPL moved in that timeframe.
#     week_open = aapl_bars[0].o
#     week_close = aapl_bars[-1].c
#     print(aapl_bars)
#     # if aapl_bars[0].c > float(price)*1.0015:
#     #     print(api.submit_order(
#     #         symbol='AAPL',
#     #         qty=3,
#     #         side='sell',
#     #         type='market',
#     #         time_in_force='gtc'
#     #     ))
#     #     break
#     time.sleep(5)
   