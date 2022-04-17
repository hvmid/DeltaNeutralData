import pandas as pd
from datetime import datetime
import os

os.system("node mostLiquid.js")

datafile0 = "top100.csv"
df0 = pd.read_csv(datafile0)
datacp0 = df0.copy()

aprs = []

for i in df0['pairAddress']:
	os.system("node graph.js %s" %i)

	datafile = "data/%s.csv" %i
	df = pd.read_csv(datafile)

	df['date'] = [datetime.fromtimestamp(date) for date in df['date']] #convert time from epoch to yyyy-mm-dd hh:mm:ss

	rate = 0.003 #current exchange fee

	df['24hr_reward'] = df['dailyVolumeUSD']*rate
	df['pool_share'] = 1/df['reserveUSD']
	df['24hr_reward_share'] = df['24hr_reward']*df['pool_share']

	backtest_apr = sum(df['24hr_reward_share'])

	aprs.append(backtest_apr)

df0["aprs"]=aprs
print(df0.head(20))

df0.to_csv("aprs.csv", sep='\t')

