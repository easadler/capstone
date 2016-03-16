import numpy as np
import pandas as pd


def remove_trip_outliers(df, duration=[3, 60], different_stations=True):
    df = df.copy()
    # subset by min/max duration
    df = df.ix[(df['tripduration'] >= duration[0]) & (df['tripduration'] <= duration[1]), :]

    #remove trips with same origin and destination
    if different_stations:
        df = df.ix[df['from_station_id'] != df['to_station_id'], :]
    return df


def subset_trips(df, eco_list=['Seattle'], usertypes=['Annual Member', 'Short-Term Pass Holder'], cols_to_drop=['gender', 'birthyear']):
    df = df.copy()
    
    eco_dict = {'Seattle': 0, 'Udist': 1, 'Outliers': -1}
    eco_list = [eco_dict[x] for x in eco_list]

    # choose stations
    df = df.ix[(df['ecosystem_to'].isin(eco_list)) & (df['ecosystem_from'].isin(eco_list)), :]

    # choose riders to include
    df = df.ix[df['usertype'].isin(usertypes), :]

    # drop uncessery columns
    df.drop(cols_to_drop, axis=1, inplace=True)

    return df


def subset_weather(df, cols_to_drop=['DIR']):
    df = df.copy()

    df.drop(cols_to_drop, axis=1, inplace=True)

    return df


def groupby(df, index, column='to_station_id', hours=[0, 6, 10, 15, 19, 23]):
    df = df.copy()

    # Grouby to get counts by hour
    df = df.groupby([column, 'datetime'])['count'].sum().reset_index()
    df.rename(columns={column: 'terminal'}, inplace=True)

    # Create base dateframe using index and merge with df
    df_b = pd.DataFrame(index=index).reset_index()
    df = df_b.merge(df, on=['datetime', 'terminal'], how='left')

    # Set NAN's to 0
    df.ix[df['count'].isnull(), 'count'] = 0

    # Bin hours
    if hours:
        df['hour'] = df['datetime'].map(lambda x: x.hour)
        df['date'] = df['datetime'].map(lambda x: x.strftime('%d-%m-%Y'))
        df['hour'] = pd.cut(df['hour'], hours, include_lowest=True, right=True, labels=['Early', 'Commute_to_work', 'Afternoon', 'Commute_from_work', 'Night'])
        df['hour'] = df['hour'].astype('str')
        df = df.groupby(['date', 'terminal', 'hour'])['count'].sum()
        df = df.reset_index()

    return df


def groupby_weather(df, full_index, hours=[0, 6, 10, 15, 19, 23]):
    df = df.copy()

    # Create base dateframe using index and merge with df
    df_b = pd.DataFrame(index=full_index).reset_index()
    df = df_b.merge(df, on='datetime')

    # Bin hours
    if hours:
        df['hour'] = df['datetime'].map(lambda x: x.hour)
        df['date'] = df['datetime'].map(lambda x: x.strftime('%d-%m-%Y'))
        df['hour'] = pd.cut(df['hour'], hours, include_lowest=True, right=True, labels=['Early', 'Commute_to_work', 'Afternoon', 'Commute_from_work', 'Night'])
        df['hour'] = df['hour'].astype('str')
        df = df.groupby(['date', 'hour']).mean()
        df = df.reset_index()

    return df


def combine(df_t, df_w):
    df_t, df_w = df_t.copy(), df_w.copy()

    # create index from weather datetime
    datetimes = df_w['datetime']
    terminals = df_t['from_station_id'].unique()
    full_index = pd.MultiIndex.from_product([datetimes, terminals], names=['datetime', 'terminal'])

    # Get weather
    df_w = groupby_weather(df_w, full_index)

    # Get demand dataset
    df_d = groupby(df_t, full_index, column='from_station_id')

    # Get supply dataset
    df_s = groupby(df_t, full_index, column='to_station_id')

    # Create dataframes holding meta information {md: meta demand, ms: supply}
    df_md = df_t[['dockcount_from', 'from_station_id', 'elevation_from', 'cluster_from', 'ecosystem_from']].drop_duplicates()
    df_md.rename(columns={'from_station_id': 'terminal', 'elevation_from': 'elevation', 'cluster_from': 'cluster', 'ecosystem_from': 'ecosystem', 'dockcount_from': 'dockcount'}, inplace=True)
    df_ms = df_t[['dockcount_to', 'to_station_id', 'elevation_to', 'cluster_to', 'ecosystem_to']].drop_duplicates()
    df_ms.rename(columns={'to_station_id': 'terminal', 'elevation_to': 'elevation', 'cluster_to': 'cluster', 'ecosystem_to': 'ecosystem', 'dockcount_to': 'dockcount'}, inplace=True)

    # Merge all datasets together
    df_d = df_d.merge(df_w, on=['date', 'hour']).merge(df_md, on='terminal')
    df_s = df_s.merge(df_w, on=['date', 'hour']).merge(df_ms, on='terminal')

    return df_d, df_s


if __name__ == '__main__':
    # df_t = pd.read_csv('../data/cleaned/cleaned_trips.csv', parse_dates=['datetime'], infer_datetime_format=True)
    # df_t = subset_trips(remove_trip_outliers(df_t))
    # df_t.to_csv('../data/cleaned/cleaned_trips.csv', index=False)
    # df_w = pd.read_csv('../data/cleaned/cleaned_weather.csv', parse_dates=['datetime'], infer_datetime_format=True)
    # df_w = subset_weather(df_w)
    # df_w.to_csv('../data/cleaned/cleaned_weather.csv', index=False)

    df_w = pd.read_csv('../data/cleaned/cleaned_weather.csv', parse_dates=['datetime'], infer_datetime_format=True)

    df_t = pd.read_csv('../data/cleaned/cleaned_trips.csv', parse_dates=['datetime'], infer_datetime_format=True)

    df_t['count'] = 1

    df_d, df_s = combine(df_t, df_w)

    df_d.to_csv('../data/final/demand_all_features.csv', index=False)
    df_s.to_csv('../data/final/supply_all_features.csv', index=False)




