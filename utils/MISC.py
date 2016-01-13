import pandas as pd

df_d = None

# code for dummies
jd = pd.get_dummies(df_d['cluster'])
df_d = pd.concat([df_d, jd], axis=1)
df_d.drop(['cluster', 0], inplace=True, axis=1)

#old feat engineer functions
'''
def fit(self, df):
    df = df.copy()

    # Get dow & month features
    df['dow'] = map(lambda x: x.dayofweek, df['date'])
    df['month'] = map(lambda x: x.month, df['date'])

    # Get dictionaries of average values
    hour_average = df.groupby(['hour', 'terminal'])['count'].mean().reset_index()
    hour_average.columns = ['hour', 'terminal', 'hour_avg']

    month_average = df.groupby(['month', 'terminal'])['count'].mean().reset_index()
    month_average.columns = ['month', 'terminal', 'month_avg']

    dow_average = df.groupby(['dow', 'terminal'])['count'].mean().reset_index()
    dow_average.columns = ['dow', 'terminal', 'dow_avg']

    df = df[['hour', 'dow', 'month', 'terminal']].drop_duplicates()
    df = df.merge(hour_average, on=['hour', 'terminal']).merge(month_average, on=['month', 'terminal']).merge(dow_average, on=['dow', 'terminal'])
    self.df = df

    return self

def transform(self, df, adjust_month=True):
    df = df.copy()

    df['dow'] = map(lambda x: x.dayofweek, df['date'])
    df['month'] = map(lambda x: x.month, df['date'])

    if adjust_month:
        df.ix[df['month'] > max(self.df['month']), 'month'] = max(self.df['month'])
    df = df.merge(self.df, on=['hour', 'dow', 'month', 'terminal'])

    df.drop(['month', 'dow'], axis=1, inplace=True)

    return df
'''