import threading
import mongo_connector
import shared
import time
import datetime

class Analysis(threading.Thread):
  def __init__(self,sleeptime=120,verbose=False):
    threading.Thread.__init__(self)
    connector = mongo_connector.MongoConnector()
    self.stories_collection = connector.getCol("stories")
    self.tweet_collection = connector.getCol("tweets")
    self.last_update = datetime.datetime.utcnow()
    self.sleeptime = sleeptime
    self.verbose = verbose
  
  def run(self):
    while 1:
      #Sleep for sleeptime
      if self.verbose:
        print "[INFO] Analysis Thread: sleeping for {0}.".format(self.sleeptime)
      time.sleep(self.sleeptime)
      
      self.add_stories_to_mongo(shared.stories)
      
      curr_time = datetime.datetime.utcnow()  
      self.add_new_time_period_to_stories(shared.stories, self.last_update, curr_time)
      self.last_update = curr_time

  def add_stories_to_mongo(self, stories):
    """Goes through a list of stories and adds them to the stories in mongo. 
    If story with this title is already there it just updates the date."""
    if self.verbose:
      print "[INFO] Analysis Thread: Adding extra stories to db."
      
    for story in stories:
      in_db = self.stories_collection.find_one({"title": story["title"]})
      if not in_db:
        if self.verbose:
          print "[INFO] Analysis Thread: Story {0} is not in db. Adding...".format(story["title"])
        self.stories_collection.insert(story)
      else:
        if self.verbose:
          print "[INFO] Analysis Thread: Story {0} is in db. Updating date.".format(story["title"])
        in_db.update({"$set": {"date": story["date"]}})
  
  def add_new_time_period_to_stories(self, stories, start, end):
    """Goes through tweets posted between start and end and assigns them to appropriate stories"""
    if self.verbose:
      print "[INFO] Analysis Thread: Adding time period from {0} to {1} to stories.".format(start,end)
      
    #Add time period stub to stories
    if self.verbose:
      print "[INFO] Analysis Thread: Adding curr_period to story objects"
    for story in stories:
      story["curr_period"] = {'period': end, 'tweets': []}
      
    #Loop through tweets
    if self.verbose:
      print "[INFO] Analysis Thread: Loading tweets from {0} to {1}.".format(start,end)
    tweets_in_time_period = self.tweet_collection.find({"created_at": {"$gte": start, "$lt": end}})
    for tweet in tweets_in_time_period:
      if self.verbose:
        print "  " + tweet["text"]
      for story in stories:
        for keyword in story["keywords"]:
          keyword_words = keyword.split()
          if len(keyword_words) <= 0:
            continue;
          exists = True
          for keyword_word in keyword_words:
            exists = exists and (tweet["text"].find(keyword_word) != -1)
          if exists:
            story["curr_period"]["tweets"].append(tweet["_id"])
            break;
    
    if self.verbose:
      print "[INFO] Analysis Thread: Pushing new periods to db."
      
    for story in stories:
      if self.verbose:
        print "[INFO] Analysis Thread: Pushing period with {0} tweets to {1}".format(len(story["curr_period"]["tweets"]), story["title"])
      self.stories_collection.update({"title":story["title"]},{"$push": {"periods": story["curr_period"]}})    