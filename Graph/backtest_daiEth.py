import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


datafile = "data.csv"
df = pd.read_csv(datafile)
datacp = df.copy()

df['date'] = [datetime.fromtimestamp(date) for date in df['date']] #convert time from epoch to yyyy-mm-dd hh:mm:ss

print(df.head())

rate = 0.003 #current exchange fee for dai-eth (3%)
l_you = 2000000 #liquidity you provide

df['24hr_reward'] = df['dailyVolumeUSD']*rate
df['pool_share'] = l_you/df['reserveUSD']
df['24hr_reward_share'] = df['24hr_reward']*df['pool_share']

backtest_apr = sum(df['24hr_reward_share'])/l_you

print(backtest_apr)

