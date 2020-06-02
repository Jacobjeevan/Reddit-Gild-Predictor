from crossvalidate import CrossValidate
from sklearn.dummy import DummyClassifier
from cvmetrics import CVMetrics

class Test_CV:
    
    def __init__(self):
        self.cvresults = {'test_truePositives' : [5, 5], 'test_falsePositives' : [5, 5], 'test_falseNegatives' : [5, 5],
                    'test_roc_auc' : [1, 2, 3]}
        self.Metrics = CVMetrics(self.cvresults)
        
    def test_calculateTotal(self):
        assert self.Metrics.calculateTotal('test_truePositives') == 10
        
    def test_calculateF1(self):
        self.Metrics.calculateF1()
        assert self.Metrics.scores == [0.5]
        
    def test_calculateROC(self):
        Metrics = CVMetrics(self.cvresults)
        Metrics.calculateROC()
        assert Metrics.scores == [2]
        
    def test_getScores(self):
        Metrics = CVMetrics(self.cvresults)
        assert Metrics.getScores() == [0.5, 2]
    
    def test_run(self):
        classifier = DummyClassifier(strategy="constant", constant=1)
        cv = CrossValidate()
        cv.setClassifier(classifier)
        cv.run()
        Metrics = cv.getMetrics()
        f1, roc = Metrics.getScores()
        assert round(f1) == 0
        assert round(roc) == 0
        
    def test_all(self):
        self.test_calculateTotal()
        self.test_calculateF1()
        self.test_calculateROC()
        self.test_getScores()
        self.test_run()

def main():
    Test_CV().test_all()
    print("All tests passed!")


if __name__ == "__main__":
    main()