import numpy as np
import pandas as pd


def remove_trip_outliers(df, duration=[3, 60], same=False):
    # subset by min/max duration
    df = df.ix[(df['tripduration'] >= duration[0]) & (df['tripduration'] <= duration[1]), :]

    #remove trips with same origin and destination
    if same:
        df = df.ix[df['from_station_id'] != df['to_station_id'], :]
    return df


def subset_trips(df, hours=[0, 6, 10, 15, 19], eco_list=['Seattle'], usertypes=['Annual Member', 'Short-Term Pass Holder']):
    eco_dict = {'Seattle': 0, 'Udist': 1, 'Outliers': -1}
    eco_list = [eco_dict[x] for x in eco_list]

    # bin hours
    df['hour'] = pd.cut(df['hour'], hours, include_lowest=True, right=True)

    # choose stations
    df = df.ix[(df['ecosystem_to'].isin(eco_list)) & (df['ecosystem_from'].isin(eco_list)), :]

    # choose riders to include
    df = df.ix[df['usertype'].isin(usertypes), :]

    return df


def combine(df_t, df_w):
    # groupby to get supply & demand

    # create index from weather datetime

    # merge weather with supply & demand seperately

    # return supply and demand datasets
    pass
