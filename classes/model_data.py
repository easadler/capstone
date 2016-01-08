import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import RandomForestRegressor as RFR

class CreateModel(object):
    """docstring for CreateModel"""
    def __init__(self, test=['all', 'season', 9], k_folds=False, model=RFC()):


    def fit_transform(df, y='count'):
        if self.add_feats:
            engineer_feats(df)




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

class EngineerFeats(object):
    """docstring for CreateModel"""
    def __init__(self, test=['all', 'season', 9]):
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
