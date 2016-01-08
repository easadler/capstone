import numpy as np
import pandas as pd


def remove_trip_outliers(df, duration=[0, 60], same=False):
    # subset by min/max duration

    #remove trips with same origin and destination
    pass


def subset_trips(df, hours=[1, 7, 10, 4, 6], stations=['Seattle', 'WF'], rider_type=['Annual', 'Temporary']):
    # bin hours

    # choose stations

    # choose riders to include
    pass


def combine(df_t, df_w):
    # groupby to get supply & demand

    # create index from weather datetime

    # merge weather with supply & demand seperately

    # return supply and demand datasets
    pass


def split_data(df, how=False, split=0.25):
    if how:
        # get start month & traing & test size
        pass
        # return train_x, train_y, test_x, test_y
    else:
        # use train test split 
        pass
        # return train_x, train_y, test_x, test_y
