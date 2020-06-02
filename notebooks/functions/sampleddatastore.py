#! usr/bin/env python3
import pandas as pd
import numpy as np
from datastore import DataStore
from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek, SMOTEENN
from imblearn.over_sampling import SMOTE, ADASYN
import os
from pathlib import Path

class SampledDataStore(DataStore):

    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "../../data/processed/")
    
    def initializeSamplers(self):
        self.makeDataDirectory()
        random_sampler = RandomOverSampler(sampling_strategy=0.1, random_state=42)
        smote = SMOTE(sampling_strategy=0.1, random_state=42)
        ada = ADASYN(sampling_strategy=0.1, random_state=42)
        smote_tomek = SMOTETomek(sampling_strategy=0.1, random_state=42)
        smote_enn = SMOTEENN(sampling_strategy=0.1, random_state=42)
        self.samplers = [random_sampler, smote, ada, smote_tomek, smote_enn]
        self.names = ["RandomSample", "SMOTE", "ADASYN", "SMOTETomek", "SMOTEEnn"]
        for sampler, name in zip(self.samplers, self.names):
            self.runSampler(sampler, name)
        self.loadAll()
        
    def makeDataDirectory(self):
        Path(SampledDataStore.filepath).mkdir(parents=True, exist_ok=True)
    
    def runSampler(self, sampler, name):
        xTrain, yTrain = self.getFileNames(name)
        if not self.doFilesExist(name):
            X_resampled, y_resampled = sampler.fit_resample(self.getxTrain(), self.getyTrain())    
            np.save(xTrain, X_resampled)
            np.save(yTrain, y_resampled)  

    def getFileNames(self, name):
        xTrain = f"{SampledDataStore.filepath}/{name}x.npy"
        yTrain = f"{SampledDataStore.filepath}/{name}y.npy"
        return xTrain, yTrain              
    
    def doFilesExist(self, name):
        xTrain, yTrain = self.getFileNames(name)
        return os.path.exists(f"{xTrain}") and os.path.exists(f"{yTrain}")
    
    def loadAll(self):
        self.RandomSample = self.load("RandomSample")
        self.SMOTE = self.load("SMOTE")
        self.ADASYN = self.load("ADASYN")
        self.SMOTETomek = self.load("SMOTETomek")
        self.SMOTEEnn = self.load("SMOTEEnn")

    def load(self, name):
        xTrain, yTrain = self.getFileNames(name)
        return [np.load(xTrain), np.load(yTrain)]
        
    def getRandomSampled(self):
        return self.RandomSample
    
    def getSMOTESampled(self):
        return self.SMOTE
    
    def getADASYNSampled(self):
        return self.ADASYN
    
    def getSMOTETOMEKSampled(self):
        return self.SMOTETomek
    
    def getSMOTEENNSampled(self):
        return self.SMOTEEnn