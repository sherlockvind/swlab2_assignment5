import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

def maximum(df, field):
    # Calculate maximum of input data frame 'df' for the given 'field'
    return df[field].max()

def minimum(df, field):
    # Calculate minimum of input data frame 'df' for the given 'field'
    return df[field].min()

def count_relative_minima(df, options):
    field, n = options
    # n : number of points to be checked before and after
    # field : field of the data on which this method has to be applied upon
    return argrelextrema(df[field].to_numpy(), np.less_equal, order=n)[0].shape[0]

def count_relative_maxima(df, options):
    field, n = options
    # n : number of points to be checked before and after
    # field : field of the data on which this method has to be applied upon
    return argrelextrema(df[field].to_numpy(), np.greater_equal, order=n)[0].shape[0]

def calc_slopes(data_frame, column_names):
    time_field, reading_field = column_names
    t1 = data_frame[time_field].to_numpy()[0:-1]
    t2 = data_frame[time_field].to_numpy()[1:]
    avg_time_period = (t2-t1).mean()
    #print(t1, t2)
    #print(avg_time_period)

    r1 = data_frame[reading_field].to_numpy()[0:-1]
    r2 = data_frame[reading_field].to_numpy()[1:]
    reading_difference = r2-r1
    #print(reading_difference)

    negative_difference = reading_difference[reading_difference < 0]
    positive_difference = reading_difference[reading_difference > 0]

    avg_negative_diff = 0
    avg_positive_diff = 0

    if negative_difference.size > 0:
        avg_negative_diff = negative_difference.mean()

    if positive_difference.size > 0:
        avg_positive_diff = positive_difference.mean()

    avg_downward_slope = avg_negative_diff / avg_time_period
    avg_upward_slope = avg_positive_diff / avg_time_period

    return (avg_downward_slope, avg_upward_slope)

def summarise(df, options):
    time_field, reading_field, sensor_field, neighbourhood_size = options

    max_val = maximum(df, reading_field)
    min_val = minimum(df, reading_field)
    rel_max_count = count_relative_maxima(df, (reading_field, neighbourhood_size))
    rel_min_count = count_relative_minima(df, (reading_field, neighbourhood_size))
    (avg_dec_slope, avg_inc_slope) = calc_slopes(df, (time_field, reading_field))

    summarised_dict = {"maximum": max_val, "minimum": min_val, "maxima_count": rel_max_count, "minima_count": rel_min_count, "avg_inc_slope": avg_inc_slope, "avg_dec_slope": avg_dec_slope, "sensor": df[sensor_field].unique()[0]}

    return summarised_dict

def leak_detection_off(df, time_field, reading_field, threshold=5):
    t = df[time_field].to_numpy()
    r = df[reading_field].to_numpy()
    start_idx = None
    data = []
    
    for i in range(1, t.shape[0]):
        diff = r[i] - r[i-1]
        if diff < 0 and diff > -1*threshold:
            #a new leak entry
            if start_idx is None:
                start_idx = i - 1                                          
        else:
            if start_idx:
                leak_dict = {'start_time':t[start_idx], 'end_time':t[i-1], 
                             'duration':t[i-1] - t[start_idx], 
                             'quantity':r[start_idx] - r[i-1]}
                data.append(leak_dict)
                start_idx = None
                
        #handling last entry
        if i == t.shape[0] - 1 and start_idx:
            leak_dict = {'start_time':t[start_idx], 'end_time':t[i], 
                         'duration':t[i] - t[start_idx], 
                         'quantity':r[start_idx] - r[i]}
            data.append(leak_dict)
            start_idx = None
                
    return data
            
def theft_detection_off(df, time_field, reading_field, threshold=5):
    t = df[time_field].to_numpy()
    r = df[reading_field].to_numpy()
    start_idx = None
    data = []
    
    for i in range(1, t.shape[0]):
        diff = r[i] - r[i-1]
        if diff <= -1 * threshold:
            #a new theft entry
            if start_idx is None:
                start_idx = i - 1                                          
        else:
            if start_idx:
                theft_dict = {'start_time':t[start_idx], 'end_time':t[i-1], 
                             'duration':t[i-1] - t[start_idx], 
                             'quantity':r[start_idx] - r[i-1]}
                data.append(theft_dict)
                start_idx = None
                
        #handling last entry
        if i == t.shape[0] - 1 and start_idx:
            theft_dict = {'start_time':t[start_idx], 'end_time':t[i], 
                         'duration':t[i] - t[start_idx], 
                         'quantity':r[start_idx] - r[i]}
            data.append(theft_dict)
            start_idx = None
    
    return data