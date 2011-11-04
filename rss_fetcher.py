import feedparser, pymongo, json, hashlib, bson, threading, time

from dateutil import parser    # For easily parsing strings to Date

import keyword_extractor

import shared


class RssFetcher(threading.Thread):
  def __init__(self, rss="http://news.google.com/?output=rss", verbose=False, sleeptime=500):
    threading.Thread.__init__(self)
    self.extractor = keyword_extractor.KeywordExtractor()
    self.rss_link = rss
    self.verbose = verbose
    self.sleeptime = sleeptime
  
  def run(self):
    while 1:
      shared.event.clear()
      self.getNews()
      # We got the news, so we allow the tweet thread to work 
      shared.event.set()
      
      # Sleep for 5 minutes
      if self.verbose:
        print "[INFO] RSS Thread: Going to sleep for {0}.".format(self.sleeptime)
      time.sleep(self.sleeptime)
      if self.verbose:
        print "[INFO] RSS Thread: Waking up."
      
      shared.flag = True
  
  @staticmethod
  def gNews_title_fix(title):
    """Gets rid of the final hyphen of the Google News titles 
       from the google news api"""
    dashOccurence = (len(title) - 1) - title[::-1].index('-')
    return title[0:dashOccurence]
  
  @staticmethod
  def gNews_get_link(link):
    """Get the news URL from a weirdly crafted google news url"""
    return link[link.find("&url=")+len("&url="):]
  
  def getNews(self):
    """Download news stories and put them in the shared list"""
    if self.verbose:
      print "[INFO] RSS Thread: Fetching news feed from {0}.".format(self.rss_link)
    feed = feedparser.parse(self.rss_link)
    news_stories = []
    
    for entry in feed["items"]:
      if self.verbose:
        print "[INFO] RSS Thread: Parsing story {0}.".format(entry["title"])
      news_story = {}
      news_story["title"] = RssFetcher.gNews_title_fix(entry["title"])
      news_story["link"] = RssFetcher.gNews_get_link(entry["link"])
      news_story["date"] = parser.parse(entry["updated"])
      news_story["keywords"] = self.extractor.getKeywordsByURL(news_story["link"])
      if self.verbose:
        print "  Adding keywords: {0}.".format(news_story["keywords"])
      news_stories.append(news_story)
    
    if self.verbose:
      print "[INFO] RSS Thread: Putting a new set of stories into the shared list."
    shared.stories = news_stories
  

if __name__ == "__main__":
  r = RssFetcher()
  r.getNews()
