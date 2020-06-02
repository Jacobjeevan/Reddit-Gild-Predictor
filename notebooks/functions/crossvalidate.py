#! usr/bin/env python3
from sklearn.model_selection import cross_validate
from modelspace import ModelSpace
from utilities import getScoring
from cvmetrics import CVMetrics

class CrossValidate(ModelSpace):
    
    def __init__(self):
        super().__init__()
        self.metrics = None
    
    def run(self):
        scores = cross_validate(self.getClassifier(), self.getData.getxTrain(), self.getData.getyTrain(), scoring=getScoring(), 
                                cv=self.getCrossValidator())
        self.metrics = CVMetrics(scores)
        
    def getMetrics(self):
        return self.metrics