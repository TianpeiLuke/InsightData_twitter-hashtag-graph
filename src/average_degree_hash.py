# -*- coding: utf-8 -*-
from __future__ import with_statement
import os, sys
import json
from collections import deque
import getopt
from dateutil.parser import parse
from datetime import datetime,timedelta

class HashtagState:
    def __init__(self, created_at, degree_increase):
       self.created_at = created_at 
       self.degree_increase = degree_increase

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
       self.node_list = []
       self.hash_nodeDegree = {}
       self.queue_hist_hashtags = deque([])
       self.queue_hist_hashtags_rep = deque([])
       self.list_avg_Degree = []
       self.maximum_timestamp = parse("Mon Jan 01 00:00:00 +0000 1000", fuzzy=True)


   def restart(self):
       self.num_total_degree = 0
       self.num_nodes = 0
       self.node_list = []
       self.hash_nodeDegree = {}
       self.queue_hist_hashtags.clear()
      
        

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
           if len(hashtags) > 1:
              hashtag_hist_node = HashtagHist(created_at, hashtags)
              self.queue_hist_hashtags_rep.append(hashtag_hist_node) 
              self.graph_grow(hashtags, created_at)

           self.list_avg_Degree.append(float(self.num_total_degree) / float(self.num_nodes))
           print("Total nodes {0:3d}  Total Degrees {1:5d}  Avg Degree {2:.3f}".format(self.num_nodes, self.num_total_degree, self.list_avg_Degree[-1])) 

       self.inputfile.close()


   def graph_grow(self, hashtags, created_at):
       '''

          use the hash table to store the total degree for each hashtag
          modify the graph strcture for each given list of hashtags
       ''' 
       #add code here
       if len(hashtags) == 1:
           #drop single hashtag
           return 
       # find the number of new nodes and parse current time
       num_newnodes = self.count_new_nodes(hashtags)
       timestamp = parse_time(created_at)
       self.num_nodes = self.num_nodes + num_newnodes
       #node degree adjustment: consider the case
       #1.  when both ends of the edge exists previously but the edge itself is not included 
       (node_degree_adjust, ifnewEdge) = self.node_degree_adjust(timestamp, hashtags)
       if (ifnewEdge):
           print("Edge adjustment")
           print(node_degree_adjust)
       if ( num_newnodes > 0 or ifnewEdge ):
           # store history of hashtags
           hashtag_hist_node = HashtagHist(timestamp, hashtags)
           self.queue_hist_hashtags.append(hashtag_hist_node)

       for hashtag in hashtags:
           try: 
               self.hash_nodeDegree[hashtag] = self.hash_nodeDegree[hashtag] + num_newnodes 
           except KeyError:
               self.hash_nodeDegree[hashtag] = len(hashtags) - 1
               self.num_total_degree = self.num_total_degree + len(hashtags) - 1 
           else:
               if (num_newnodes + node_degree_adjust[hashtag]) > 0 :
                  self.hash_nodeDegree[hashtag] = self.hash_nodeDegree[hashtag] + node_degree_adjust[hashtag]
                  self.num_total_degree = self.num_total_degree + num_newnodes + node_degree_adjust[hashtag] 
               
         
       return



   def graph_prune(self, time_stamp):
       '''

           pruning of the graph according to the time_stamp. 
           For each node, see the top of the queue, if the time is out of the 60 second window, pop the queue, use decrease the degree according to the degree_increase value

       '''
       if len(self.queue_hist_hashtags_rep) == 0:
           return 
       ifrebuild = False
       while( not is_valid(parse_time(self.queue_hist_hashtags_rep[0].created_at), time_stamp)):
           old_hashtags = self.queue_hist_hashtags_rep.popleft() #delete all out-of-window cases
           ifrebuild = True
           if len(self.queue_hist_hashtags_rep) == 0:
              break
#           common_edge_nodes = []
#                  common_edge_nodes.append(rep_nodes)
#           k = len(old_hashtags)
#           for hashtag in set(common_edge_nodes):
#               #delete all out-of-window cases
#               #if out of window, we should delete it
#               #print("Adjust degree of node " + hashtag)
#               if(not is_valid(self.hash_nodeIncrease[hashtag].created_at, time_stamp)):
#                   s_temp = self.hash_nodeIncrease[hashtag].popleft()
#               #s_temp = queue.popleft() # add more
#               degree_adjust = - s_temp.degree_increase
#               #delete too many edges, recover the intersection of the deleted edge and all after
#               for sublist in common_edge_nodes:
#                   if hashtag in sublist
#
#               self.hash_nodeDegree[hashtag] = self.hash_nodeDegree[hashtag] + degree_adjust
#               self.num_total_degree = self.num_total_degree + degree_adjust
#                      if len(queue) == 0:
#                        delete_node.append(hashtag)
#                      break

#       while( not is_valid(self.queue_hist_hashtags[0].created_at, time_stamp)):
#           self.queue_hist_hashtags.popleft()
#           if len(self.queue_hist_hashtags) == 0:
#              break
       if ifrebuild:
          print("rebuild graph")
          self.restart()
          for i in range(len(self.queue_hist_hashtags_rep)):
              hashtags = self.queue_hist_hashtags_rep[i].hashtags
              created_at = self.queue_hist_hashtags_rep[i].created_at
              self.graph_grow(hashtags, created_at)

       return 
      # self.num_nodes = len(self.node_list) 

#               rep_nodes = [hashtag for hashtag in old_hashtags if hashtag in hashtag_node.hashtags ]
#               if len(rep_nodes) > 2:
       #delete_node = []
       #delete too many edges, recover the intersection of the deleted edge and all after
#       Delete_node = list(set(self.hash_nodeDegree.keys())- set(self.node_list))
#       for hashtag in Delete_node:
#           self.hash_nodeIncrease.pop(hashtag, None) 
#           self.hash_nodeDegree.pop(hashtag, None) 
#       self.num_nodes = self.num_nodes - len(set(delete_node))
#       if len(set(delete_node)) >0:
#           #print("Delete {0:3d} nodes".format(len(set(delete_node))))
#           for hashtag in set(delete_node):
#              # if the queue is empty, means that this node should be deleted
#              self.hash_nodeIncrease.pop(hashtag, None)
#              self.hash_nodeDegree.pop(hashtag, None)
#       return


   def ifSharedEdges(self, hashtags):
       '''
       
           Store the intersecion(hashtags, self.queue_hist_hashtags_rep[i].hashtags) for i= 1.. n-1

       '''
       ifsharedEdge = False
       shared_nodes = []
       for hashtag_node in self.queue_hist_hashtags_rep:
           rep_nodes = [hashtag for hashtag in hashtags if hashtag in hashtag_node.hashtags ]
           if len(rep_nodes) >= 2:
              ifsharedEdge = True
              s = HashtagHist(hashtag_node.created_at, rep_nodes)
              shared_nodes.append(s)
       return (ifsharedEdge, shared_nodes)


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


   def node_degree_adjust(self, timestamp, hashtags):
       '''
    
           Given the current time, and hashtags, check previous time for every node in the hashtags. 
           if two nodes in hashtags has the same time in history, then their edge is redundant, otherwise this edge is new. Both nodes add one degree
 
       '''
       node_degree_adjust = {}
       n_neighbor = len(hashtags) - 1
       for hashtag in hashtags:
           node_degree_adjust[hashtag] = 0

       hashtag_edgelist = []
       for i in range(len(hashtags)-1):
           for j in range(i+1, len(hashtags)):
               hashtag1 = hashtags[i]
               hashtag2 = hashtags[j]
               if((not self.ifnewNode(hashtag1)) and (not self.ifnewNode(hashtag2))):
                  hashtag_edgelist.append([hashtag1, hashtag2])


       common_edges = []
       ifnewEdge = False
       for edge in hashtag_edgelist:
           common_nodes = []
           flag = False
           for hashtag_node in self.queue_hist_hashtags:
               rep_nodes = [hashtag for hashtag in edge if hashtag in hashtag_node.hashtags ]
               if len(rep_nodes) == 1:
                  common_nodes.append(rep_nodes[0]) #store repeated nodes
               if len(rep_nodes) == 2: 
                  #repeated edges
                  flag = True
                  common_edges.append(edge)
#                 for rep_node in rep_nodes:
#                   node_degree_adjust[rep_node] = node_degree_adjust[rep_node] - 1
           if not flag and len(set(common_nodes)) > 1:
               node_degree_adjust[edge[0]] = node_degree_adjust[edge[0]] + 1
               node_degree_adjust[edge[1]] = node_degree_adjust[edge[1]] + 1
               ifnewEdge = True
#       for rep_node, value in node_degree_adjust.iteritems():
##           if value < 0:
##               node_degree_adjust[rep_node] = node_degree_adjust[rep_node] + n_neighbor 
#           if len(set(common_nodes)) > 1: 
#               # a new edge whose two ends both appear before but not form a repeated edge
#               if (rep_node in set(common_nodes)) and (rep_node not in set(common_edges)): #(node_degree_adjust[rep_node] == 0):
#                   node_degree_adjust[rep_node] = node_degree_adjust[rep_node] + n_neighbor
#
#
#       for rep_node, value in node_degree_adjust.iteritems():
#           if value > 0:
#               ifnewEdge = True
#               break

       return (node_degree_adjust, ifnewEdge)
#   def check_new_edge(self, hashtags):
#       '''
#            check if a new edge is added in timestamp 
#
#            compare timestamp with queue for both ends  
#       '''
#       ifnewEdge = True
#       for hashtag_node in self.queue_hist_hashtags:
#           temp = [hashtag for hashtag in hashtags if hashtag in hashtag_node.hashtags ]
#           if len(temp) > 2:
#              ifnewEdge = False
#              break
#       return ifnewEdge


   def ifnewNode(self, hashtag):
       try:
           self.hash_nodeDegree[hashtag]
       except KeyError:
           return True
       else: 
           return False


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
           print >> self.outputfile, "{0:.3f}".format(num)
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
    #print("Graph construct")
    #HashGraphObj.graph_construct(inputfile)
    print("Running ... ")
    HashGraphObj.run(inputfile)
    print("Write to " + outputfile)
    HashGraphObj.write_txt(outputfile)




if __name__ == "__main__":
    main(sys.argv[1:])