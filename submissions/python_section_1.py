from typing import Dict, List

import pandas as pd

#Question1:-
def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    # Your code goes here.
    result = []
    for i in range(0, len(lst), n):
        start = i
        end = min(i + n, len(lst))
        while start < end - 1:
            lst[start], lst[end - 1] = lst[end - 1], lst[start]
            start += 1
            end -= 1
        result.extend(lst[i:i+n])
    return lst

# Get user input
lst = input("Enter a list of numbers (space-separated): ")
lst = [int(x) for x in lst.split()]
n = int(input("Enter the value of n: "))

# Call the function and print the result
print("Original List:", lst)
print("Reversed List:", reverse_by_n_elements(lst, n))


#Question2:-
def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    """
    Groups the strings by their length and returns a dictionary.
    """
    # Your code here
    result = {}
    for string in lst:
        length = len(string)
        if length in result:
            result[length].append(string)
        else:
            result[length] = [string]
    return dict(sorted(result.items()))

# Get user input
lst = input("Enter a list of strings (space-separated): ").split()

# Call the function and print the result
print("Grouped by length:")
print(group_by_length(lst))

#Question3:-
def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    """
    Flattens a nested dictionary into a single-level dictionary with dot notation for keys.
    
    :param nested_dict: The dictionary object to flatten
    :param sep: The separator to use between parent and child keys (defaults to '.')
    :return: A flattened dictionary
    """
    # Your code here
    flattened_dict = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            for subkey, subvalue in flatten_dict(value, sep).items():
                flattened_dict[f"{key}{sep}{subkey}"] = subvalue
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    for subkey, subvalue in flatten_dict(item, sep).items():
                        flattened_dict[f"{key}{sep}{index}{sep}{subkey}"] = subvalue
                else:
                    flattened_dict[f"{key}{sep}{index}"] = item
        else:
            flattened_dict[key] = value
    return dict

# Get user input
nested_dict = eval(input("Enter a nested dictionary: "))

# Call the function and print the result
print("Flattened Dictionary:")
print(flatten_dict(nested_dict))
    
#Question4:-
def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    
    :param nums: List of integers (may contain duplicates)
    :return: List of unique permutations
    """
    # Your code here
import itertools

def unique_permutations(nums: List[int]) -> List[List[int]]:
    """Generate all unique permutations of a list that may contain duplicates."""
    # Generate all permutations
    perms = itertools.permutations(nums)
    # Convert to list and remove duplicates
    unique_perms = [list(x) for x in set(perms)]
    return unique_perms

# Get user input
nums = input("Enter a list of integers (space-separated): ")
nums = [int(x) for x in nums.split()]

# Call the function and print the result
print("Unique Permutations:")
print(unique_permutations(nums))


#Question5:-
import re
def find_all_dates(text: str) -> List[str]:
    """
    This function takes a string as input and returns a list of valid dates
    in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string.
    
    Parameters:
    text (str): A string containing the dates in various formats.

    Returns:
    List[str]: A list of valid dates in the formats specified.
    """
    """This function takes a string as input and returns a list of valid dates in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string."""
    # Regular expression pattern to match the dates
    pattern = r'\b(?:\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{4}\.\d{2}\.\d{2})\b'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    return matches

text = input('enter the string:')
print("Valid dates found:")
print(find_all_dates(text))

    
#Question6:-
import polyline
import pandas as pd

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
    polyline_str (str): The encoded polyline string.
    
    Returns:
    pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """
    # Decode the polyline string into a list of coordinates
    coords = polyline.decode(polyline_str)
    
    # Initialize lists to store latitude, longitude, and distance
    latitudes = []
    longitudes = []
    distances = [0]  # First distance is 0
    
    # Iterate over the coordinates
    for i in range(len(coords)):
        latitudes.append(coords[i][0])
        longitudes.append(coords[i][1])
        
        # Calculate distance using Haversine formula for points in successive rows
        if i > 0:
            lat1, lon1 = coords[i-1]
            lat2, lon2 = coords[i]
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = (sin(dlat/2))**2 + cos(lat1)*cos(lat2)*(sin(dlon/2))**2
            c = 2*asin(sqrt(a))
            distance = 6371 * c  # Radius of earth in kilometers
            distances.append(distance * 1000)  # Convert to meters
    
    # Create a DataFrame
    df = pd.DataFrame({
        'latitude': latitudes,
        'longitude': longitudes,
        'distance': distances
    })
    
    return df
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """



#Question7:-
def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then multiply each element 
    by the sum of its original row and column index before rotation.
    
    Args:
    - matrix (List[List[int]]): 2D list representing the matrix to be transformed.
    
    Returns:
    - List[List[int]]: A new 2D list representing the transformed matrix.
    """
    n = len(matrix)
    rotated_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Rotate the matrix by 90 degrees clockwise
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n-i-1] = matrix[i][j]
    
    # Print the rotated matrix
    print("Rotated Matrix:")
    print(rotated_matrix)
    
    # Replace each element with the sum of all elements in the same row and column, excluding itself
    transformed_matrix = [[sum(rotated_matrix[i]) + sum([row[j] for row in rotated_matrix]) - rotated_matrix[i][j] for j in range(n)] for i in range(n)]
    
    # Print the transformed matrix
    print("Transformed Matrix:")
    print(transformed_matrix)
    
    return transformed_matrix

# User input
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Function call
result = rotate_and_multiply_matrix(matrix)
    
    return []


#Question8:-
def time_check(df):
    print("Input DataFrame:")
    print(df)
    
    df['startTime'] = pd.to_datetime(df['startTime'], errors='coerce')
    df['endTime'] = pd.to_datetime(df['endTime'], errors='coerce')
    
    # Create 'startHour' and 'startDay' columns
    df['startHour'] = df['startTime'].dt.hour
    df['startDay'] = df['startTime'].dt.dayofweek
    
    print("\nDataFrame with converted datetime columns:")
    print(df)
    
    incorrect_timestamps = df.groupby(['id', 'id_2']).apply(lambda x: 
        not (set(range(24)) == set(x['startHour']) and 
             set(range(7)) == set(x['startDay'])))
    
    print("\nIncorrect timestamps:")
    print(incorrect_timestamps)
    
    return incorrect_timestamps

# Call the function with your DataFrame as input
time_check(df)
