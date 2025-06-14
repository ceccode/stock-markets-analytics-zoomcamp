import pandas as pd

def make_return_matrix_fixed(price_dict: dict, max_horizon: int = 30) -> pd.DataFrame:
    """
    Rows: tickers, Cols: day-X total return (AdjClose_t / AdjClose_0 − 1).
    
    This fixed version handles price series with DateTimeIndex correctly.
    """
    mat = pd.DataFrame(index=price_dict.keys(),
                       columns=range(1, max_horizon + 1),
                       dtype=float)

    for tkr, px in price_dict.items():
        # Make sure we have enough data points
        if len(px) <= max_horizon:
            continue
            
        # Get the first price (base price)
        base = px.iloc[0]
        
        # Calculate returns for each time horizon
        for x in mat.columns:
            if x < len(px):  # Check that we have enough data points
                mat.loc[tkr, x] = px.iloc[x] / base - 1.0
    
    return mat

# Example usage in your notebook:
# rets23 = make_return_matrix_fixed(prices23)
# rets24 = make_return_matrix_fixed(prices24)
# rets25 = make_return_matrix_fixed(prices25)
