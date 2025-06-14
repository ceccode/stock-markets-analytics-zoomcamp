import pandas as pd
import numpy as np

def make_return_matrix_robust(price_dict: dict, max_horizon: int = 30) -> pd.DataFrame:
    """
    Creates a matrix of returns for different time horizons from price data.
    Rows: tickers, Cols: day-X total return (price_t / price_0 - 1)
    
    This robust version handles different price series formats and properly
    deals with price data from yfinance.
    """
    # Initialize return matrix
    mat = pd.DataFrame(index=list(price_dict.keys()),
                      columns=range(1, max_horizon + 1),
                      dtype=float)
    
    # Fill with NaN as default
    mat.loc[:, :] = np.nan
    
    # Process each ticker
    for tkr, px in price_dict.items():
        # Skip empty series
        if px.empty:
            continue
        
        # Get base price (first trading day)
        base_price = float(px.iloc[0])
        
        # Check for reasonable base price
        if base_price <= 0 or pd.isna(base_price):
            continue
        
        # Calculate return for each horizon day
        days_available = min(len(px), max_horizon + 1)
        
        for day in range(1, days_available):
            try:
                # Get price at this horizon
                price_at_day = float(px.iloc[day])
                
                # Calculate return
                if price_at_day > 0 and not pd.isna(price_at_day):
                    return_val = price_at_day / base_price - 1.0
                    mat.loc[tkr, day] = return_val
            except (IndexError, ValueError, TypeError) as e:
                # Skip problematic values
                continue
    
    return mat

# For debugging: print details about price data structure
def diagnose_price_data(price_dict):
    """Diagnose the structure of price data to help debug issues"""
    print(f"Number of tickers in price dict: {len(price_dict)}")
    
    if not price_dict:
        print("Price dictionary is empty!")
        return
        
    # Take first ticker as sample
    sample_ticker = next(iter(price_dict))
    sample_data = price_dict[sample_ticker]
    
    print(f"\nSample ticker: {sample_ticker}")
    print(f"Type of price data: {type(sample_data)}")
    print(f"Index type: {type(sample_data.index)}")
    print(f"Data shape: {sample_data.shape}")
    print(f"First few index values: {sample_data.index[:3].tolist() if len(sample_data) >= 3 else sample_data.index.tolist()}")
    
    # Print the first few values
    print("\nFirst few values:")
    print(sample_data.head(3) if hasattr(sample_data, 'head') else sample_data[:3])

# Example usage in notebook
"""
# First diagnose the price data structure
diagnose_price_data(prices23)

# Then use the robust function
rets23 = make_return_matrix_robust(prices23)
rets24 = make_return_matrix_robust(prices24)
rets25 = make_return_matrix_robust(prices25)

# Verify shapes
print(f"Return matrices shapes - 2023: {rets23.shape}, 2024: {rets24.shape}, 2025: {rets25.shape}")
"""
