import ccxt
import pandas as pd
import time

def get_coinbase_ohlcv(symbol, timeframe, limit=100):
    """
    Fetches OHLCV data from Coinbase Advanced Trade.

    Args:
        symbol (str): The trading pair (e.g., 'BTC/USDT').
        timeframe (str): The candlestick interval ('1m', '5m', '1h', '1d', etc.).
        limit (int): The number of data points to fetch.

    Returns:
        pandas.DataFrame: A DataFrame with OHLCV data or None on error.
    """
    try:
        # We use 'coinbasepro' as the ID to access the advanced trading API.
        exchange = ccxt.coinbasepro()
        
        # Load the market information to ensure the symbol exists
        exchange.load_markets()
        
        if symbol not in exchange.markets:
            print(f"Error: Symbol '{symbol}' not found on Coinbase.")
            return None
        
        print(f"Fetching {limit} {timeframe} candles for {symbol} from Coinbase...")
        
        # Fetch the OHLCV data using the specified parameters
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        if not ohlcv:
            print(f"No data found for {symbol} with timeframe {timeframe}.")
            return None

        # Convert the list of lists into a pandas DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Convert the timestamp to a readable datetime format and set it as the index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df

    except ccxt.NetworkError as e:
        print(f"Network error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # --- Tunable Variables ---
    SYMBOL = 'BTC/USDT'     # Try other pairs like 'ETH/USDT', 'SOL/USD', etc.
    LIMIT = 20              # Number of data points to fetch

    # --- Fetching minute data ---
    MINUTE_TIMEFRAME = '1m'
    minute_data = get_coinbase_ohlcv(SYMBOL, MINUTE_TIMEFRAME, LIMIT)
    if minute_data is not None:
        print(f"\n--- {MINUTE_TIMEFRAME} Data for {SYMBOL} ---\n")
        print(minute_data)
        print("\n" + "="*50 + "\n")

    # --- Fetching hourly data ---
    HOURLY_TIMEFRAME = '1h'
    hourly_data = get_coinbase_ohlcv(SYMBOL, HOURLY_TIMEFRAME, LIMIT)
    if hourly_data is not None:
        print(f"--- {HOURLY_TIMEFRAME} Data for {SYMBOL} ---\n")
        print(hourly_data)
        print("\n" + "="*50 + "\n")
        
    # --- Fetching daily data ---
    DAILY_TIMEFRAME = '1d'
    daily_data = get_coinbase_ohlcv(SYMBOL, DAILY_TIMEFRAME, LIMIT)
    if daily_data is not None:
        print(f"--- {DAILY_TIMEFRAME} Data for {SYMBOL} ---\n")
        print(daily_data)coinbase
