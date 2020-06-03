from Data import Data

class ThreadData(Data):

    def __init__(self):
        super().__init__()
        self.data = {"thread_ids": [], "title": [], "author_ids": [], "upvotes": [
        ], "gildings": [], "created_utc": [], "premium": [], "num_comments": [], "edited": []}

    def retrieveData(self, submission):
        if (submission.id in self.getIds()):
            pass
        else:
            self.retrieveSubmission(submission)

    def retrieveSubmission(self, submission):
        self.retrieveThreadAuthor(submission)
        self.data["thread_ids"].append(submission.id)
        self.data["title"].append(submission.title)
        self.data["upvotes"].append(submission.ups)
        self.data["edited"].append(submission.edited)
        self.data["gildings"].append(submission.gildings)
        self.data["created_utc"].append(submission.created_utc)
        self.data["num_comments"].append(submission.num_comments)

    def retrieveThreadAuthor(self, submission):
        try:
            self.data["author_ids"].append(submission.author_fullname[3:])
            self.data["premium"].append(submission.author_premium)
        except:
            self.data["author_ids"].append("NaN")
            self.data["premium"].append("NaN")

    def getIds(self):
        return self.data["thread_ids"]

    def getLength(self):
        return len(self.data["thread_ids"])

    def saveData(self):
        super().saveData("ThreadData.json")
    
    def loadData(self):
        self.data = super().loadData("ThreadData.json")
