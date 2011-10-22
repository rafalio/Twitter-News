#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
import json
import sys
#from pymongo import Connection

from twitter_login import login


#connection = Connection()
#db = connection['twitter-news']
#users_ = db['users']



class Network:
   
  def __init__(self, base_users):
    try:
      self.loadFromFile()
    except:
      self.makeNetwork(base_users,2,verbose=True)

    s = '{"nodes":['
    for n in self.network.nodes():
      s += '{"name":"' + n + '"},'
    s = s.rpartition(',')[0]
    s += '],"links":['
    for n in self.network.edges():
      s += '{"source":"' + n[0] + '","target":"' + n[1] + '"},'
    s = s.rpartition(',')[0]
    s += ']}'
    f = open('graph.json','w+')
    f.write(s)
    print s

  def makeNetwork(self,base_users,depth,verbose=False):
    current_lvl = set([])
    next_lvl = set([])

    self.network = nx.DiGraph()


    self.t = login()
    count = 0
    api_count = 0
    # Add base users to the network
    for u in base_users:
      # Get user id
      if verbose:
        api_count = api_count + 1
        print "API call {}".format(api_count)
      u_id = self.t.users.lookup(screen_name=u)[0]["id"]
      
      if verbose:
        count = count + 1
        print "Adding {} user with id {}".format(count, u_id)
      self.network.add_node(u_id)
      current_lvl.add(u_id)

    # Go through the current_lvl depth times
    for i in range(0,depth):
      # Go through all u_ids in current level
      if verbose:
        print current_lvl
      for u_id in current_lvl:
        # Only expand u+id if level 1 (no connections yet)
        # or if at least as many followers as current lvl
        if verbose:
          api_count = api_count + 1
          print "API call {}, expanding user {}".format(api_count, u_id)
        follow_ids = self.t.friends.ids(user_id=u_id)
        for f_id in follow_ids:
          # If f_id not in the network add to next_lvl
          if f_id not in self.network:
            if verbose:
              count = count + 1
              print "Adding {} user with id {}".format(count, f_id)
            next_lvl.add(f_id)
          if verbose:
            print "Connecting {} with {}".format(u_id, f_id)
          # Connect u_id to f_id
          self.network.add_edge(u_id, f_id)
      current_lvl = set([])
      for f_id in next_lvl:
        if self.network.in_degree(f_id) > i+1:
          current_lvl.add(f_id)
      next_lvl = set([])

    # remove users with only one connectios
    for u in self.network:
      if (self.network.in_degree(u) < 2):
        self.network.remove_node(u)
    
    if verbose:
      print "\n\n-----------------------Relabeling nodes-----------------------"
    mapping={}
    nodes = self.network.nodes()
    for i in range(0,len(nodes),100):
      if verbose:
        api_count = api_count + 1
        print "API call {}".format(api_count)
      users = self.t.users.lookup(user_id=(",".join(map(str,nodes[i:i+100]))))
      for u in users:
        mapping[u["id"]] = u["screen_name"]
        u["_id"] = u["id"]
        #users_.insert(u)
    nx.relabel_nodes(self.network,mapping,copy=False)
    nx.write_gpickle(self.network,"graph.pickle")

  def loadFromFile(self):
    self.network = nx.read_gpickle("graph.pickle")

t = Network(["ihnatko","gruber","siracusa"])

