import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def maximum(df):
    return df['quantity'].max()

def minimum(df):
    return df['quantity'].min()

def count_relative_minima(df, n=5):
    # n : number of points to be checked before and after  
    return argrelextrema(df.quantity.values, np.less_equal, order=n)[0].shape[0]

def count_relative_maxima(df, n=5):
    # n : number of points to be checked before and after    
    return argrelextrema(df.quantity.values, np.greater_equal, order=n)[0].shape[0]
    

def calc_slopes(data_frame, column_names):
        time_field, reading_field = column_names
        # Convert required column data to numpy array before slope calculation
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