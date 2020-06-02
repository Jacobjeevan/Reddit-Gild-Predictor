from sampleddatastore import SampledDataStore
from imblearn.over_sampling import RandomOverSampler
import joblib
import os
from pathlib import Path

class Test_SampledDataStore:
    
    def __init__(self):
        self.SampledDataStore = SampledDataStore()
        self.filepath = self.SampledDataStore.filepath
        
    def test_makeDataDirectory(self):
        self.SampledDataStore.makeDataDirectory()
        assert os.path.exists(self.filepath)
        
    def test_runSampler(self):
        sampler = RandomOverSampler(sampling_strategy=0.1, random_state=42)
        name = "RandomSample"
        self.SampledDataStore.runSampler(sampler, name)
        
    def test_DoFilesExist(self):
        xTrain = "RandomSamplex.npy"
        assert self.SampledDataStore.doFilesExist("RandomSample") == os.path.exists(f"{self.filepath}/{xTrain}")

    def loadAll(self):
        self.SampledDataStore.loadAll()
        
    def test_RandomSamples(self):
        x, y = self.SampledDataStore.getRandomSampled()
        assert len(x) == len(y)
        
    def test_SMOTESamples(self):
        x, y = self.SampledDataStore.getSMOTESampled()
        assert len(x) == len(y)
        
    def test_ADASYNSamples(self):
        x, y = self.SampledDataStore.getADASYNSampled()
        assert len(x) == len(y)

    def test_SMOTETomekSamples(self):
        x, y = self.SampledDataStore.getSMOTETOMEKSampled()
        assert len(x) == len(y)

    def test_SMOTEENNSamples(self):
        x, y = self.SampledDataStore.getSMOTEENNSampled()
        assert len(x) == len(y)
        
    def test_all(self):
        self.test_makeDataDirectory()
        self.test_runSampler()
        self.test_DoFilesExist()
        SampledDataStore().initializeSamplers()
        self.loadAll()
        self.test_RandomSamples()
        self.test_SMOTESamples()
        self.test_ADASYNSamples()
        self.test_SMOTEENNSamples()
        
def main():
    Test_SampledDataStore().test_all()
    print("All tests passed!")


if __name__ == "__main__":
    main()