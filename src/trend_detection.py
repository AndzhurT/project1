import numpy as np

def max_subarray(arr):
    max_sum = float('-inf')
    current_sum = 0
    start = end = temp_start = 0

    for i in range(len(arr)):
        current_sum += arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start  # Update start index
            end = i  # Update end index

        if current_sum < 0:
            current_sum = 0
            temp_start = i + 1  # Move start to the next element

    return max_sum, start, end


def max_crossing_subarray(arr, low, mid, high):
    left_sum = float('-inf')
    current_sum = 0
    max_left = mid
    for i in range(mid, low - 1, -1):
        current_sum += arr[i]
        if current_sum > left_sum:
            left_sum = current_sum
            max_left = i

    right_sum = float('-inf')
    current_sum = 0
    max_right = mid + 1
    for i in range(mid + 1, high + 1):
        current_sum += arr[i]
        if current_sum > right_sum:
            right_sum = current_sum
            max_right = i

    return left_sum + right_sum, max_left, max_right
