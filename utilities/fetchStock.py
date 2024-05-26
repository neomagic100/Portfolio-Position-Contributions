import traceback
from enum import Enum
from datetime import datetime, time
import pytz
import yfinance as yf

class Day(Enum):
    MONDAY    = 0
    TUESDAY   = 1
    WEDNESDAY = 2
    THURSDAY  = 3
    FRIDAY    = 4
    SATURDAY  = 5
    SUNDAY    = 6
    
_NEW_YORK_TZ = pytz.timezone('America/New_York')

class StockTickerData:
    def __init__(self, tickerData = None):
        """
         @brief Initialize the object with an optional paramater of data.
         @param tickerData A dictionary of ticker data. (default = None)
        """
        self.tickerData = {} if not tickerData else tickerData
    
    def addTickerData(self, symbol, data):
        """
         @brief Set the ticker data for a symbol.
         @param symbol The stock symbol to use as a key
         @param data The yfinance fastData to be saved
        """
        self.tickerData[symbol] = data
    
    def getTickerData(self):
        """
         @brief Returns the ticker data for all saved positions
         @return A dictionary that maps symbol to the ticker data of that stock
        """
        return self.tickerData
    
    def getTickerDataForSymbol(self, symbol):
        """
         @brief Get the ticker data for only one position. 
         @param symbol The symbol to look up.
         @return The ticker data or None if not found.
        """
        # Returns the ticker data if any.
        if not self.tickerData:
            return None
        
        try:
            data = self.tickerData[symbol]
        except KeyError:
            return None
        
        return data

def _fetchTickers(stocks, tickerData):
    """
     @brief Fetches information about the tickers. This is a wrapper for yf. Tickers which does not require a lot of API calls
     @param stocks List of stock symbols to fetch information for
     @param tickerData A dictionary of symbols to yfinance Ticker Data. Can be an empty dictionary to populate.
     @return Dict with ticker : fastData for each ticker in stocks or {} if there is no ticker for any stocks
    """
    try:
        fastData = {}
        # Get fast info for each stock
        if len(stocks) == 1:
            ticker = yf.Ticker(stocks[0])
            fastData[ticker.ticker] = ticker.get_fast_info()
            tickerData.addTickerData(ticker.ticker, ticker)
        else:
            tickerList = yf.Tickers(stocks)
            # Get fast data for each symbol in tickerList. tickers
            for symbol in tickerList.tickers:
                ticker = tickerList.tickers[symbol]    
                fastData[symbol] = ticker.get_fast_info()
                tickerData.addTickerData(symbol, ticker)
            
        return fastData

    except ValueError as e:
        print(f"Invalid stock symbol: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def _getPrice(data):
    """
     @brief Get the price of the stock current value. This is based on the market state or the previous close price.
     @param data Ticker object of a stock
     @return Price of the trade as a float between 0 and 1. If the market is open it will return the last price
    """
    price = data["lastPrice"] if _isMarketOpen() else data["previousClose"]
    return price

def _getPrices(tickerFastData):
    """
     @brief Get prices for each ticker. This is a wrapper around _getPrice to avoid having to re - map the ticker data
     @param tickerFastData dictionary of ticker data. ( {symbol: Ticker} )
     @return dictionary of ticker data with price in decimal format ( {symbol: Price} )
    """
    prices = {}
    
    # Get the price of the ticker data for each symbol.
    for symbol, tickerData in tickerFastData.items():
        prices[symbol] = _getPrice(tickerData)

    return prices
        
def _isMarketOpen():
   """
    @brief Check if market is open. Determine if we're on the market's day and time that is a weekday and open time.
    @return True if market is open False otherwise. Note that the return value does not depend on the state of the system
   """
   newYorkNow = datetime.now(_NEW_YORK_TZ)
   dateNow = newYorkNow.date()
   timeNow = newYorkNow.time()
   return _isWeekday(dateNow) and _isOpenTime(timeNow)
   
def _isWeekday(dateObj):
    """
     @brief Checks if dateObj is a weekday.
     @param dateObj the date to examine.
     @return C { True } if the dateObj is a weekday C { False } otherwise. >>> _isWeekday ( date )
    """
    return dateObj.weekday() != Day.SATURDAY and dateObj.weekday() != Day.SUNDAY

def _isOpenTime(timeObj):
    """
     @brief Check if timeObj is between 9:30 AM and 4:30 PM.
     @param timeObj A datetime object representing the time to check
     @return True if timeObj is between9:30 AM and 4:30 PM. False otherwise
    """
    openTime  = time(hour = 9, minute = 30, tzinfo = _NEW_YORK_TZ)
    closeTime = time(hour = 16, minute = 30, tzinfo = _NEW_YORK_TZ)
    return timeObj > openTime and timeObj < closeTime

def fetchLatestPrices(stocks, tickerData):
    """
     @brief Get the latest prices for a list of stocks. This is a wrapper around _fetchTickers to allow us to do this in one call
     @param stocks A list of stock symbols to query ( ['AAPL', 'MSFT'] )
     @param tickerData A dictionary of symbols to yfinance Ticker Data. Can be an empty dictionary to populate.
     @return A dictionary of prices keyed by stock ( ex. {'AAPL': 1234.56, 'MSFT': 5678.90} )
    """
    marketData = _fetchTickers(stocks, tickerData)
    prices = _getPrices(marketData)
    return prices
