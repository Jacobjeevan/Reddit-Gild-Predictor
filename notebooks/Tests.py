from DataStore import DataStore
import utils
from SearchGrid import SearchGrid
from CrossValidate import CrossValidate
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
import joblib

sampleGrid = joblib.load("sampleGrid.pkl")
sampleGridResults = sampleGrid.cv_results_

class Tests:
    
    parameters = {'class_weight':[{0:1,1:10}]}
    classifier = LogisticRegression(random_state=42)
    variableNames = ['split' + str(i) + f'_test_truePositives' for i in range(1)]
    
    def __init__(self):
        self.getData = DataStore()
    
    def test_DataStore(self):
        xTrain, yTrain, xTest, yTest = self.getData()
        assert len(xTrain) == len(yTrain)
        assert len(xTest) == len(yTest)
        
    def test_InitializeGrid(self):
        self.GridSpace = SearchGrid(self.getData)
        self.GridSpace.setGridParameters(Tests.parameters)
        self.GridSpace.setClassifier(Tests.classifier)
        
    def test_runGrid(self):
        self.Grid = self.GridSpace.trainGrid()
        self.GridResults = self.Grid.cv_results_
        
    def test_getVariableNames(self):
         assert Tests.variableNames == self.GridSpace.getVariableNames("truePositives", 1)

    def test_calculateF1(self):
        f1 = self.GridSpace.calculateF1(sampleGridResults, 0)
        assert round(f1,2) == 0.30

    def test_calculate_totals(self):
        total = self.GridSpace.calculateTotal(sampleGridResults, "truePositives", 0)
        assert total >= 0
    
    def test_crossValidate(self):
        classifier = DummyClassifier(strategy="constant", constant=1)
        crossvalidate = CrossValidate(self.getData)
        crossvalidate.setClassifier(classifier)
        crossvalidate.run()
        assert round(crossvalidate.getScores()) == 0, 0

    def run_tests(self):
        #self.test_DataStore()
        self.test_InitializeGrid()
        self.test_calculateF1()
        self.test_getVariableNames()
        self.test_calculate_totals()
        #self.test_runGrid()
        #self.test_crossValidate

Tests().run_tests()