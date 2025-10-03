import yfinance as yf
import pandas as pd

def download_prices(tickers, period):
    """
    Download adjusted close prices from Yahoo Finance.
    
    Parameters:
    - tickers: List[str], ticker symbols
    - period: str, data period for download (e.g., '10y')

    Returns:
    - pd.DataFrame: DataFrame with tickers as columns and datetime index.
    """
    data = yf.download(tickers, period=period)
    if isinstance(data.columns, pd.MultiIndex):
        if 'Adj Close' in data.columns.get_level_values(0):
            adj_close = data['Adj Close']
        elif 'Close' in data.columns.get_level_values(0):
            adj_close = data['Close']
        else:
            raise ValueError("No 'Adj Close' or 'Close' data found.")
    else:
        if 'Adj Close' in data.columns:
            adj_close = data[['Adj Close']]
            adj_close.columns = [tickers[0]]
        elif 'Close' in data.columns:
            adj_close = data[['Close']]
            adj_close.columns = [tickers[0]]
        else:
            raise ValueError("No 'Adj Close' or 'Close' data found.")
    if adj_close.isnull().all().all():
        raise ValueError("No valid price data found.")
    return adj_close
