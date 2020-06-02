#! usr/bin/env python3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utilities import filter_add_attributes
from pathlib import Path
import os

class DataStore:
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "../../data/processed/")
    train_data = pd.read_csv(f"{filepath}/train_data_baseline.csv")
    test_data = pd.read_csv(f"{filepath}test_data_baseline.csv")
    
    def __init__(self):
        self.xTrain = None
        self.yTrain = None
        self.xTest = None
        self.yTest = None
        self.OriginalxTrain = None
        self.OriginalyTrain = None
        self.transformSet()
        
    def __call__(self):
        return self.getxTrain(), self.getyTrain(), self.getxTest(), self.getyTest()
 
    def createPipeline(self):
        pipeline = Pipeline([
            ('filter_add', filter_add_attributes()),
            ('scaler', StandardScaler()),
        ])
        return pipeline
    
    def setxTrain(self, x):
        self.xTrain = x
        
    def setyTrain(self, y):
        self.yTrain = y
        
    def revertToOriginal(self):
        self.xTrain = self.OriginalxTrain
        self.yTrain = self.OriginalyTrain
        
    def setOriginalxTrain(self, x):
        self.OriginalxTrain = x
        self.setxTrain(x)
        
    def setOriginalyTrain(self, y):
        self.OriginalyTrain = y
        self.setyTrain(y)
        
    def setxTest(self, x):
        self.xTest = x
        
    def setyTest(self, y):
        self.yTest = y
    
    def getxTrain(self):
        return self.xTrain
        
    def getyTrain(self):
        return self.yTrain
        
    def getxTest(self):
        return self.xTest
        
    def getyTest(self):
        return self.yTest
    
    def setAll(self, xTrain, yTrain, xTest, yTest):
        self.setOriginalxTrain(xTrain)
        self.setOriginalyTrain(yTrain)
        self.setxTest(xTest)
        self.setyTest(yTest)
        
    def transformSet(self):
        pipeline = self.createPipeline()
        xTrain = pipeline.fit_transform(DataStore.train_data)
        yTrain = DataStore.train_data["gildings"].to_list()
        xTest = pipeline.transform(DataStore.test_data)
        yTest = DataStore.test_data["gildings"].to_list()
        self.setAll(xTrain, yTrain, xTest, yTest)
        