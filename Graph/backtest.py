import pandas as pd
import numpy as np
from datetime import date
import time
import os
import sys

pd.options.mode.chained_assignment = None


def getTopPairs(n, date):
    os.system("node mostLiquid.js %i %i" % (n, int(date)))
    datafile = "topPairs.csv"
    df = pd.read_csv(datafile)

    return df

def getDailyPrices(tokenAddress, days):
    os.system("node tokenPriceUSD.js %s %i" % (tokenAddress, days))
    datafile = "data/prices/%s.csv" % tokenAddress
    df = pd.read_csv(datafile)

    return df


def backtest(pairAddress, days, LP_rate, B_rate, S_rate):

    #Run JS script and import data
    os.system("node graph.js %s %i" % (pairAddress, days))
    datafile = "data/%s.csv" % pairAddress
    df = pd.read_csv(datafile)
    date = df['date'][0]

    #Get token ID to query its historic prices
    token0 = df['token0.id'][0]
    token1 = df['token1.id'][0]

    #Query historic price for given token
    toke0Prices = getDailyPrices(str(token0), days)
    toke1Prices = getDailyPrices(str(token1), days)

    #Extra rows via getDailyPrices
    df['token0.priceUSD'] = toke0Prices['priceUSD']
    df['token1.priceUSD'] = toke1Prices['priceUSD']
    df['token0.volumeUSD'] = df['token0.priceUSD']*df['dailyVolumeToken0']
    df['token1.volumeUSD'] = df['token1.priceUSD']*df['dailyVolumeToken1']

    #Total pool rewards pool in 24hr
    df['24hr_reward'] = df['dailyVolumeUSD'] * LP_rate
    df['pool_share'] = 1 / df['reserveUSD'] #Your pool share
    df['24hr_reward_share'] = df['24hr_reward'] * df['pool_share'] #Reward Share %

    #Calculating daily iloss
    df['ratio'] = df['token1.priceUSD']/df['token0.priceUSD']
    df['ratio'] = df['ratio'][len(df)-1]/df['ratio']
    df['iloss'] = (2 * (df['ratio']**0.5 / (1 + df['ratio'])) - 1)

    df['daily_borrow_fee'] = B_rate/365
    #Approximate First days stake rate
    firstDay_stake_rate = S_rate/365
    #Approximate n days stake rate
    df['daily_stake_reward'] = [((firstDay_stake_rate+1)**(i+1))-1 for i in range(len(df))][::-1]

    #Calculating daily compouding rewards
    df['24hr_comp_reward_share'] = 1+df['24hr_reward_share'] #Temporary columns values
    for i in range(len(df)-2, -1, -1):
        df['24hr_comp_reward_share'][i]=(df['24hr_comp_reward_share'][i+1]) * (df['24hr_comp_reward_share'][i])
    for i in range(0, len(df)-1):
        df['24hr_comp_reward_share'][i]=df['24hr_comp_reward_share'][i]-df['24hr_comp_reward_share'][i+1]
    df['24hr_comp_reward_share'][len(df)-1]-=1

    df['dnlp_rew'] = df['24hr_reward_share'] + (df['daily_stake_reward']/2) - (df['daily_borrow_fee']/2)
    df['dnlp_CumRew'] = df['24hr_comp_reward_share'] + (df['daily_stake_reward']/2) - (df['daily_borrow_fee']/2)

    #Calculating net deltra neutral lp income
    LP_Rewards = sum(df['24hr_reward_share'])
    LP_CumRew = sum(df['24hr_comp_reward_share'])
    DNLP_Rewards = sum(df['dnlp_rew'])
    DNLP_CumRew = sum(df['dnlp_CumRew'])

    df.to_csv("data/%s.csv" % pairAddress)

    return LP_Rewards, LP_CumRew, DNLP_Rewards, DNLP_CumRew, date, df


def main():

    top, days, LP_rate, B_rate, S_rate = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    pairReward = []
    pairCumRew = []
    deltaRewards = []
    deltaCumRew = []
    ethUSDC = "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"
    date = backtest(ethUSDC, days, LP_rate, B_rate, S_rate)[4]
    df = getTopPairs(top, date)
    for pair in df['pairAddress']:
        pairReward.append(backtest(pair, days, LP_rate, B_rate, S_rate)[0])
        pairCumRew.append(backtest(pair, days, LP_rate, B_rate, S_rate)[1])
        deltaRewards.append(backtest(pair, days, LP_rate, B_rate, S_rate)[2])
        deltaCumRew.append(backtest(pair, days, LP_rate, B_rate, S_rate)[3])

    df["pairReward"], df["pairCumRew"], df["deltaRewards"], df["deltaCumRew"] = pairReward, pairCumRew, deltaRewards, deltaCumRew
    df.to_csv("topPairs.csv")

    


if __name__ == '__main__':
    main()
