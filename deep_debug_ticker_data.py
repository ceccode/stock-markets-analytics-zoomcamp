import pandas as pd
import yfinance as yf
import json
import os
import time
from tqdm import tqdm

# Function to inspect the IPO data structure and do detailed debugging
def inspect_ipo_data(notebook_path):
    """Extract and inspect IPO data from the notebook file"""
    
    print("Reading notebook file...")
    with open(notebook_path, 'r') as f:
        nb_content = f.read()
    
    # Try to find if there's a problem with date conversion
    print("\nChecking IPO data format from a sample...")
    
    # Create a minimal test function to debug one ticker at a time
    def debug_single_ticker(ticker, ipo_date_str):
        print(f"\nDebugging ticker: {ticker} with date string: {ipo_date_str}")
        
        # Check if the date is a string and needs conversion
        if isinstance(ipo_date_str, str):
            try:
                ipo_date = pd.to_datetime(ipo_date_str)
                print(f"Converted date string to timestamp: {ipo_date}")
            except Exception as e:
                print(f"Error converting date: {e}")
                return False
        else:
            ipo_date = ipo_date_str
            print(f"Using provided date object: {ipo_date}")
            
        # Set up date range
        start = ipo_date - pd.Timedelta(days=5)
        end = ipo_date + pd.Timedelta(days=85)
        print(f"Date range: {start} to {end}")
        
        # Attempt download with detailed error reporting
        try:
            print(f"Attempting to download data for {ticker}...")
            data = yf.download(ticker, start=start, end=end, progress=False)
            
            if data.empty:
                print("Download completed but returned empty DataFrame")
                print("Testing with a standard ticker (AAPL) to check API connectivity...")
                
                control_data = yf.download("AAPL", start=start, end=end, progress=False)
                if control_data.empty:
                    print("Control test failed too - possible API connectivity issue")
                else:
                    print(f"Control test succeeded with {len(control_data)} rows - API is working")
                    
                return False
            else:
                print(f"Success! Downloaded {len(data)} rows of data")
                print("First 2 rows:")
                print(data.head(2))
                return True
                
        except Exception as e:
            print(f"Error during download: {e}")
            return False
    
    # Test a few sample tickers from each year with explicit dates
    print("\n--- Testing sample IPO tickers with explicit dates ---")
    
    # Test 2023 IPOs
    test_cases = [
        # A few sample tickers from 2023
        ("ARM", "2023-09-14"),  # Arm Holdings - a well-known 2023 IPO
        ("RDDT", "2023-03-23"), # Reddit - should be a known ticker
        ("CVKD", "2023-01-20"), # Random 2023 IPO
        
        # A few sample tickers from 2024
        ("CHEB", "2024-06-07"), # From your output
        ("RAPP", "2024-06-07"), # From your output
        
        # A few sample tickers from 2025
        ("OMDA", "2025-06-06"), # From your output
        ("CRCL", "2025-06-05"), # From your output
    ]
    
    results = {
        "success": 0,
        "failure": 0
    }
    
    for ticker, date_str in test_cases:
        success = debug_single_ticker(ticker, date_str)
        if success:
            results["success"] += 1
        else:
            results["failure"] += 1
        
        # Add a brief delay to avoid rate limiting
        time.sleep(1)
    
    print("\n--- Summary ---")
    print(f"Test cases run: {len(test_cases)}")
    print(f"Successful: {results['success']}")
    print(f"Failed: {results['failure']}")
    
    print("\nPossible issues:")
    if results['success'] == 0:
        print("1. Yahoo Finance API access issue - no tickers work")
        print("2. Date format issues across all IPOs")
        print("3. All ticker symbols might need formatting")
    elif results['failure'] > 0:
        print("1. Some tickers work but others don't - check ticker symbol format")
        print("2. Recent IPOs might not have data yet")
        print("3. Some dates might be incorrect")
    
    # Final diagnosis
    if results['success'] > 0:
        print("\nDiagnosis: Some tickers work but others don't. Focus on filtering working tickers.")
    else:
        print("\nDiagnosis: Critical issue - no tickers work. Focus on API connectivity, date formats, or data source.")

if __name__ == "__main__":
    # Path to your notebook file
    notebook_path = "/Users/francesco/Dev/stock-markets-analytics-zoomcamp/02-dataframe-analysis/[2025]_Module_02_Colab_Working_with_the_data.ipynb"
    
    inspect_ipo_data(notebook_path)
