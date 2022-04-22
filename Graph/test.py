from datetime import datetime
import time
import pandas as pd
import backtest as bt
import numpy as np
# now = str(datetime.now())[0:10].split("-")
# t = datetime(int(now[0]), int(now[1]), int(now[2]), 20, 00)
# unixTime = time.mktime(t.timetuple())*1000
# print(unixTime)

datafile = "data/%s.csv" % "0x21b8065d10f73ee2e260e5b47d3344d3ced7596e"
df = pd.read_csv(datafile)

# token0 = df['token0.id'][0]
# token1 = df['token1.id'][0]

# toke0Prices = bt.getDailyPrices(str(token0), 10)
# toke1Prices = bt.getDailyPrices(str(token1), 10)

# df['token0.priceUSD'] = toke0Prices['priceUSD']
# df['token1.priceUSD'] = toke1Prices['priceUSD']
# df['ratio'] = df['token1.priceUSD']/df['token0.priceUSD']
# df['ratio'] = df['ratio'][0]/df['ratio']
# df['iloss'] = (2 * (df['ratio']**0.5 / (1 + df['ratio'])) - 1)
# print(df)
daily_stake_rate = 0.1

x = [((daily_stake_rate+1)**(i+1))-1 for i in range(len(df))]
print(x)
