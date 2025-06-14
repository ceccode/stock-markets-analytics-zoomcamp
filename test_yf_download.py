import pandas as pd
import yfinance as yf

# Test with known ticker and date range
def test_ticker(ticker="AAPL", days_back=90):
    print(f"Testing ticker: {ticker}")
    
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=days_back)
    
    print(f"Date range: {start_date} to {end_date}")
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=True)
        
        print(f"Data shape: {data.shape}")
        if not data.empty:
            print("First few rows:")
            print(data.head())
        else:
            print("No data returned")
        
        return data
    except Exception as e:
        print(f"Error downloading ticker: {e}")
        return None

# Test with an IPO from 2023
def test_ipo_ticker(ticker, ipo_date):
    print(f"Testing IPO ticker: {ticker} (IPO date: {ipo_date})")
    
    start = ipo_date - pd.Timedelta(days=5)
    end = ipo_date + pd.Timedelta(days=85)
    
    print(f"Date range: {start} to {end}")
    
    try:
        data = yf.download(ticker, start=start, end=end, progress=True)
        
        print(f"Full data shape: {data.shape}")
        
        # Filter to only dates on or after IPO
        filtered_data = data[data.index >= ipo_date]
        
        print(f"Filtered data shape (after IPO date): {filtered_data.shape}")
        
        if not filtered_data.empty:
            print("First few rows after filtering:")
            print(filtered_data.head())
        else:
            print("No data returned after filtering")
        
        return filtered_data
    except Exception as e:
        print(f"Error downloading ticker: {e}")
        return None

if __name__ == "__main__":
    # Test a known good ticker first
    test_ticker("AAPL")
    
    # Test with a 2023 IPO ticker
    test_ipo_ticker("RDDT", pd.Timestamp("2023-03-23"))
    
    # Test with a more recent IPO
    test_ipo_ticker("ARM", pd.Timestamp("2023-09-14"))
