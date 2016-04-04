# -*- coding: utf-8 -*-
from __future__ import with_statement
import os, sys
import json
from collections import deque
import getopt
from dateutil.parser import parse
from datetime import datetime,timedelta

class HashtagState:
    def __init__(self, created_at, num_edges):
       self.created_at = created_at 
       self.num_edges = num_edges

class HashtagHist:
    def __init__(self, created_at, hashtags):
       self.created_at = created_at
       self.hashtags = hashtags


class HashtagGraph:
   '''

      This is the main class that contains Hashtags Graph
   '''
   def __init__(self):
       self.num_nodes = 0
       self.num_total_degree = 0
       self.num_edges = 0
       self.node_list = []
       self.queue_hist_hashtags = deque([])
       self.queue_hist_total_edges = deque([])
       self.list_avg_Degree = []
       self.maximum_timestamp = parse("Mon Jan 01 00:00:00 +0000 1000", fuzzy=True)


   def run(self, input_filename):
       '''
     
        This is the interface for running the graph_grow and graph_prune
       '''
       if(self.inputfile_open(input_filename) == False):
           return 
       count = 0
       for tweet_line in self.inputfile:
           # parse tweet line
           count = count + 1
           print("Line: {0:d} ===============================".format(count))
           hashtags, created_at = parse_tweet(tweet_line)
           timestamp = parse_time(created_at)
           if timestamp > self.maximum_timestamp:
               self.maximum_timestamp = timestamp
               # graph check and prunning only when the time window moves
               self.graph_prune(timestamp)
           elif not is_valid(timestamp, self.maximum_timestamp):
               #out of 60 second window
               print("out of order in time and outside the 60-second")
               continue
           # grow graph
           self.graph_grow(hashtags, created_at)
           self.list_avg_Degree.append(float(self.num_total_degree) / float(self.num_nodes))
           print("Total nodes {0:3d}  Total Degrees {1:5d}  Avg. Degree {2:.2f}".format(self.num_nodes, self.num_total_degree, self.list_avg_Degree[-1])) 

       self.inputfile.close()


   def graph_grow(self, hashtags, created_at):
       '''

          use the hash table to store the total degree for each hashtag
          modify the graph strcture for each given list of hashtags
       ''' 
       #add code here
       if len(hashtags) == 1:
           #drop single hashtag
           print("drop single hashtag")
           return 

       # find the number of new nodes and parse current time
       num_newnodes = self.count_new_nodes(hashtags)
       timestamp = parse_time(created_at)
       #print("Add {0:3d} nodes".format(num_newnodes))
       self.num_nodes = self.num_nodes + num_newnodes

       #if ( num_newnodes > 0 or ifnewEdge ):
       # store history of hashtags
       hashtag_hist_node = HashtagHist(timestamp, hashtags)
       self.queue_hist_hashtags.append(hashtag_hist_node)
 
       hashtags_hist = []
       for hashtag_node in self.queue_hist_hashtags:
           hashtags_hist.append(hashtag_node.hashtags)

       # inclusion-exclusion principle
       self.num_edges, _  = edge_update(hashtags_hist, len(hashtags_hist))
       self.num_total_degree = self.num_edges * 2
       state = HashtagState(timestamp, self.num_edges)
       self.queue_hist_total_edges.append(state)
       return



   def graph_prune(self, time_stamp):
       '''

           pruning of the graph according to the time_stamp. 
           For each node, see the top of the queue, if the time is out of the 60 second window, pop the queue, use decrease the degree according to the degree_increase value

       '''
       if len(self.queue_hist_hashtags) == 0:
           return 

       while( not is_valid(self.queue_hist_hashtags[0].created_at, time_stamp)):
           old_hashtags = self.queue_hist_hashtags.popleft() #delete all out-of-window cases
           #decide number of nodes to delete
           nodelist = list(set(self.node_list) - set(old_hashtags.hashtags))
           self.node_list = nodelist
           if len(self.queue_hist_hashtags) == 0:
              break

       for i in range(len(self.queue_hist_hashtags)):
           hashtags = self.queue_hist_hashtags[i].hashtags
           num_newnodes = self.count_new_nodes(hashtags)

       while( not is_valid(self.queue_hist_total_edges[0].created_at, time_stamp)):
           self.queue_hist_total_edges.popleft() #delete all out-of-window cases
           if len(self.queue_hist_hashtags) == 0:
              break
       self.num_nodes = len(self.node_list)
       return



       

   def count_new_nodes(self, hashtags):
       '''

          count number of new nodes in hashtag list
       '''
       if(len(self.node_list) == 0):
           nodelist = hashtags
           num_newnodes = len(hashtags)
       else:
           num_newnodes = len(set(hashtags) - set(self.node_list))
           nodelist = list(set(hashtags + self.node_list))
       self.node_list = nodelist
       return num_newnodes


#   def node_degree_adjust(self, timestamp, hashtags):
#       '''
#    
#           Given the current time, and hashtags, check previous time for every node in the hashtags. 
#           if two nodes in hashtags has the same time in history, then their edge is redundant, otherwise this edge is new. Both nodes add one degree
# 
#       '''
#       node_degree_adjust = {}
#       #n_neighbor = len(hashtags) - 1
#       for hashtag in hashtags:
#           node_degree_adjust[hashtag] = 0
#
#       ifnewEdge = False
#       list_common_nodes = []
#       set_common_nodes = {}
#       for hashtag_node in self.queue_hist_hashtags:
#           rep_nodes = [hashtag for hashtag in hashtags if hashtag in hashtag_node.hashtags ]
#           #if len(rep_nodes) == 1:
#           #    common_nodes.append(rep_nodes[0]) #store repeated nodes
#           if len(rep_nodes) > 2: 
#               #repeated edges
#               #s = HashtagHist(timestamp, rep_nodes)
#               #self.queue_hashtags_share.append(s)
#               list_common_nodes.append(rep_nodes)
#               set_common_nodes = set.union(set(rep_nodes), set_common_nodes)
#
#       for hashtag in set_common_nodes:
#           node_degree_adjust[hashtag] = - list_common_nodes.count(hashtag)
#
##       for rep_node, value in node_degree_adjust.iteritems():
##           if value < 0:
##               node_degree_adjust[rep_node] = node_degree_adjust[rep_node] + n_neighbor 
##           if len(set(common_nodes)) > 1: 
##               # a new edge whose two ends both appear before but not form a repeated edge
##               if (rep_node in set(common_nodes)) and (node_degree_adjust[rep_node] == 0):
##                   node_degree_adjust[rep_node] = node_degree_adjust[rep_node] + n_neighbor
##
##
#       for rep_node, value in node_degree_adjust.iteritems():
#           if value < 0:
#               ifnewEdge = True
#               break
#
#       return (node_degree_adjust, ifnewEdge)


   def empty(self):
       self.hash_nodeDegree = {}
       self.hash_nodeIncrease = {}
       self.num_nodes = 0
       self.num_total_degree = 0
       self.maximum_timestamp = parse("Mon Jan 01 00:00:00 +0000 1000", fuzzy=True)
       self.queue_hist_hashtags.empty()
       self.list_avg_Degree = []

   def inputfile_open(self, input_filename):
       try:
            self.inputfile = open(input_filename , 'r' )
       except EnvironmentError:
            print 'open inputfile failure'
            return False
       else:
            return True

   def outputfile_open(self, output_filename):
       try:
            open(output_filename,"w").close()
       except EnvironmentError:
            print 'open outputfile failure'
            return False
       else:
            self.outputfile = open(output_filename , 'w')
            return True

   def write_txt(self, output_filename):
       '''

            Write to given file
       '''
       if(self.outputfile_open(output_filename) == False):
           return
       #self.outputfile.write("\n".join(str(self.list_avg_Degree)))
       for num in self.list_avg_Degree:
           print >> self.outputfile, "{0:.2f}".format(num)
       try:
           self.outputfile.close()
       except AttributeError:
           print("no output")


   def __str__(self): 
       print("Number of nodes: {0:5d}".format(self.num_nodes))
       print("Average degree: ")
       for num in self.list_avg_Degree:
           print("{0:.3f}".format(num))
'''
=================================================================
'''
def edge_update(hashtags_hist, n):
    if n == 0:
        return (0, [])
    
    if n == 1:
        return (complete_edge(len(hashtags_hist[0])), [])
    else:
        hashtags = hashtags_hist[n-1]
        hashtags_inter_hist = []
        for i in range(n-1):
            hashtags_inter = [hashtag for hashtag in hashtags if hashtag in hashtags_hist[i] ]
            hashtags_inter_hist.append(hashtags_inter)
        temp1, _ = edge_update(hashtags_hist, n-1) 
        temp2, _ = edge_update(hashtags_inter_hist, n-1)
        temp = temp1  + complete_edge(len(hashtags))
        temp = temp - temp2
        return (temp, hashtags_inter_hist) 


#def edge_update_aux(num_edges, hist_hashtags, hashtags, n, stored_result):
#    '''
#        Use dynamic programming for inclusion and exclusion 
#    '''
#
#    if n == 0:
#       stored_result.append(complete_edge(len(hashtags)))
#       return complete_edge(len(hashtags))
#    elif n == 1:
#       hashtags_pre = hist_hashtags[0]
#       hashtags_inter = [hashtag for hashtag in hashtags if hashtag in hashtags_pre]
#       return complete_edge(len(hashtags)) + stored_result[0] - complete_edge(len(hashtags_inter))
#    else:
#        for i in range()




def complete_edge(n):
    return int((n-1)*n/2)

def parse_tweet(tweet_line):
    '''

       Read one line of the tweet.txt file and parse it by json·
       The extracted "created_at" and "hashtags" are returned
       txtfile is the file handle created before calling the function

    '''
    #with open(filename) as txtfile: 
    jsonObj = json.loads(tweet_line)
    created_at = jsonObj.get("created_at")
    hashtag_list = jsonObj.get("entities").get("hashtags")
    hashtag_txt_list = [ hashtag_list[i].get('text') for i in range(len(hashtag_list)) ]

    return (hashtag_txt_list, created_at)

def parse_time(created_at):
    '''

       return datetime.datetime format 
    '''
    return parse(created_at, fuzzy=True)

def is_valid(time_stamp, time_stamp_ref):
    '''

         time_stamp is the old time 
         time_stamp_ref is the current time 
         time_stamp is datetime.datetime(year, month, day, hour, min, secend, tzinfo=tzutc()) 
    '''
    diff = time_stamp_ref - time_stamp
    #diff_normal = divmod(diff.days * 86400 + diff.seconds, 60)
    return ((diff.days == 0) and (diff.seconds < 60) )
#=====================  main =================================
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print 'average_degree.py -i <inputfile> -o <outputfile>'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'average_degree.py -i <inputfile> -o <outputfile>'
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    #construct graph object
    HashGraphObj = HashtagGraph()
    print("Running ... ")
    HashGraphObj.run(inputfile)
    print("Write to " + outputfile)
    HashGraphObj.write_txt(outputfile)




if __name__ == "__main__":
    main(sys.argv[1:])