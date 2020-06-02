class Metrics:
    
    def calculateTotal(self):
        pass
    
    def calculateF1(self, confusionMatrixArray):
        truePositives = confusionMatrixArray[0]
        falsePositives = confusionMatrixArray[1]
        falseNegatives = confusionMatrixArray[2]
        f1 = (2*truePositives)/(2*truePositives+falsePositives+falseNegatives)
        return f1