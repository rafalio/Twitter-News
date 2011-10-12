#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
import twitter
import json
import pymongo
from pymongo import Connection


from twitter.oauth_dance import oauth_dance

consumer_key = '2UHgepnNHqKF7abtF8klqQ' 
consumer_secret = 'fq4ubYC7nwAObfdVD9J2htfxbrGs0Av4vdUtPIU0'

connection = Connection()
db = connection['twitter-news']
users_ = db['users']



class Network:
   
  def __init__(self, base_users):
    (oauth_token, oauth_token_secret) = oauth_dance('twitNews_docproj', consumer_key, consumer_secret)
    t = twitter.Twitter(domain='api.twitter.com', api_version='1', auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,
    consumer_key, consumer_secret))
    
    current_lvl = set([])
    temp = set([])
    
    self.network = nx.DiGraph()
    for u in base_users:
      u_id = t.users.lookup(screen_name=u)[0]["id"]
      self.network.add_node(u_id)
      current_lvl.add(u_id)
    
    for i in range(0,1):
      for u_id in current_lvl:      
        follow_ids = t.friends.ids(user_id=u_id)
        for f_id in follow_ids:
          if f_id in self.network:
            temp.add(f_id)
          #print f_id
          self.network.add_edge(u_id, f_id)
      current_lvl = temp
      temp = set([])
    
    mapping={}
    nodes = self.network.nodes()
    for i in range(0,len(nodes),100):
      users = t.users.lookup(user_id=(",".join(map(str,nodes[i:i+100]))))
      for u in users:
        mapping[u["id"]] = u["screen_name"]
        users_.insert(u)
      
    nx.relabel_nodes(self.network,mapping,copy=False)

    
    print self.network.nodes()
    print self.network.edges()   


t = Network(["but_is_it_art","jamalzkhan"])