import numpy as np
import pandas as pd


def round_to_hour(x):
    if x.minute > 30:
        x = x.replace(minute=0)
        x = x + pd.offsets.Hour(1)
    else:
        x = x.replace(minute=0)
    return x


def transform_weather(df):
    # Replace missing values as to NA.
    df = df.replace('\*+', np.nan, regex=True)

    # Replace trace amounts with small number
    df = df.replace('T', 0.001, regex=True)

    # Round to nearest hour
    rounded_time = map(round_to_hour, pd.to_datetime(df['YR--MODAHRMN'], format='%Y%m%d%H%M'))

    # Subset relevent columns and convert to float
    df = df[['TEMP', 'SPD', 'PCP01', 'CLG', 'DIR', 'VSB', 'DEWP', 'SLP', 'STP']].astype(float)

    # Add datetime column
    df['datetime'] = rounded_time

    # Group by to remove duplicates
    df = df.groupby(['datetime']).mean()

    return df


def transform_trips(df):
    # Drop unnecessary columns
    df = df.drop(['from_station_name', 'to_station_name', 'trip_id', 'stoptime', 'bikeid'], axis=1)

    # Convert columns and create hour column
    df['starttime'] = pd.to_datetime(df['starttime'])

    # Convert tripduration to minutes
    df['tripduration'] = df['tripduration'] / float(60)

    # Create hour column
    df['hour'] = df['starttime'].map(lambda x: x.hour)

    # rename starttime
    df = df.rename(columns={'starttime': 'datetime'})

    # Remove closed station and pronto shop
    df = df.ix[(~df['from_station_id'].isin(['Pronto shop', 'UW-01'])) & (~df['to_station_id'].isin(['Pronto shop', 'UW-01'])), :]

    return df


def add_cluster(df_t, df_c):
    df = df_t.merge(df_c[['dockcount', 'elevation', 'cluster', 'ecosystem', 'terminal']], left_on='from_station_id', right_on='terminal',  how='left')
    df.drop('terminal', axis=1, inplace=True)
    df = df.merge(df_c[['terminal', 'cluster', 'ecosystem']], left_on='to_station_id', right_on='terminal', suffixes=['_from', '_to'])
    df.drop('terminal', axis=1, inplace=True)

    return df

if __name__ == '__main__':
    # df_w = pd.read_table('../data/raw/hw.txt', sep=' ', error_bad_lines=False, index_col=False)
    # transform_weather(df_w).to_csv('../data/cleaned/cleaned_weather.csv', index=False)

    df_t = pd.read_csv('../data/raw/2015_trip_data.csv')
    df_c = pd.read_csv('../data/raw/clusters.csv')

    df_t = transform_trips(df_t)
    add_cluster(df_t, df_c).to_csv('../data/cleaned/cleaned_trips.csv', index=False)
