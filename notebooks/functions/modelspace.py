from datastore import DataStore
from sklearn.model_selection import RepeatedStratifiedKFold
import joblib
from pathlib import Path
import os

class ModelSpace:
    
    def __init__(self):
        self.Classifier = None
        self.getData = DataStore()
        self.rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=2, random_state=42)
    
    def getDataStore(self):
        return self.getData
    
    def setClassifier(self, Classifier):
        self.Classifier = Classifier
        
    def getClassifier(self):
        return self.Classifier
    
    def getCrossValidator(self):
        return self.rskf
    
    def run(self):
        pass

    def load(self, file):
        self = joblib.load(file)
        return self
    
    def save(self, name):
        filepath = self.makeFilepath()
        fileName = filepath + f"/{name}.pkl"
        joblib.dump(self, fileName)
        
    def makeFilepath(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "../models")
        Path(filepath).mkdir(parents=True, exist_ok=True)
        return filepath
    