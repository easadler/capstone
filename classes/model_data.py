import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import RandomForestRegressor as RFR


class CreateModel(object):
    """docstring for CreateModel"""
    def __init__(self, k_folds=False, model=RFC()):
        pass

    def fit(X, y):
        # fit the model with given data
        pass

    def predict(X, y):
        pass

    def score(X, y):
        pass



'''
1. get station averages for 
    * all data
    * 3/4 every season
    * 9 months

2. add features to data set


3. train/test RFC or RFR:
    * k-fold cv for all date
    * one model for season & 9 months

4. produce results
'''


def split_data(df, how=False, split=0.25):
    if how:
        # get start month & traing & test size
        pass
        # return train_x, train_y, test_x, test_y
    else:
        # use train test split
        pass
        # return train_x, train_y, test_x, test_y


class EngineerFeats(object):
    """docstring for CreateModel"""
    def __init__(self):
        self.feats = None

    def fit_transform(self, df):
        self.fit(df)
        self.feats = self.ha_dict, self.da_dict, self.ma_dict
        return self.feats

    def fit(self, df):
        # Get dow & month features
        df['dow'] = map(lambda x: x.dayofweek, df['date'])
        df['month'] = map(lambda x: x.month, df['date'])

        # Get dictionaries of average values
        hour_average = df.groupby(['hour', 'terminal'])['count'].mean().reset_index()
        hour_average.columns = ['hour', 'terminal', 'hour_avg']
        self.ha_dict = hour_average.pivot(index='hour', columns='terminal', values='hour_avg').to_dict()

        month_average = df.groupby(['month', 'terminal'])['count'].mean().reset_index()
        month_average.columns = ['month', 'terminal', 'month_avg']
        self.ma_dict = month_average.pivot(index='month', columns='terminal', values='month_avg').to_dict()

        dow_average = df.groupby(['dow', 'terminal'])['count'].mean().reset_index()
        dow_average.columns = ['dow', 'terminal', 'dow_avg']
        self.da_dict = dow_average.pivot(index='dow', columns='terminal', values='dow_avg').to_dict()

if __name__ == '__main__':
    df_d = pd.read_csv('../data/final/demand_all_features.csv', parse_dates=['date'], infer_datetime_format=True)
    ef = EngineerFeats()
    print ef.fit_transform(df_d)
