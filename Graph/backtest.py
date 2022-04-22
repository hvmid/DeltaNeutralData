import pandas as pd
import numpy as np
from datetime import date
import time
import os
import sys


def getTopPairs(n, date):
    os.system("node mostLiquid.js %i %s" % (n, date))
    datafile = "topPairs.csv"
    df = pd.read_csv(datafile)

    return df

def getDailyPrices(tokenAddress, days):
    os.system("node tokenPriceUSD.js %s %i" % (tokenAddress, days))
    datafile = "data/prices/%s.csv" % tokenAddress
    df = pd.read_csv(datafile)

    return df


def backtest(pairAddress, days, LP_rate, B_rate, S_rate):

    daily_borrow_rate = B_rate/365
    daily_stake_rate = S_rate/365
    os.system("node graph.js %s %i" % (pairAddress, days))
    datafile = "data/%s.csv" % pairAddress
    df = pd.read_csv(datafile)
    date = df['date'][0]

    token0 = df['token0.id'][0]
    token1 = df['token1.id'][0]

    toke0Prices = getDailyPrices(str(token0), days)
    toke1Prices = getDailyPrices(str(token1), days)

    df['token0.priceUSD'] = toke0Prices['priceUSD']
    df['token1.priceUSD'] = toke1Prices['priceUSD']
    df['token0.volumeUSD'] = df['token0.priceUSD']*df['dailyVolumeToken0']
    df['token1.volumeUSD'] = df['token1.priceUSD']*df['dailyVolumeToken1']
    df['24hr_reward'] = df['dailyVolumeUSD'] * LP_rate
    df['pool_share'] = 1 / df['reserveUSD']
    df['24hr_reward_share'] = df['24hr_reward'] * df['pool_share']
    df['ratio'] = df['token1.priceUSD']/df['token0.priceUSD']
    df['ratio'] = df['ratio'][0]/df['ratio']
    df['iloss'] = (2 * (df['ratio']**0.5 / (1 + df['ratio'])) - 1)
    df['daily_borrow_fee'] = B_rate/365
    df['daily_stake_reward'] = [((daily_stake_rate+1)**(i+1))-1 for i in range(len(df))]

    df.to_csv("data/%s.csv" % pairAddress)

    pairApr = sum(df['24hr_reward_share'])
    pairApy = np.prod([1+reward for reward in df['24hr_reward_share']])-1

    # df['dlp_net_apr'] = 
    # df['dlp_net_apy'] = 
    
    return pairApr, pairApy, date, df


def main():

    top, days, LP_rate, B_rate, S_rate = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    aprs = []
    apys = []
    deltaAprs = []
    deltaApys = []
    ethUSDC = "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"
    date = backtest(ethUSDC, days, LP_rate, B_rate, S_rate)[2]
    df = getTopPairs(top, date)
    df.loc[df['dailyVolumeUSD'] != 0,:]
    for pair in df['pairAddress']:
        aprs.append(backtest(pair, days, LP_rate, B_rate, S_rate)[0])
        apys.append(backtest(pair, days, LP_rate, B_rate, S_rate)[1])

    df["aprs"], df["apys"] = aprs, apys
    df.to_csv("backtest%sdays.csv" % days)


if __name__ == '__main__':
    # Try python3 backtest.py 10 365 0.003
    main()
