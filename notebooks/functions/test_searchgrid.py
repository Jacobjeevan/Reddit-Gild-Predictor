from datastore import DataStore
from searchgrid import SearchGrid
from gridmetrics import GridMetrics
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

class Test_SearchGrid:
    
    parameters = {'class_weight':[{0:1,1:10}]}
    classifier = LogisticRegression(random_state=42)
    variableNames = ['split' + str(i) + f'_test_truePositives' for i in range(1)]
    gridresults = {'split0_test_truePositives' : [5, 5], 'split0_test_falsePositives' : [5, 15], 
    'split0_test_falseNegatives' : [5, 15], 'mean_test_roc_auc' : [2, 1],
    'params': [{'class_weight' : {0:1, 1:10}}, {'class_weight' : {0:10, 1:1}}]}

    def test_InitializeGrid(self):
        self.GridSpace = SearchGrid()
        self.GridSpace.setClassifier(Test_SearchGrid.classifier)
        
    def test_setGridParameters(self):
        self.GridSpace.setGridParameters(Test_SearchGrid.parameters)
        assert Test_SearchGrid.parameters == self.GridSpace.getGridParameters()
        
    def test_initializeGridMetrics(self):
        self.metrics = GridMetrics(Test_SearchGrid.gridresults, NUM_SPLITS=1)
    
    def test_BestResults(self):
        params, scores = self.metrics.getBestResults()
        assert params == {'class_weight': {0: 1, 1: 10}}
        assert scores == ((0.5, 2))

    def test_getVariableNames(self):
         assert Test_SearchGrid.variableNames == self.metrics.getVariableNames("truePositives", 1)

    def test_calculateTotal(self):
        total = self.metrics.calculateTotal("truePositives", 0)
        assert total == 5

    def test_calculateF1(self):
        f1 = self.metrics.calculateF1(0)
        assert f1 == 0.5

    def test_calculateScores(self):
        self.metrics.calculateScores()
        assert self.metrics.getBestindex() == 0

    def test_calculateBestindex(self):
        # also tests calculateScore method (same as above, except
        # that there's only one parameter)
        gridresult = {'split0_test_truePositives' : [5], 'split0_test_falsePositives' : [5], 
        'split0_test_falseNegatives' : [5], 'mean_test_roc_auc' : [2],
        'params': [{'class_weight' : {0:1, 1:10}}]}
        metrics = GridMetrics(gridresult, NUM_SPLITS=1)
        metrics.calculateBestindex()
        assert metrics.getBestindex() == 0

    def test_run(self):
        self.GridSpace.run()
        assert self.GridSpace.getMetrics().getBestindex() == 0

    def test_all(self):
        self.test_InitializeGrid()
        self.test_setGridParameters()
        self.test_initializeGridMetrics()
        self.test_BestResults()
        self.test_getVariableNames()
        self.test_calculateTotal()
        self.test_calculateF1()
        self.test_calculateScores()
        self.test_calculateBestindex()
        self.test_run()

def main():
    Test_SearchGrid().test_all()
    print("All tests passed!")


if __name__ == "__main__":
    main()