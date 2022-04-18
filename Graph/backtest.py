import pandas as pd
from datetime import datetime
import os

def topPairs(top):

	os.system("node mostLiquid.js %i" %top)
	datafile = "topPairs.csv"
	df = pd.read_csv(datafile)

	return df

def backtest(pairAddress, days, rate):

	os.system("node graph.js %s %i" %(pairAddress, days))
	datafile = "data/%s.csv" %pairAddress
	df = pd.read_csv(datafile)

	pairApr = apr(rate, df)

	return pairApr

def apr(rate, df):
	df['24hr_reward'] = df['dailyVolumeUSD']*rate
	df['pool_share'] = 1/df['reserveUSD']
	df['24hr_reward_share'] = df['24hr_reward']*df['pool_share']
	backtest_apr = sum(df['24hr_reward_share'])

	return backtest_apr

# def apy():

def do_backtest(top, days, rate):

	aprs  = []
	df = topPairs(top)
	pairs = df['pairAddress']

	for pair in pairs:
		aprs.append(backtest(pair, days, rate))
	
	df["aprs"]=aprs
	df.to_csv("aprs%s.csv" %days)

do_backtest(10, 7, 0.003)

