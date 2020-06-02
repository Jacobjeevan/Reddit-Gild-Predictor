#! usr/bin/env python3
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from utilities import getScoring
from gridmetrics import GridMetrics
from modelspace import ModelSpace

class SearchGrid(ModelSpace):
    
    def __init__(self):
        super().__init__()
        self.GridParameters = None
        
    def setGridParameters(self, parameters):
        self.GridParameters = parameters
        
    def getGridParameters(self):
        return self.GridParameters
    
    def run(self):
        self.grid = GridSearchCV(self.getClassifier(), self.getGridParameters(), scoring=getScoring(), cv=self.getCrossValidator(), 
                            refit=self.getBestindex)
        self.grid.fit(self.getData.getxTrain(), self.getData.getyTrain())
        return self.grid
    
    def getBestindex(self, gridresults):
        self.metrics = GridMetrics(gridresults)
        return self.metrics.getBestindex()
    
    def getMetrics(self):
        return self.metrics