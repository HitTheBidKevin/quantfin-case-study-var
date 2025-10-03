import numpy as np
import pandas as pd

def calculate_historical_var(returns, confidence_level):
    """
    Calculate Historical VaR as a percentile of the return distribution.

    Parameters:
    - returns: pd.Series, portfolio returns over a period
    - confidence_level: float, confidence level (e.g., 0.95)

    Returns:
    - float: negative VaR percentile (positive number indicating loss)
    """
    return -np.percentile(returns, (1 - confidence_level) * 100)

def rolling_historical_var(returns_df, weights, window_years, confidence_level=0.95, trading_days_per_year=252):
    """
    Calculate rolling historical VaR for a weighted portfolio with fixed window size.

    Parameters:
    - returns_df: pd.DataFrame, asset returns (columns = assets)
    - weights: list or array-like, portfolio weights
    - window_years: int, window size in years
    - confidence_level: float
    - trading_days_per_year: int, default 252

    Returns:
    - pd.Series: rolling VaR index by window end date.
    """
    window_size = int(window_years * trading_days_per_year)
    step = trading_days_per_year

    portfolio_returns = (returns_df * weights).sum(axis=1)
    rolling_vars = []
    rolling_dates = []

    for start in range(0, len(portfolio_returns) - window_size + 1, step):
        window_returns = portfolio_returns.iloc[start:start+window_size]
        var = calculate_historical_var(window_returns, confidence_level)
        date_label = portfolio_returns.index[start + window_size - 1]
        rolling_vars.append(var)
        rolling_dates.append(date_label)

    return pd.Series(rolling_vars, index=rolling_dates)
