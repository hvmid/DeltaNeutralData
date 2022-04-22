# DeltaNeutralData
Uniswap V2: Backtesting Liquidity pools

Dependencies: 
- node v17.9
- npm v8.5.5
- Python v3.10
- axios
- pandas
- numpy

How to use:

Run the following command from this repos directory:

```
python3 backtest.py top days LP_rate B_rate S_rate
```

Where: 

- top = number of top pairs
- days = number of days to backtest 
- LP_rate = Liquidity pool fee rate
- B_rate = Borrow rate for shorting volatile token
- S_rate = Staking rate for stablecoin


Output:

1. Data (folder): contains csv tables with pairDayData (reserveUSD, dailyVolumeUSD, etc.) for a given pair, csv tables names are 
each pairs' pairAddress.

2. topPairs.csv: contains the outout of topPairs.js. top n pairs ordered by reserveUSD descending and contains the final product of the backtest running n days.

