import pandas as pd
import os


def topPairs(n):
    # n: number of top pairs
    # Runs node script: "mostLiquid.js"
    # Returns the DataFrame with top n pairs
    # Columns: (token0, token1, reserveUSD, pairAddress)
    # Data is saved into a csv table "topPairs.csv"

    os.system("node mostLiquid.js %i" % n)
    datafile = "topPairs.csv"
    df = pd.read_csv(datafile)

    return df


def backtest(pairAddress, days, rate):

    os.system("node graph.js %s %i" % (pairAddress, days))
    datafile = "data/%s.csv" % pairAddress
    df = pd.read_csv(datafile)

    pairApr = apr(rate, df)

    return pairApr


def apr(rate, df):
    df['24hr_reward'] = df['dailyVolumeUSD'] * rate
    df['pool_share'] = 1 / df['reserveUSD']
    df['24hr_reward_share'] = df['24hr_reward'] * df['pool_share']
    backtest_apr = sum(df['24hr_reward_share'])
    backtest_apy = apy(backtest_apr)

    return backtest_apr, backtest_apy


def apy(apr):

    return ((1 + apr / 365)**365) - 1


def topPairs_backtest(top, days, rate):

    aprs = []
    apys = []
    df = topPairs(top)
    pairs = df['pairAddress']

    for pair in pairs:
        aprs.append(backtest(pair, days, rate)[0])
        apys.append(backtest(pair, days, rate)[1])

    df["aprs"] = aprs
    df["apys"] = apys
    df.to_csv("backtest%sdays.csv" % days)


if __name__ == "main":
    topPairs_backtest(100, 7, 0.003)
