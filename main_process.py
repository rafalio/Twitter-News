import threading, time

import rss_fetcher
import stream_reader
import shared
import keyword_extractor

class NewsFetchThread(threading.Thread):
  def run(self):
    r = rss_fetcher.RssFetcher()
    k = keyword_extractor.KeywordExtractor()
    
    while 1:
      print "Getting news...."
      r.getNews()
      
      print "Getting keywords..."
      k.getKeywords()
      
      print "Starting fetching thread..."
      s = StreamFetchThread() 
      s.start()
      
      print "Sleeping..."
      time.sleep(60*5)
      
      print "Stopping fetching thread"
      s._Thread__stop()
    
  
  
class StreamFetchThread(threading.Thread):
  def run(self):
    print "In fetching thread"
    t = stream_reader.StreamReader()
    
    print "Stories:"
    print shared.stories
    
    keywords = set([])
    for s in shared.stories:
      for k in s["keywords"]:
        keywords.add(k)
    
    t.getTweetsBySubject(keywords, t.receive_and_write_to_Mongo)
  
if __name__ == "__main__":
  NewsFetchThread().start()
