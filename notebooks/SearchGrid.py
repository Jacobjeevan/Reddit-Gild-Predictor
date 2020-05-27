#! usr/bin/env python3
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from utils import getScoring

class SearchGrid:
    
    def __init__(self, DataStore):
        self.GridParameters = None
        self.Classifier = None
        self.getData = DataStore
        self.reset()
        
    def calculateScore(self, gridresults):
        f1 = self.calculateF1(gridresults, 0)
        roc_auc = gridresults['mean_test_roc_auc'][0]
        self.appendToScores(f1, roc_auc)
        self.bestindex = 0
        self.bestF1 = f1
        self.bestROC =roc_auc
    
    def calculateScores(self, gridresults):
        for i in range(len(gridresults['params'])):
            f1 = self.calculateF1(gridresults, i)
            roc_auc = gridresults['mean_test_roc_auc'][i]
            self.appendToScores(f1, roc_auc)
            if f1 > self.bestF1:
                self.bestindex = i
                self.bestF1 = f1
                self.bestROC =roc_auc
                
    def getBestScores(self):
        return self.bestF1, self.bestROC
    
    def getBestindex(self, gridresults):
        numberOfParameters = len(gridresults['params'])
        if (numberOfParameters == 1):
            self.calculateScore(gridresults)
        else:
            self.calculateScores(gridresults)
        return self.bestindex
    
    def appendToScores(self, f1, roc_auc):
        self.f_scores.append(f1)
        self.roc_scores.append(roc_auc)
    
    def getAllScores(self):
        return self.f_scores, self.roc_scores
    
    def getBestParameters(self):
        return self.bestparameters
    
    def reset(self):
        self.f_scores = []
        self.roc_scores = []
        self.bestindex = -1
        self.bestF1 = -1
        self.bestROC = -1
        self.bestparameters = {}
    
    def setGridParameters(self, parameters):
        self.GridParameters = parameters
        
    def getGridParameters(self):
        return self.GridParameters
    
    def setClassifier(self, Classifier):
        self.Classifier = Classifier
        
    def getClassifier(self):
        return self.Classifier
    
    def saveModel(self):
        # TO DO
        pass

    def getVariableNames(self, variable, num_splits):
        '''Returns list of variable names for k splits; i.e. split0_test_falseNegatives
        split1_test_falseNegatives etc.'''
        return ['split' + str(i) + f'_test_{variable}' for i in range(num_splits)]

    def calculateTotal(self, gridresults, variable, index):
        variableNamesList = self.getVariableNames(variable, 20)
        total = 0
        for i in variableNamesList:
            total+= gridresults[i][index]
        return total

    def calculateF1(self, gridresults, index):
        truePositives = self.calculateTotal(gridresults, "truePositives", index)
        falsePositives = self.calculateTotal(gridresults, "falsePositives", index)
        falseNegatives = self.calculateTotal(gridresults, "falseNegatives", index)
        f1 = (2*truePositives)/(2*truePositives+falsePositives+falseNegatives)
        return f1

    def trainGrid(self):
        rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=2, random_state=42)
        grid = GridSearchCV(self.getClassifier(), self.getGridParameters(), scoring=getScoring(), cv=rskf, 
                            refit=self.getBestindex)
        grid.fit(self.getData.getxTrain(), self.getData.getyTrain())
        self.getBestindex(grid.cv_results_)
        self.bestparameters = grid.best_params_
        return grid