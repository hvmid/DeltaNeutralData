import sys
import pandas as pd


# x = int(sys.argv[1])
try:
	x = int(sys.argv[1])

except ValueError:
	tok0 = input("Input token a: ").upper()
	tok1 = input("Input token b: ").upper()
except IndexError:
	 print("hey")

# datafile = "topPairs.csv"
# df = pd.read_csv(datafile)

# tok0 = 'usdt'.upper()
# tok1 = 'weth'.upper()

# pairADD = (df.query('(token0 == "%s" and token1 == "%s")or(token1 == "%s" and token0 == "%s")' %(tok0, tok1, tok0, tok1)))['pairAddress']

# print(pairADD)