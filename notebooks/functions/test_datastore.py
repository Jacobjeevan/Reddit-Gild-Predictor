from datastore import DataStore

class Test_DataStore:
    
    def __init__(self):
        self.getData = DataStore()
    
    def test_DataStore(self):
        xTrain, yTrain, xTest, yTest = self.getData()
        assert len(xTrain) == len(yTrain)
        assert len(xTest) == len(yTest)
 
    def test_all(self):
        self.test_DataStore()
        
def main():
    Test_DataStore().test_all()
    print("All tests passed!")

if __name__ == "__main__":
    main()