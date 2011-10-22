import pymongo

class MongoConnector:

  def __init__(self):
    """docstring for __init__"""
    self.connection = pymongo.Connection()
    self.db = self.connection["twitter_news"]

  def getCol(self,collection):
    return self.db[collection]
