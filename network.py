#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
import json
from pymongo import Connection

from twitter_login import login


connection = Connection()
db = connection['twitter-news']
users_ = db['users']



class Network:
   
  def __init__(self, base_users):
    self.t = login()

    try:
      self.loadFromFile()
    except:
      self.makeNetwork(base_users)

    print self.network.nodes()
    print self.network.edges()   

  def makeNetwork(self,base_users):
    current_lvl = set([])
    temp = set([])

    self.network = nx.DiGraph()

    for u in base_users:
      u_id = self.t.users.lookup(screen_name=u)[0]["id"]
      self.network.add_node(u_id)
      current_lvl.add(u_id)

    for i in range(0,1):
      for u_id in current_lvl:      
        follow_ids = self.t.friends.ids(user_id=u_id)
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
      users = self.t.users.lookup(user_id=(",".join(map(str,nodes[i:i+100]))))
      for u in users:
        mapping[u["id"]] = u["screen_name"]
        u["_id"] = u["id"]
        users_.insert(u)

    nx.relabel_nodes(self.network,mapping,copy=False)
    nx.write_gpickle(self.network,"graph.pickle")

  def loadFromFile(self):
    self.network = nx.read_gpickle("graph.pickle")

t = Network(["but_is_it_art","jamalzkhan"])

