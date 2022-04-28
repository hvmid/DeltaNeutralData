import os
import sys
import backtest as bt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def main():
	ans = input("Would you like to display any charts?(y/n): ")

	if ans.upper()=="Y":
		print("Please enter a pair from topPairs.csv to display its backtest charts.")
		tok0 = input("Input token a: ").upper()
		tok1 = input("Input token b: ").upper()

		datafile = "topPairs.csv"
		df = pd.read_csv(datafile)

		pairADD = (df.query('(token0 == "%s" and token1 == "%s")or(token1 == "%s" and token0 == "%s")' %(tok0, tok1, tok0, tok1))['pairAddress']).to_list()[0]

		datafile = "data/%s.csv" %pairADD
		df = pd.read_csv(datafile)
		df['date'] = [datetime.fromtimestamp(date) for date in df['date']]

		date = df['date']
		rew = df['24hr_reward_share']*100
		cumRew = df['24hr_comp_reward_share']*100
		dnlpRew = df['dnlp_rew']*100
		dnlpCumRew = df['dnlp_CumRew']*100
		iloss = df['iloss']*(-100)

		fig = plt.figure()
		plt.ylabel('ROI %')
		plt.xlabel("Date")
		plt.suptitle('%s-%s pool' %(df['token0'][0], df['token1'][0]))
		plt.plot(date, rew, label = "24hr LP Reward Share")
		plt.plot(date, cumRew, label = "24hr Cumulative LP Reward Share")
		plt.plot(date, dnlpRew, label = "24hr DNLP Reward Share")
		plt.plot(date, dnlpCumRew, label = "24hr Cumulative DNLP Reward Share")
		plt.plot(date, iloss, label = "IL")
		plt.legend()
		plt.show()


if __name__ == "__main__":
	main()