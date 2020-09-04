import alpaca_trade_api as tradeapi
import time
from configparser import ConfigParser

api = tradeapi.REST(
    'PKUFEOFDZG3TUEMVMHEN',
    'ICTpmj6x6xws9y3HX3jJwjpV5qm7ySaJjHVC9bGx',
    'https://paper-api.alpaca.markets'
    )

symbol = "FUV"
barset = api.get_barset(symbol, '5Min',limit=300)
aapl_bars = barset[symbol]
print(len(aapl_bars))
fd = open("data/"+symbol+".txt","w+")
fd.write("%s,%s,%s,%s,%s,%s\n" % ("timestamp","open","close","high","low","volume"))

for bar in aapl_bars:
    print(bar.t, bar.c)
    fd.write("%s,%.3f,%.3f,%.3f,%.3f,%ld\n" % 
    (bar.t.isoformat(),bar.o,bar.c,bar.h,bar.l,bar.v))
fd.close()