from metrics import Metrics
import numpy as np

class CVMetrics(Metrics):
    
    def __init__(self, cvresults):
        self.cvresults = cvresults
        self.scores = []
        
    def getScores(self):
        self.calculateF1()
        self.calculateROC()
        return self.scores

    def calculateF1(self):
        truePositives = self.calculateTotal('test_truePositives')
        falsePositives = self.calculateTotal('test_falsePositives')
        falseNegatives = self.calculateTotal('test_falseNegatives')
        confusionMatrixArray = [truePositives, falsePositives, falseNegatives]
        f1 = super().calculateF1(confusionMatrixArray)
        self.scores.append(f1)
        
    def calculateTotal(self, confusionMatrixVariable):
        scoresList = self.cvresults[confusionMatrixVariable]
        total = np.sum(scoresList)
        return total
    
    def calculateROC(self):
        roc = np.mean(self.cvresults['test_roc_auc'])
        self.scores.append(roc)