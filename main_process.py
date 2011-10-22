import threading, time

import rss_fetcher
import stream_reader
import shared

class NewsFetchThread(threading.Thread):

  def run(self):

    r = rss_fetcher.RssFetcher()

    while 1:
      print "Getting news...."
      r.getNews()

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

    print "keyword_list"
    print shared.keyword_list

    t.getTweetsBySubject(shared.keyword_list, t.receive_and_write_to_Mongo)

if __name__ == "__main__":
  NewsFetchThread().start()
