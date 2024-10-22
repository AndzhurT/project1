import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_data
from data_processor import clean_data
from trend_detection import max_subarray
from visualizer import plot_buy_sell_opportunities, plot_stock_growth, plot_anomaly_report

DEFAULT_STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA']

def calculate_stock_growth_and_profit(data, selected_stocks):
    """Calculates and prints stock growth and max profit for selected stocks."""
    results = []

    for stock in selected_stocks:
        stock_data = data[data['Name'] == stock]

        # Check if stock_data is empty
        if stock_data.empty:
            print(f"Warning: No data found for stock '{stock}'. Skipping...")
            continue

        # Calculate growth percentage
        initial_price = stock_data.iloc[0]['close']
        final_price = stock_data.iloc[-1]['close']
        growth_percentage = ((final_price - initial_price) / initial_price) * 100

        # Calculate maximum profit using max_subarray function
        prices = stock_data['close'].values
        max_profit, buy_idx, sell_idx = max_subarray(prices)

        results.append({
            'Stock': stock,
            'Growth (%)': f"{growth_percentage:.2f}%",
            'Max Profit ($)': f"{max_profit:.2f}",
            'Buy Day': buy_idx,
            'Sell Day': sell_idx
        })

    # Print results in a tabular format
    print("\nStock Growth (%):")
    for result in results:
        print(f"{result['Stock']}: {result['Growth (%)']}")

    print("\nMax Profit Details:")
    for result in results:
        print(f"{result['Stock']} - Max Profit: {result['Max Profit ($)']}$ from day {result['Buy Day']} to {result['Sell Day']}")



def get_user_selected_stocks(data):
    """Prompt user to select stocks to visualize or use default."""
    available_stocks = data['Name'].unique()
    print("\nAvailable Stocks:", ', '.join(available_stocks))

    user_input = input(
        "\nEnter the stock symbols you want to visualize (comma-separated), or press Enter to use default: "
    ).strip()

    if user_input:
        selected_stocks = [stock.strip().upper() for stock in user_input.split(',')]
        valid_stocks = [s for s in selected_stocks if s in available_stocks]

        if not valid_stocks:
            print("\nNo valid stocks entered. Using default stocks.\n")
            return DEFAULT_STOCKS
        return valid_stocks
    else:
        print("\nUsing default stocks.\n")
        return DEFAULT_STOCKS

def main():
    # Load and clean data
    data = load_data('dataset/all_stocks_5yr.csv')  # Assuming load_data handles CSV reading
    cleaned_data = clean_data(data)

    # User input for report type
    print("Choose a report type:")
    print("1. Buy/Sell Opportunities")
    print("2. Stock Growth")
    print("3. Anomaly Report")
    choice = input("Enter the number corresponding to your choice: ")

    # Get user-selected stocks
    selected_stocks = get_user_selected_stocks(cleaned_data)

    calculate_stock_growth_and_profit(cleaned_data, selected_stocks)

    # Call the appropriate function based on user choice
    if choice == '1':
        plot_buy_sell_opportunities(cleaned_data, selected_stocks)
    elif choice == '2':
        plot_stock_growth(cleaned_data, selected_stocks)
    elif choice == '3':
        # User input for anomaly detection threshold
        while True:
            try:
                threshold = 10.0
                break  # Exit loop if conversion is successful
            except ValueError:
                print("Invalid input. Please enter a numeric value for the threshold.")
        plot_anomaly_report(cleaned_data, selected_stocks, threshold)
    else:
        print("Invalid choice. Please choose a valid report type.")

if __name__ == "__main__":
    main()
