import feedparser, pymongo, json, hashlib, bson, threading, time

from dateutil import parser    # For easily parsing strings to Date

import stream_reader
import mongo_connector
import keyword_extractor

import shared


class RssFetcher(threading.Thread):
  # List of rss feeds to get news from
  RSS_LINK = "http://news.google.com/?output=rss"

  def __init__(self):
    threading.Thread.__init__(self)
    self.extractor = keyword_extractor.KeywordExtractor()

  def run(self):
    while 1:

      shared.event.clear()

      self.getNews()

      # We got the news, so we allow the tweet thread to work 
      shared.event.set()

      # Sleep for 30 seconds
      time.sleep(60)
      shared.flag = True

      print "Finished sleeping, back to beginning of loop"
  


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
    feed = feedparser.parse(self.RSS_LINK)
    news_stories = []
    
    for entry in feed["items"]:
      news_story = {}
      news_story["title"] = RssFetcher.gNews_title_fix(entry["title"])
      news_story["link"] = RssFetcher.gNews_get_link(entry["link"])
      news_story["date"] = parser.parse(entry["updated"])
      news_story["keywords"] = self.extractor.getKeywordsByURL(news_story["link"])
      print news_story["keywords"]
      news_stories.append(news_story)
      
    shared.stories = news_stories

    
if __name__ == "__main__":
  r = RssFetcher()
  r.getNews()
