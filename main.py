# Andzhur Terminkeev
# CMPSC 463 - Design Analysis Algorithms
# Project 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import math

# First exercise

# Merge Sort Implementation for Time-Series Sorting
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    sorted_arr = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

# Load dataset and sort by date using Merge Sort 
data = pd.read_csv("dataset/all_stocks_5yr.csv")
data_np = data[['date', 'close', 'Name']].to_records(index=False)
sorted_data = merge_sort(data_np, key=0)
print(f"First 10 sorted entries:\n{sorted_data[:10]}")

# Second exericse

# Divide-and-conquer algorithm for maximum subarray (Kadane’s Algorithm for 1D & 2D)
def max_subarray(arr, low, high):
    # Base case: only one element
    if low == high:
        return arr[low], low, high  # Return the single element and its indices

    mid = (low + high) // 2

    # Find the maximum subarray sum in left half
    left_max, left_start, left_end = max_subarray(arr, low, mid)
    # Find the maximum subarray sum in right half
    right_max, right_start, right_end = max_subarray(arr, mid + 1, high)

    # Find the maximum subarray sum crossing the midpoint
    cross_max, cross_start, cross_end = max_crossing_subarray(arr, low, mid, high)

    # Return the maximum of the three
    if left_max >= right_max and left_max >= cross_max:
        return left_max, left_start, left_end
    elif right_max >= left_max and right_max >= cross_max:
        return right_max, right_start, right_end
    else:
        return cross_max, cross_start, cross_end

def max_crossing_subarray(arr, low, mid, high):
    # Find max sum on left side
    left_sum = float('-inf')
    current_sum = 0
    max_left = mid

    for i in range(mid, low - 1, -1):
        current_sum += arr[i]
        if current_sum > left_sum:
            left_sum = current_sum
            max_left = i

    # Find max sum on right side
    right_sum = float('-inf')
    current_sum = 0
    max_right = mid + 1

    for i in range(mid + 1, high + 1):
        current_sum += arr[i]
        if current_sum > right_sum:
            right_sum = current_sum
            max_right = i

    # Return the combined sum and the indices
    return left_sum + right_sum, max_left, max_right

price_changes = np.diff([record[1] for record in data_np])

max_profit, start_idx, end_idx = max_subarray(price_changes, 0, len(price_changes) - 1)

# get the stock start and end date
start_date = data_np[start_idx + 1][0]
end_date = data_np[end_idx + 1][0]

# Get the stock name using the start index (the +1 accounts for the diff)
stock_name = data_np[start_idx + 1][2] 

print(f"Max Profit: {max_profit}, Start Date: {start_date}, End Date: {end_date}, Stock Name: {stock_name}")


# Third Exercise:
