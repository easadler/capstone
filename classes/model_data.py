import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import RandomForestRegressor as RFR

class CreateModel(object):
    """docstring for CreateModel"""
    def __init__(self, k_folds=False, model=RFC()):


    def fit(X,y):
        # fit the model with given data
        pass

    def predict(X,y):
        pass


    def score(X,y):
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
    def __init__(self, test='all'):
        self.feats

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)

    def fit(self, df):
        # goupby season, all, 9 get averages for count
        pass

    def transform(self, df):
        # merge with original df
        pass
