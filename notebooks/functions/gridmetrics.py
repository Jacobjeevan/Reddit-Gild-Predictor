from metrics import Metrics

class GridMetrics(Metrics):
    
    NUM_SPLITS = 20 #Number of splits in Crossvalidation
    
    def __init__(self, gridresults, NUM_SPLITS=None):
        if NUM_SPLITS:
            GridMetrics.NUM_SPLITS = NUM_SPLITS
        self.gridresults = gridresults
        self.parameters = self.gridresults['params']
        self.scores = []
        self.bestindex = -1
        self.calculateBestindex()
    
    def calculateBestindex(self):
        numberOfParameters = len(self.gridresults['params'])
        if (numberOfParameters == 1):
            self.calculateScore()
        else:
            self.calculateScores()
    
    def calculateScore(self):
        f1 = self.calculateF1(0)
        roc_auc = self.gridresults['mean_test_roc_auc'][0]
        self.appendToScores(f1, roc_auc)
        self.bestindex = 0

    def calculateScores(self):
        bestf1 = -1
        for i in range(len(self.parameters)):
            f1 = self.calculateF1(i)
            roc_auc = self.gridresults['mean_test_roc_auc'][i]
            self.appendToScores(f1, roc_auc)
            if f1 > bestf1:
                self.bestindex = i
                bestf1 = f1
                
    def calculateF1(self, index):
        truePositives = self.calculateTotal("truePositives", index)
        falsePositives = self.calculateTotal("falsePositives", index)
        falseNegatives = self.calculateTotal("falseNegatives", index)
        confusionMatrixArray = [truePositives, falsePositives, falseNegatives]
        f1 = super().calculateF1(confusionMatrixArray)
        return f1

    def calculateTotal(self, variable, index):
        variableNamesList = self.getVariableNames(variable, GridMetrics.NUM_SPLITS)
        total = 0
        for i in variableNamesList:
            total+= self.gridresults[i][index]
        return total
    
    def getVariableNames(self, variable, num_splits):
        '''Returns list of variable names for k splits; i.e. split0_test_falseNegatives
        split1_test_falseNegatives etc.'''
        return ['split' + str(i) + f'_test_{variable}' for i in range(num_splits)]
    
    def appendToScores(self, f1, roc_auc):
        self.scores.append((f1, roc_auc))
    
    def getAllresults(self):
        return self.parameters, self.scores
    
    def getBestResults(self):
        return self.parameters[self.bestindex], self.scores[self.bestindex]
    
    def getBestindex(self):
        return self.bestindex