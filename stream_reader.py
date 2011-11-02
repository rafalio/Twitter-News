import pycurl, json, pymongo, ConfigParser, bson, hashlib, threading, itertools

import mongo_connector
import shared

class StreamReader(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.tweet_collection = mongo_connector.MongoConnector().getCol("tweets")

    config = ConfigParser.RawConfigParser()
    config.read('config.conf')

    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')

    print "making new stream reader"


  def run(self):

    while 1:
      print "Waiting for RSS to get news"
      shared.event.wait()
      print "Got news..."
      self.getTweetsBySubject(list(itertools.chain.from_iterable(map(lambda a : a["keywords"], shared.stories))),
                              self.receive_and_write_to_Mongo)
      shared.flag = False;

  def getTweetsBySubject(self, subjects, onwrite):

    print "Starting the stream getting...."

    stream_url  = "https://stream.twitter.com/1/statuses/filter.json"
    print subjects
    post_data = "track=" + ",".join(subjects)
    print "post_data = " + post_data

    conn = self.openStream(stream_url, onwrite)
    conn.setopt(pycurl.POST, 1)
    conn.setopt(pycurl.POSTFIELDS, post_data)

    # Stream until I need to change the keyword list
    try:
      conn.perform()
    except Exception:
      print "Done..."
      conn.close()

  def openStream(self, stream, write_function):
    conn = pycurl.Curl()
    conn.setopt(pycurl.USERPWD, "%s:%s" % (self.twitter_username, self.twitter_password))
    conn.setopt(pycurl.URL, stream)
    conn.setopt(pycurl.WRITEFUNCTION, write_function)
    return conn

  def on_receive(self, data):
    print json.loads(data)

  def receive_and_write_to_Mongo(self, data):
    try:

      # Means we need to restart with new set of keywords
      if shared.flag:
        print "return -1 ASDFASDFASDFASDF"
        # This will get out of the pycurl thread, it will cause
        # an exception
        return -1

      data = json.loads(data)
      data["_id"] = bson.objectid.ObjectId(hashlib.md5(str(data["id"])).hexdigest()[:24])
      print data["text"]
      self.tweet_collection.insert(data)

    except ValueError:
      print "Error in tweet."
      print data

def main():
  t = StreamReader()
  t.getTweetsBySubject(['libya,gaddafi'], t.receive_and_write_to_Mongo)

if __name__ == "__main__":
  main()
