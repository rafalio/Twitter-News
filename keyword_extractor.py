import ConfigParser, pycurl, bson, json
import shared

class KeywordExtractor:
  
  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    self.key = config.get('alchemyapi','key')

  def getKeywordsByURL(self, url, story):
    url = str(url)
    # Alchemy API settings
    stream = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords"
    apikey_option = 'apikey=' + self.key
    url_option = 'url=' + url
    output_option = 'outputMode=' + 'json'
    keyword_limit_option = 'maxRetrieve=' + '5'
    stream += '?' + apikey_option + "&" + url_option + "&" + output_option + '&' + keyword_limit_option
    
    
    write_function = lambda data, story=story: self.recieve_and_save(data, story)
    #self.recieve_and_save
    
    conn = self.openStream(stream, write_function)
    conn.perform()
    conn.close()
    
  def openStream(self, stream, write_function):
    conn = pycurl.Curl()
    conn.setopt(pycurl.URL, stream)
    conn.setopt(pycurl.WRITEFUNCTION, write_function)
    return conn
    
  def getKeywords(self):
    for story in shared.stories:
      self.getKeywordsByURL(story["link"], story)
      
        
  def recieve_and_save(self, data, story):
    keywords = []
    try:
      data = json.loads(data)
      keyword_data =  data['keywords']
      for keyword_entry in keyword_data:
        keywords.append(keyword_entry['text'])
      story['alchemykeywords'] = keywords
      
    except ValueError:
      print "Error in data"
      print data


if __name__ == "__main__":
  k = KeywordExtractor()
  k.getKeywords()
  #k.getKeywordsByURL("http://bit.ly/oTPnyE")
  #k.getKeywordsByURL("http://techcrunch.com/2011/10/19/dropbox-minimal-viable-product/")