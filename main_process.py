import rss_fetcher
import stream_reader
import analysis

   
class Twitinfo:
  def start(self):
    self.r = rss_fetcher.RssFetcher().start()
    self.s = stream_reader.StreamReader().start()
    self.a = analysis.Analysis().start()
  
if __name__ == "__main__":
  Twitinfo().start()
