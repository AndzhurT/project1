import math
import pandas as pd

def closest_pair(points):
    # Save the original points to retrieve indices later
    original_points = points.copy()
    
    # Sort points by x-coordinate
    points = sorted(points, key=lambda x: x[0])  # Sort by x-coordinates
    return closest_pair_recursive(points, original_points)

def closest_pair_recursive(points, original_points):
    if len(points) <= 3:
        return brute_force_closest_pair(points, original_points)

    mid = len(points) // 2
    left = points[:mid]
    right = points[mid:]

    # Recursively find the closest pair in both halves
    d_left, p1_left, p2_left, idx1_left, idx2_left = closest_pair_recursive(left, original_points)
    d_right, p1_right, p2_right, idx1_right, idx2_right = closest_pair_recursive(right, original_points)

    # Find the minimum distance and corresponding points
    d = min(d_left, d_right)
    if d == d_left:
        min_pair = (p1_left, p2_left, idx1_left, idx2_left)
    else:
        min_pair = (p1_right, p2_right, idx1_right, idx2_right)

    # Check for points close to the dividing line
    strip = [p for p in points if abs(p[0] - points[mid][0]) < d]
    strip_closest, s1, s2, idx1, idx2 = brute_force_closest_pair(strip, original_points)

    # Return the closest pair found
    if strip_closest < d:
        return strip_closest, s1, s2, idx1, idx2
    return d, *min_pair

def brute_force_closest_pair(points, original_points):
    min_dist = float('inf')
    p1 = p2 = None
    idx1 = idx2 = None
    
    # Iterate over all pairs of points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.dist(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = points[i], points[j]
                idx1, idx2 = original_points.index(p1), original_points.index(p2)  # Get indices
    return min_dist, p1, p2, idx1, idx2

def detect_anomalies(data, threshold):
    anomalies = []
    points = list(zip(data['close'], range(len(data))))  # Using closing prices as points

    min_dist, p1, p2, idx1, idx2 = closest_pair(points)

    # Use the closest pair distance to find potential anomalies
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if math.dist(points[i], points[j]) > threshold:
                anomalies.append(data.iloc[j])  # Append the anomaly data point
    return pd.DataFrame(anomalies)  # Return anomalies as a DataFrame
