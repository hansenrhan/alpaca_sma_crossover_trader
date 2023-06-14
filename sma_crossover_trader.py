#DISCLAIMER: 
#This example is purely for research illustrative purposes only. 
#Past performance is not indicative of future results. 

#Import necessary packages
import alpaca_trade_api as tradeapi
import time
import datetime
from datetime import timedelta
from pytz import timezone
import logging
import math

#Setup logging
logging.basicConfig(filename='./sma_crossover_trader.log', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('{} logging started'.format(datetime.datetime.now().strftime("%x %X")))

#Configure twitter and alpaca API
tz = timezone('EST')
alpaca_api_key = 'YOUR-API-KEY'
alpaca_api_secret = 'YOUR-API-SECRET'
alpaca_endpoint = 'https://paper-api.alpaca.markets' 
alpaca_api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, alpaca_endpoint)
account = alpaca_api.get_account()

#Determine the time until the market opens 
def time_to_open(current_time):
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds


def sma_crossover_trader(symbol, short_period, long_period):
    """
    symbol: the ticker to be traded
    short_period: the length of the short moving average (in hours)
    long_period: the length of the long moving average (in hours)
    """
    # Get historical data
    print('sma_crossover_trader started')

    #setup context variables
    current_average_higher = None
    last_average_higher = None
    
    while True:
        # Check if Monday-Friday
        if datetime.datetime.now(tz).weekday() >= 0 and datetime.datetime.now(tz).weekday() <= 4:
            # Checks market is open
            print('Trading day')
            if datetime.datetime.now(tz).time() > datetime.time(9, 30) and datetime.datetime.now(tz).time() <= datetime.time(15, 30):
                historical_data = alpaca_api.get_barset(symbol, 'hour', limit=long_period+1).df[symbol]

                # Get the moving averages
                short_ma = historical_data['close'].rolling(window=short_period).mean().iloc[-1]
                long_ma = historical_data['close'].rolling(window=long_period).mean().iloc[-1]

                if short_ma >= long_ma:
                    current_average_higher = "Short"
                else:
                    current_average_higher = "Long"

                # Buy Signal
                if current_average_higher == "Short" and last_average_higher == "Long":
                    # calculate how many shares you can purchase at the given moment
                    
                    # retrieve the buying power
                    buying_power = float(account.buying_power)

                    # Retrieve the last trade information for the symbol
                    last_trade = alpaca_api.get_last_trade(symbol=symbol)

                    # Get the current price from the last trade
                    current_price = last_trade.price

                    purchase_size = math.floor(buying_power/current_price)

                    order = alpaca_api.submit_order(
                        symbol=symbol,
                        qty=purchase_size,
                        side="buy",
                        type="market",
                        time_in_force='gtc'
                    )
                    
                # Sell Signal
                elif current_average_higher == "Long" and last_average_higher == "Short":
                    # check if you have stock
                    position = alpaca_api.get_position(symbol)

                    if position > 0:
                        order = alpaca_api.submit_order(
                            symbol=symbol,
                            qty=position,
                            side="sell",
                            type="market",
                            time_in_force='gtc'
                        )
                
                last_average_higher = current_average_higher
                            
                #Checks sentiment every hour (may be very interesting to experiment with further!)         
                time.sleep(3600)
            else:
                # Get time amount until open, sleep that amount
                print('Market closed ({})'.format(datetime.datetime.now(tz)))
                print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')
                time.sleep(time_to_open(datetime.datetime.now(tz)))
        else:
            # If not trading day, find out how much until open, sleep that amount
            print('Market closed ({})'.format(datetime.datetime.now(tz)))
            print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')
            time.sleep(time_to_open(datetime.datetime.now(tz)))


#Run strategy on S&P500 ETF with a 48h and 120h moving averages
sma_crossover_trader('SPY', 48, 120)
