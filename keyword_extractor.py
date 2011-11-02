import ConfigParser, json, urllib

class KeywordExtractor:
  
  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    self.key = config.get('alchemyapi','key')
    self.stream = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords"
    self.apikey_option = 'apikey=' + self.key
    self.output_option = 'outputMode=' + 'json'
    self.keyword_limit_option = 'maxRetrieve=' + '5'

  def getKeywordsByURL(self, url):
    # Building Alchemy API call
    call = self.stream +  '?' + self.apikey_option + "&" + 'url=' + url + "&" + self.output_option + '&' + self.keyword_limit_option
    data = urllib.urlopen(call)
    keywords = []
    try:
      data = json.loads(data.read())
      keyword_data =  data['keywords']
      for keyword_entry in keyword_data:
        keywords.append(str(keyword_entry['text']))
    except ValueError:
      print "Error in data from the keyword extractor"
      print data
    return keywords

if __name__ == "__main__":
  k = KeywordExtractor()
  print k.getKeywordsByURL("http://bit.ly/oTPnyE")
  print k.getKeywordsByURL("http://techcrunch.com/2011/10/19/dropbox-minimal-viable-product/")