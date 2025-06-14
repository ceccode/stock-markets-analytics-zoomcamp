import pandas as pd
import yfinance as yf
from tqdm import tqdm

# Original function with debugging added
def get_first_n_trading_days_improved(ticker: str, ipo_date: pd.Timestamp, n: int = 40, debug: bool = True) -> pd.Series:
    """
    Return a Series of 'Adj Close' prices for the first `n` trading days
    *starting with* the first day on or after `ipo_date`.
    Empty Series if retrieval fails or insufficient data.
    """
    if debug:
        print(f"Processing {ticker} with IPO date {ipo_date}")
        
    try:
        # Fetch max 90 days around the IPO to be safe
        start = ipo_date - pd.Timedelta(days=5)
        end = ipo_date + pd.Timedelta(days=85)
        
        # Remove the debug print that might be causing issues
        # print(start, end)  # <-- This was causing problems
        
        # Add more verbose output in debug mode
        if debug:
            print(f"  Date range: {start} to {end}")
            
        # Download the data with progress=False to avoid cluttering output
        px = yf.download(ticker, start=start, end=end, progress=False)
        
        if px.empty:
            if debug:
                print(f"  No data found for {ticker}")
            return pd.Series(dtype=float)
            
        # Add column check
        if "Adj Close" not in px.columns:
            if debug:
                print(f"  'Adj Close' column not found for {ticker}. Available columns: {px.columns.tolist()}")
            if "Close" in px.columns:  # Try to use Close if Adj Close is not available
                adj_close = px["Close"]
            else:
                return pd.Series(dtype=float)
        else:
            adj_close = px["Adj Close"]
            
        # Align to the first trading day *on or after* the IPO calendar date
        px_filtered = adj_close[adj_close.index >= ipo_date].sort_index()
        
        if debug:
            print(f"  Found {len(px_filtered)} trading days after IPO date")
            
        if len(px_filtered) < n:  # Too few data points – drop
            if debug:
                print(f"  Insufficient data: only {len(px_filtered)} days (need {n})")
            return pd.Series(dtype=float)
        
        if debug:
            print(f"  Successfully returning {n} days of data")
        return px_filtered.iloc[:n]  # first n trading days
        
    except Exception as e:
        if debug:
            print(f"  Error processing {ticker}: {str(e)}")
        return pd.Series(dtype=float)
        
# Test function to see what's happening with our IPO data
def test_harvesting(ipos_df, year, sample_size=5):
    """Test the data harvesting on a sample of the IPOs dataframe"""
    
    print(f"\nTesting {year} IPOs (sample of {sample_size}):")
    
    if len(ipos_df) == 0:
        print(f"No IPOs found for {year}")
        return {}
        
    # Take a sample for testing
    sample = ipos_df.sample(min(sample_size, len(ipos_df)))
    
    prices = {}
    successful = 0
    
    for _, row in sample.iterrows():
        ticker = row["Symbol"]
        ipo_date = row["IPO Date"]
        
        # Use our improved function with debug=True
        ts = get_first_n_trading_days_improved(ticker, ipo_date, n=31, debug=True)
        
        if not ts.empty:
            prices[ticker] = ts
            successful += 1
    
    print(f"Processed {len(sample)} tickers, {successful} were successful.")
    print(f"Success rate: {successful/len(sample)*100:.1f}%")
    
    return prices

# Main execution
# This script should be copied and pasted into a cell in your notebook
# or imported into the notebook, then run with your actual IPO dataframes

# Example usage would be:
# test_harvesting(ipos_2023, "2023", sample_size=10)
# test_harvesting(ipos_2024, "2024", sample_size=10)
# test_harvesting(ipos_2025, "2025", sample_size=10)
