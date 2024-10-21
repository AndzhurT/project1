import pandas as pd

def clean_data(data):
    """Cleans the stock data by handling missing values and converting data types."""
    data['date'] = pd.to_datetime(data['date'])
    data = data.dropna()  # Remove rows with missing values
    return data
