import pandas as pd
import argparse, time, json
from CommentData import CommentData
from AuthorData import AuthorData
from GildData import GildData
from ThreadData import ThreadData
from datetime import timedelta
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import StratifiedShuffleSplit
from pathlib import Path


class preprocess:

    def __init__(self, args):
        self.initializeDataObjects()
        self.loadpath = "../../data/raw/"
        self.savepath = args.savepath
        if args.loadpath != "../../data/raw/":
            self.loadpath = args.loadpath
            self.setDifferentLoadpath()
        self.loadData()
        self.convertToPandas()
        self.MergedData = None

    def initializeDataObjects(self):
        self.threaddata = ThreadData()
        self.commentdata = CommentData()
        self.gilddata = GildData()
        self.authordata = AuthorData()
        
    def setDifferentLoadpath(self):
        self.threaddata.setpath(self.loadpath)
        self.commentdata.setpath(self.loadpath)
        self.gilddata.setpath(self.loadpath)
        self.authordata.setpath(self.loadpath)

    def loadData(self):
        self.threaddata.loadData()
        self.commentdata.loadData()
        self.gilddata.loadData()
        self.authordata.loadData()
    
    def convertToPandas(self):
        self.threaddata = pd.DataFrame(self.threaddata.getData())
        self.commentdata = pd.DataFrame(self.commentdata.getData())
        self.gilddata = pd.DataFrame(self.gilddata.getData())
        self.authordata = pd.DataFrame(self.authordata.getData())

    def dropDuplicatesAndEmptyRows(self, data, key_columns):
        df = data.copy()
        df.drop_duplicates(subset=key_columns, keep='last', inplace=True, ignore_index=True)
        return df.dropna()

    def toDays(self, x, currentime):
        '''Takes in created_utc time (Unix time, in seconds) and current time. Calculates
        age and returns the number of days'''
        d = timedelta(seconds=currentime-x)
        return d.days

    def convertDatesToDays(self, data, new_column):
        '''Convert the created_utc time to datetime, fetch the days and place it
        in a new column. Also removes the original created_utc column'''
        df = data.copy()
        now = time.time() #This will differ everytime, but the change will be constant across all the rows.
        df[new_column] = df.created_utc.map(lambda x: self.toDays(x, now))
        return df.drop(["created_utc"], axis=1)

    def process(self):
        self.authordata = self.dropDuplicatesAndEmptyRows(self.authordata, ['author_ids'])
        self.commentdata = self.dropDuplicatesAndEmptyRows(self.commentdata, ['comment_ids'])
        self.gilddata = self.dropDuplicatesAndEmptyRows(self.gilddata, ['comment_ids'])
        self.threaddata = self.dropDuplicatesAndEmptyRows(self.threaddata, ['thread_ids'])
        authors = self.convertDatesToDays(self.authordata, "acc_age_days")
        comments = self.convertDatesToDays(self.commentdata, "comment_age_days")
        commentsAndGilds = self.gilddata.merge(comments, how='outer', on='comment_ids')
        self.MergedData = commentsAndGilds.merge(authors, how='inner', on='author_ids')
        transformGilds = gildsToBinary()
        self.MergedData, self.targets = transformGilds.transform(self.MergedData)

    def splitAndSave(self):
        splits = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_index, test_index in splits.split(self.MergedData, self.targets):
            pass
        train_data = self.MergedData.iloc[train_index, :]
        test_data = self.MergedData.iloc[test_index, :]
        train_data.reset_index(drop=True, inplace=True)
        test_data.reset_index(drop=True, inplace=True)
        self.savetoJson(train_data, "train_data_baseline")
        self.savetoJson(test_data, "test_data_baseline")

    def savetoJson(self, df, filename):
        Path(self.savepath).mkdir(parents=True, exist_ok=True)
        filename = f"{self.savepath}{filename}.json"
        df.to_json(filename, orient="columns")
        
class gildsToBinary(BaseEstimator, TransformerMixin):
    '''Using Sklearn's base transformer class to process the gildings column (convert the dictionary into binary)'''
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        df = X.copy()
        df["gildings"].fillna(0, inplace=True)
        df["gildings"] = df["gildings"].apply(lambda x: 1 if x != 0 else 0)
        return df, df["gildings"]

def build_parser():
    loadpath = "../../data/raw/"
    savepath = "../../data/processed/"
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loadpath",
                        help="Load folder for raw files", type=str, default=loadpath)
    parser.add_argument("-s", "--savepath",
                        help="Save folder for processed files", type=str, default=savepath)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    Preprocess = preprocess(args)
    Preprocess.process()
    Preprocess.splitAndSave()

if __name__ == "__main__":
    main()