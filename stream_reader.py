import pycurl, json, pymongo, ConfigParser, bson, hashlib

import mongo_connector

class StreamReader:

  def __init__(self):
    self.tweet_collection = mongo_connector.MongoConnector().getCol("tweets")

    config = ConfigParser.RawConfigParser()
    config.read('config.conf')

    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')

    print "making new stream reader"

  def getTweetsBySubject(self, subjects, onwrite):
    stream_url  = "https://stream.twitter.com/1/statuses/filter.json"
    post_data = "track=" + ",".join(subjects)

    print "post_data = " + post_data

    conn = self.openStream(stream_url, onwrite)
    conn.setopt(pycurl.POST, 1)
    conn.setopt(pycurl.POSTFIELDS, post_data)
    conn.perform()
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
      data = json.loads(data)
      #data["_id"] = data["id"]
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
