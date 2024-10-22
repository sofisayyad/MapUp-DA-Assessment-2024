import pandas as pd
#loading the dataset
df = pd.read_csv('dataset-2.csv')

#Question9 :-
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = pd.DataFrame(index=df['id_start'], columns=df['id_start'])
    for i in range(len(df)):
        for j in range(len(df)):
            if i == j:
                distance_matrix.iloc[i, j] = 0
            else:
                distance_matrix.iloc[i, j] = df['distance'][i] + df['distance'][j]
    distance_matrix = distance_matrix + distance_matrix.T
    return distance_matrix

distance_matrix = calculate_distance_matrix(df)
print(distance_matrix)

return df

#Question10:-
def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    rows = []
    for i in df.index:
        for j in df.columns:
            if i != j:
                rows.append([i, j, df.loc[i, j]])
    result_df = pd.DataFrame(rows, columns=['id_start', 'id_end', 'distance'])
    result_df = result_df[result_df['id_start'] == 1001400].sort_values('id_end')
    return result_df

unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df.to_string(index=False))


#Question11:-
def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Convert 'distance' column to numeric values
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    
    # Calculate average distance for the reference value
    average_distance = df[df['id_start'] == reference_id]['distance'].mean()
    
    # Calculate the threshold values (10% of the average distance)
    lower_threshold = average_distance * 0.9
    upper_threshold = average_distance * 1.1
    
    # Filter the DataFrame to include only rows within the threshold
    filtered_df = df[(df['id_start'] != reference_id) & (df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]
    
    # Sort the filtered DataFrame by 'id_start' and return the sorted list
    return sorted(filtered_df['id_start'].unique().tolist())

# Test the function
df = unroll_distance_matrix(distance_matrix)
print(find_ids_within_ten_percentage_threshold(df, 1001400))


#Question12:-
def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
     # Define the rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    # Calculate the toll rates for each vehicle type
    for vehicle, coefficient in rate_coefficients.items():
        df[vehicle] = df['distance'] * coefficient
    
    return df

# Test the function

df = unroll_distance_matrix(distance_matrix)
df = calculate_toll_rate(df)
print(df)



#Question13:-
import datetime
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    
    # Define the discount factors for each time interval
    discount_factors = {
        'weekdays_00_10': 0.8,
        'weekdays_10_18': 1.2,
        'weekdays_18_24': 0.8,
        'weekends': 0.7
    }
    
    # Define the time ranges
    time_ranges = {
        '00_10': (pd.Timestamp('00:00:00').time(), pd.Timestamp('10:00:00').time()),
        '10_18': (pd.Timestamp('10:00:00').time(), pd.Timestamp('18:00:00').time()),
        '18_24': (pd.Timestamp('18:00:00').time(), pd.Timestamp('23:59:59').time())
    }
    
    # Create a new DataFrame to store the results
    result_df = pd.DataFrame()
    
    # Loop through each unique (id_start, id_end) pair
    for (id_start, id_end), group_df in df.groupby(['id_start', 'id_end']):
        # Create a new DataFrame for this pair
        pair_df = pd.DataFrame()
        
        # Loop through each day of the week
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            # Set the start_day and end_day columns
            pair_df['start_day'] = day
            pair_df['end_day'] = day
            
            # Loop through each time range
            for time_range, (start_time, end_time) in time_ranges.items():
                # Set the start_time and end_time columns
                pair_df['start_time'] = start_time
                pair_df['end_time'] = end_time
                
                # Apply the discount factors
                if day in ['Saturday', 'Sunday']:
                    discount_factor = discount_factors['weekends']
                else:
                    discount_factor = discount_factors[f'weekdays_{time_range}']
                
                pair_df['moto'] = group_df['moto'] * discount_factor
                pair_df['car'] = group_df['car'] * discount_factor
                pair_df['rv'] = group_df['rv'] * discount_factor
                pair_df['bus'] = group_df['bus'] * discount_factor
                pair_df['truck'] = group_df['truck'] * discount_factor
                
                # Append the pair_df to the result_df
                result_df = pd.concat([result_df, pair_df], ignore_index=True)
    
    return result_df
