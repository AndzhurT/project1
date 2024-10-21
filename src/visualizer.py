import matplotlib.pyplot as plt
from anomaly_detection import detect_anomalies
from trend_detection import max_subarray
import pandas as pd


def plot_data(data):
    """Plots the closing prices over time for selected stocks."""
    plt.figure(figsize=(10, 6))
    for stock_name, stock_data in data.groupby('Name'):
        plt.plot(
            stock_data['date'], 
            stock_data['close'], 
            label=f"{stock_name} (Growth: {calculate_stock_growth(stock_data):.2f}%)"
        )

    plt.title("Stock Closing Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def highlight_anomalies(data, stock_name, anomaly_indices):
    """Highlights anomalies on the plot for a specific stock."""
    stock_data = data[data['Name'] == stock_name]
    plt.figure(figsize=(10, 6))
    
    # Plot the normal price trend
    plt.plot(stock_data['date'], stock_data['close'], label=f"{stock_name} Price", color='blue')

    # Highlight the anomalies with red markers
    for idx in anomaly_indices:
        plt.plot(
            stock_data.iloc[idx]['date'], 
            stock_data.iloc[idx]['close'], 
            marker='o', color='red', markersize=8, label="Anomaly"
        )

    plt.title(f"{stock_name} - Highlighted Anomalies")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def calculate_stock_growth(stock_data):
    """Calculates the percentage growth for a specific stock."""
    initial_price = stock_data.iloc[0]['close']
    final_price = stock_data.iloc[-1]['close']
    return ((final_price - initial_price) / initial_price) * 100

def plot_stock_growth(data, selected_stocks):
    """Plot stock growth for selected stocks."""
    plt.figure(figsize=(12, 6))

    for stock in selected_stocks:
        stock_data = data[data['Name'] == stock]
        plt.plot(stock_data['date'], stock_data['close'], label=stock)

    plt.title('Stock Growth Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend(loc='best')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_anomaly_report(data, selected_stocks, threshold):
    """Visualize anomalies for selected stocks."""
    plt.figure(figsize=(12, 6))

    for stock in selected_stocks:
        stock_data = data[data['Name'] == stock]
        anomalies = detect_anomalies(stock_data, threshold)
        
        plt.plot(stock_data['date'], stock_data['close'], label=stock)
        
        # Check if anomalies is a DataFrame
        if isinstance(anomalies, pd.DataFrame):
            # Mark anomalies
            plt.scatter(anomalies['date'], anomalies['close'], color='red', marker='x', label='Anomalies')
        else:
            # If anomalies is a list, extract dates and closing prices
            anomaly_dates = [anomaly['date'] for anomaly in anomalies]
            anomaly_prices = [anomaly['close'] for anomaly in anomalies]
            plt.scatter(anomaly_dates, anomaly_prices, color='red', marker='x', label='Anomalies')

    plt.title('Anomaly Detection in Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend(loc='best')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_buy_sell_opportunities(data, selected_stocks):
    """Plot closing price trends for selected stocks with buy/sell markers."""
    plt.figure(figsize=(12, 6))

    for stock in selected_stocks:
        stock_data = data[data['Name'] == stock]
        prices = stock_data['close'].values
        dates = stock_data['date'].values

        # Calculate the buy and sell points using Kadane's Algorithm
        max_profit, buy_idx, sell_idx = max_subarray(prices)

        # Plot the stock's closing price trend
        plt.plot(dates, prices, label=stock)

        # Highlight the buy and sell points
        plt.scatter(dates[buy_idx], prices[buy_idx], color='green', marker='^', s=100, label=f'{stock} Buy')
        plt.scatter(dates[sell_idx], prices[sell_idx], color='red', marker='v', s=100, label=f'{stock} Sell')

    plt.title('Stock Closing Prices with Buy/Sell Opportunities')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend(loc='best')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
