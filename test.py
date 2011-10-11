import pycurl, json, pymongo, ConfigParser

class TwitterStuff:

  def __init__(self):
    self.setupMongo()

    config = ConfigParser.RawConfigParser()
    config.read('config.conf')

    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')


  def setupMongo(self):
    self.connection = pymongo.Connection()
    self.db = self.connection["twitter_news"]

  def getTweetsBySubject(self, subjects, onwrite):
    stream_url  = "https://stream.twitter.com/1/statuses/filter.json"
    post_data = "track=" + ",".join(subjects)
    conn = self.openStream(stream_url, onwrite)
    conn.setopt(pycurl.POST, 1)
    conn.setopt(pycurl.POSTFIELDS, post_data)
    conn.perform()

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
      print data
      collection = self.db["tweets"]
      collection.insert(data)
    except ValueError:
      print "Error in tweet."

def main():
  t = TwitterStuff()


  # Change stevejobs to whatever keywords you want. Everything will be
  # written to a mongo datastore (create a db called "twitter_news"

  t.getTweetsBySubject(['stevejobs'], t.receive_and_write_to_Mongo)

main()
