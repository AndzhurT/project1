import pandas as pd

def load_data(file_path):
    """Loads data from a CSV file."""
    return pd.read_csv(file_path)

def load_yahoo_data(ticker, start_date, end_date):
    """Loads data from Yahoo Finance for a specific ticker."""
    import yfinance as yf
    return yf.download(ticker, start=start_date, end=end_date)
