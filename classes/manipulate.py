import numpy as np
import pandas as pd


def remove_trip_outliers(df, duration=[3, 60], different_stations=True):
    # subset by min/max duration
    df = df.ix[(df['tripduration'] >= duration[0]) & (df['tripduration'] <= duration[1]), :]

    #remove trips with same origin and destination
    if different_stations:
        df = df.ix[df['from_station_id'] != df['to_station_id'], :]
    return df


def subset_trips(df, hours=[0, 6, 10, 15, 19, 23], eco_list=['Seattle'], usertypes=['Annual Member', 'Short-Term Pass Holder'], cols_to_drop=['gender', 'birthyear']):
    eco_dict = {'Seattle': 0, 'Udist': 1, 'Outliers': -1}
    eco_list = [eco_dict[x] for x in eco_list]

    # bin hours
    if hours:
        df['hour'] = pd.cut(df['hour'], hours, include_lowest=True, right=True, labels=['Early', 'Commute_to_work', 'Afternoon', 'Commute_from_work', 'Night'])

    # choose stations
    df = df.ix[(df['ecosystem_to'].isin(eco_list)) & (df['ecosystem_from'].isin(eco_list)), :]

    # choose riders to include
    df = df.ix[df['usertype'].isin(usertypes), :]

    # drop uncessery columns
    df.drop(cols_to_drop, axis=1, inplace=True)

    return df


def subset_weather(df, hours=[0, 6, 10, 15, 19, 23], cols_to_drop=['DIR']):
    # bin hours
    if hours:
        df['hour'] = pd.cut(df['hour'], hours, include_lowest=True, right=True, labels=['Early', 'Commute_to_work', 'Afternoon', 'Commute_from_work', 'Night'])

    df.drop(cols_to_drop, axis=1, inplace=True)

    return df


def combine(df_t, df_w):
    # groupby to get supply & demand
    df_d = df_t.groupby(['from_station_id','datetime'])['count'].sum().reset_index()
    df_s = df_t.groupby(['to_station_id','datetime'])['count'].sum().reset_index()

    # create index from weather datetime
    datetimes = df_w['datetime']
    terminals = df_t['from_station_id'].unique()
    full_index = pd.MultiIndex.from_product([datetimes, terminals], names=['datetime', 'terminal'])

    # Create dataframes holding meta information {md: meta demand, ms: supply}
    df_md= df_t[['dockcount', 'from_station_id','elevation', 'cluster_from', 'ecosystem_from']]
    df_md.rename(columns={'from_station_id': 'terminal', 'cluster_from': 'cluster', 'ecosystem_from': 'ecosystem'},inplace=True)
    df_ms = df_t[['dockcount', 'from_station_id','elevation', 'cluster_to', 'ecosystem_to']]
    df_ms.rename(columns={'from_station_id': 'terminal', 'cluster_to': 'cluster', 'ecosystem_to': 'ecosystem'}, inplace=True)

    #Merge weather to index for base dataframe 
    df = pd.DataFrame(index=full_index).reset_index()
    df = df.merge(df_w, on='datetime')

    
    # return supply and demand datasets
    pass


if __name__ == '__main__':
    df_t = pd.read_csv('../data/cleaned/cleaned_trips.csv')
    df_t = subset_trips(remove_trip_outliers(df_t))
    df_t.to_csv('../data/cleaned/cleaned_trips.csv', index=False)
    # df_w = pd.read_csv('../data/cleaned/cleaned_weather.csv')
    # df_w = subset_weather(df_w)
    # df_w.to_csv('../data/cleaned/cleaned_weather.csv', index=False)
