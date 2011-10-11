import feedparser
from future import Future

# List of rss feeds to get news from
top_stories = [ "http://news.google.com/?output=rss", "http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml"]

#Used to get all the news stories
future_calls = [Future(feedparser.parse,rss_url) for rss_url in top_stories]
feeds = [future_obj() for future_obj in future_calls] 

# Doing stuff with the feeds
for feed in feeds:
  for entry in feed["items"]:
    print entry["title"]