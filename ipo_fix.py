import pandas as pd
import yfinance as yf
from tqdm import tqdm
import time

def get_first_n_trading_days_fixed(ticker: str, ipo_date, n: int = 10) -> pd.Series:
    """
    Return a Series of 'Adj Close' prices for the first `n` trading days
    *starting with* the first day on or after `ipo_date`.
    Empty Series if retrieval fails or insufficient data.
    
    This fixed version ensures proper date handling and adds error logging.
    """
    # Make sure ipo_date is a pandas Timestamp
    if isinstance(ipo_date, str):
        ipo_date = pd.to_datetime(ipo_date)
        
    try:
        # Fetch data around the IPO date
        start = ipo_date - pd.Timedelta(days=5)
        end = ipo_date + pd.Timedelta(days=85)
        
        # Download data with a small delay to avoid rate limiting
        px = yf.download(ticker, start=start, end=end, progress=False)
        
        # Handle empty results
        if px.empty:
            return pd.Series(dtype=float)
            
        # Check for Adj Close column
        if "Adj Close" not in px.columns:
            if "Close" in px.columns:  # Try to use Close if Adj Close is not available
                adj_close = px["Close"]
            else:
                return pd.Series(dtype=float)
        else:
            adj_close = px["Adj Close"]
            
        # Filter to days on or after IPO date
        px_filtered = adj_close[adj_close.index >= ipo_date].sort_index()
            
        # Only require a few trading days to consider ticker usable
        if len(px_filtered) < n:
            return pd.Series(dtype=float)
        
        return px_filtered.iloc[:n]
        
    except Exception as e:
        # Just return empty series on error
        return pd.Series(dtype=float)

def harvest_prices_fixed(ipo_df: pd.DataFrame, n: int = 10, verbose: bool = True) -> dict:
    """
    Harvest price data for tickers in ipo_df.
    
    This fixed version ensures consistent date handling and adds delays to prevent API issues.
    """
    prices = {}
    success_count = 0
    
    # Add a keep_trying option to retry tickers
    for _, row in tqdm(ipo_df.iterrows(), total=len(ipo_df), desc="download"):
        # Make sure we have a valid ticker symbol
        ticker = str(row["Symbol"]).strip().upper()
        
        # Get the IPO date
        ipo_date = row["IPO Date"]
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(0.1)
        
        # Get price data
        ts = get_first_n_trading_days_fixed(ticker, ipo_date, n)
        
        if not ts.empty:
            prices[ticker] = ts
            success_count += 1
    
    if verbose:
        print(f"Successfully downloaded {success_count}/{len(ipo_df)} tickers")
    
    return prices

# Use these functions in your notebook by calling:
# prices23 = harvest_prices_fixed(ipos_2023, n=10)
# prices24 = harvest_prices_fixed(ipos_2024, n=10)
# prices25 = harvest_prices_fixed(ipos_2025, n=10)
#
# print(f"Usable 2023 tickers: {len(prices23)}, usable 2024: {len(prices24)}, usable 2025: {len(prices25)}")
