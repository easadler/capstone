import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.metrics import roc_auc_score


def clean(df):
    ef = EngineerFeats()
    df = ef.fit_transform(df)

    # get dummies for time
    jd = pd.get_dummies(df['hour'])
    df = pd.concat([df, jd], axis=1)
    df.drop(['Early', 'hour'], inplace=True, axis=1)

    df = df.dropna()
    return df


def train_model(df, rf=RFC(), classification=True):
    if classification:
        df.ix[df['count'] > 0, 'count'] = 1

    # Split data
    train_x, test_x, train_y, test_y = train_test_split(df.drop(['terminal', 'ecosystem', 'count', 'date', 'cluster'], axis=1), df['count'], test_size=0.2)

    # Fit data
    rf.fit(train_x, train_y)

    # get area under the curve
    if classification:
        score = roc_auc_score(test_y, rf.predict_proba(test_x)[:, 1])
    else:
        score = rf.score(test_x, test_y)

    return score, rf


def cv_model(df, rf=RFC(), cv=5, classification=True):
    if classification:
        df.ix[df['count'] > 0, 'count'] = 1

    return cross_val_score(rf, df.drop(['terminal', 'ecosystem', 'count', 'date', 'cluster'], axis=1), df['count'], scoring='roc_auc', cv=cv)


class EngineerFeats(object):
    """docstring for CreateModel"""
    def __init__(self):
        self.df = None

    def fit_transform(self, df):
        df = df.copy()
        self.fit(df)

        return self.transform(df)

    def fit(self, df):
        df = df.copy()

        # Get dow & month features
        df['dow'] = map(lambda x: x.dayofweek, df['date'])
        df['month'] = map(lambda x: x.month, df['date'])

        # Get dictionaries of average values
        hour_average = df.groupby(['terminal', 'month', 'hour'])['count'].mean().reset_index()
        hour_average.columns = ['terminal', 'month', 'hour', 'hour_avg_lagged']
        hour_average['month'] = hour_average['month'] + 1

        month_average = df.groupby(['month', 'terminal'])['count'].mean().reset_index()
        month_average.columns = ['month', 'terminal', 'month_avg_lagged']
        month_average['month'] = month_average['month'] + 1

        dow_average = df.groupby(['terminal', 'month', 'dow'])['count'].mean().reset_index()
        dow_average.columns = ['terminal', 'month', 'dow', 'dow_avg']
        dow_average['month'] = dow_average['month'] + 1

        df = df[['hour', 'dow', 'month', 'terminal']].drop_duplicates()
        df = df.merge(hour_average, on=['hour', 'month', 'terminal']).merge(month_average, on=['month', 'terminal']).merge(dow_average, on=['dow', 'month', 'terminal'])
        self.df = df

        return self

    def transform(self, df):
        df = df.copy()

        df['dow'] = map(lambda x: x.dayofweek, df['date'])
        df['month'] = map(lambda x: x.month, df['date'])

        df = df.merge(self.df, on=['hour', 'dow', 'month', 'terminal'])

        df.drop(['month', 'dow'], axis=1, inplace=True)

        return df


if __name__ == '__main__':
    df_d = pd.read_csv('../data/final/demand_all_features.csv', parse_dates=['date'], infer_datetime_format=True)
    ef = EngineerFeats()
    print ef.fit_transform(df_d)



# def fit(self, df):
#     # Get dow & month features
#     df['dow'] = map(lambda x: x.dayofweek, df['date'])
#     df['month'] = map(lambda x: x.month, df['date'])

#     # Get dictionaries of average values
#     hour_average = df.groupby(['hour', 'terminal'])['count'].mean().reset_index()
#     hour_average.columns = ['hour', 'terminal', 'hour_avg']
#     self.ha_dict = hour_average.pivot(index='hour', columns='terminal', values='hour_avg').to_dict()

#     month_average = df.groupby(['month', 'terminal'])['count'].mean().reset_index()
#     month_average.columns = ['month', 'terminal', 'month_avg']
#     self.ma_dict = month_average.pivot(index='month', columns='terminal', values='month_avg').to_dict()

#     dow_average = df.groupby(['dow', 'terminal'])['count'].mean().reset_index()
#     dow_average.columns = ['dow', 'terminal', 'dow_avg']
#     self.da_dict = dow_average.pivot(index='dow', columns='terminal', values='dow_avg').to_dict()

