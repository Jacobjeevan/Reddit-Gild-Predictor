#! usr/bin/env python3
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.base import BaseEstimator, TransformerMixin

def getTruePositives(y_true, y_pred): 
    return confusion_matrix(y_true, y_pred)[1, 1]

def getFalsePositives(y_true, y_pred): 
    return confusion_matrix(y_true, y_pred)[0, 1]

def getFalseNegatives(y_true, y_pred): 
    return confusion_matrix(y_true, y_pred)[1, 0]

scoring = {'truePositives': make_scorer(getTruePositives), 'falsePositives': make_scorer(getFalsePositives), 
       'falseNegatives': make_scorer(getFalseNegatives), 'roc_auc': make_scorer(roc_auc_score)}

def getScoring():
    return scoring

class filter_add_attributes(BaseEstimator, TransformerMixin):
    '''Custom transformer based on Sklearn's classes.
    Takes in dataframe (train or test) and adds new features and returns
    a filtered version of the original train/test datasets.'''
    def fit(self, X, y=None):
        return self.fit_transform(X)
    def transform(self, X, y=None):
        return self.fit_transform(X)
    def fit_transform(self, X, y=None):
        '''Calculates and adds comment body length and account activity (based on frequency of comment author)
        as features. Returns a new dataframe with the added columns.'''
        data = X.copy()
        data["edited_comment"] = data.edited_comment.astype(bool)
        data["comment_length"] = data.comment_body.apply(lambda x: len(x))
        data["account_activity"] = data.author_ids.map(data.author_ids.value_counts())
        data["is_premium"] = data.is_premium.astype(int)
        items = ["comment_upvotes", "comment_karma", "link_karma", "is_premium", "comment_age", "edited_comment"]
        return data.filter(items=items, axis=1)