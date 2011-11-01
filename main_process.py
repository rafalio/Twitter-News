import threading, time

import rss_fetcher
import stream_reader
import shared
import keyword_extractor

   
class Twitinfo:
  
  def start(self):
    self.r = rss_fetcher.RssFetcher().start()
    self.s = stream_reader.StreamReader().start()
  
if __name__ == "__main__":
  Twitinfo().start()
