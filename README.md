# alpaca_sma_crossover_trader
This is a trading bot for executing trades based on Simple Moving Average (SMA) crossover strategy. The script is designed to be run during market hours, specifically focusing on the SPY ETF (S&P 500) but can be easily adjusted for other tickers.



## Prerequisites
The script uses the following libraries:

- alpaca_trade_api
- time
- datetime
- pytz
- logging
- math
To install these prerequisites, use the pip package manager:

```pip install alpaca-trade-api pytz```


## Configuration
Before using this script, you need to configure your Alpaca API keys. You can sign up for a free account at Alpaca.

Replace ```'YOUR-API-KEY'``` and ```'YOUR-API-SECRET'``` with your actual Alpaca API key and secret key:

```python
alpaca_api_key = 'YOUR-API-KEY'
alpaca_api_secret = 'YOUR-API-SECRET'
```

By default, the script uses Alpaca's paper trading endpoint. To use the live trading endpoint, change the alpaca_endpoint value:

```python
alpaca_endpoint = 'https://api.alpaca.markets' # For live trading
```
## Running the Script
To run the script:


```bash
python sma_crossover_trader.py 
```

## Strategy
The script operates using a simple moving average crossover strategy. It trades a specified ticker (default is 'SPY') based on the relationship between two simple moving averages of specified lengths (default is 48 and 120 hours).

When the short-period SMA crosses above the long-period SMA, the script places a buy order. Conversely, when the short-period SMA crosses below the long-period SMA, the script places a sell order.

## Logging
The script logs activities to a file named sma_crossover_trader.log. The log file contains entries for when the script starts and actions performed such as buying or selling.

## Adjusting Parameters
You can adjust the ticker symbol and SMA periods at the bottom of the script:

```python
sma_crossover_trader('SPY', 48, 120)
```
Change 'SPY' to your preferred ticker symbol and adjust 48 and 120 to your desired SMA periods.

## Disclaimer
The code and information provided in this repository is for educational purposes only and should not be considered as financial advice. The author is not a financial advisor or broker, and assumes no liability for the use or interpretation of the code and information provided. Use of this code for trading purposes is at your own risk. It is important to do your own analysis and research before making any investment decisions.