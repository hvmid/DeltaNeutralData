# DeltaNeutralData
Uniswap V2: Backtesting Liquidity pools

Dependencies: 
- node v17.9
- npm v8.5.5
- Python v3.10
- pandas

How to use:

Run the Python script and topPair_backtest will be called, you can change the input arguments: topPair_backtest(n, days, rate)
n - number of top pair (ordered by reserveUSD (liquidity) descending)
days - number of days to backtest
rate - current exchange fee for the given liquidity pool

Output:

1. Data (folder): contains csv tables with pairDayData (reserveUSD, dailyVolumeUSD, etc.) for a given pair, csv tables names are 
each pairs' pairAddress.

2. topPairs.csv: contains the outout of topPairs.js. top n pairs ordered by reserveUSD descending.

3. backtest[n]days.csv: contains the final product of the backtest running n days.