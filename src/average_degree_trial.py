# -*- coding: utf-8 -*-
from __future__ import with_statement
import os, sys
import json
import getopt
from dateutil.parser import parse
from datetime import datetime,timedelta

class HashtagGraph:
   '''

      This is the main class that contains Hashtags Graph
   '''
   def __init__(self):
       self.num_nodes = 0
       self.num_total_degree = 0
       self.hash_nodeDegree = {}
       self.hash_nodeTime = {}
       self.list_avg_Degree = []

#   def graph_construct(self, input_filename):
#       self.inputfile_open(input_filename)
#       #read the first tweet and construct the graph
#       tweet_line = self.inputfile.readline().replace('\n','')
#       hashtag_one_tweet, created_at_one_tweet  = parse_tweet(tweet_line)
#       #add code here


   def run(self, input_filename):
       '''
     
        This is the interface for running the graph_grow and graph_prune
       '''
       self.inputfile_open(input_filename)
       for tweet_line in self.inputfile:
           # parse tweet line
           hashtags, created_ats = parse_tweet(tweet_line)
           # grow graph
           self.graph_grow(hashtags)
           self.list_avg_Degree.append(float(self.num_total_degree) / float(self.num_nodes))
           #add code here
       


   def graph_grow(self, hashtags):
       '''

          use the hash table to store the total degree for each hashtag
          modify the graph strcture for each given list of hashtags
       ''' 
       #add code here
       if len(hashtags) == 1:
           #drop single hashtag
           return 
       
       num_newnodes = self.count_new_nodes(hashtags)
       if num_newnodes == 0:
          return

       print("Add {0:3d} nodes".format(num_newnodes))
       self.num_nodes = self.num_nodes + num_newnodes
       for hashtag in hashtags:
           try: 
               self.hash_nodeDegree[hashtag] = self.hash_nodeDegree[hashtag] + num_newnodes 
           except KeyError:
               self.hash_nodeDegree[hashtag] = len(hashtags) - 1
               self.num_total_degree = self.num_total_degree + len(hashtags) - 1 
           else:
               self.num_total_degree = self.num_total_degree + num_newnodes
       return

   def graph_prune(self, time_stamp):
       return

   def count_new_nodes(self, hashtags):
       '''

          count number of new nodes in hashtag list
       '''
       num_newnodes = 0
       if len(hashtags) == 1:
           #drop single hashtag
           return num_newnodes
       node_keys = self.hash_nodeDegree.keys() 
       num_newnodes = len(set(hashtags) - set(node_keys) )
       return num_newnodes

   def inputfile_open(self, input_filename):
       try:
            self.inputfile = open(input_filename , 'r' )
       except EnvironmentError:
            print 'open inputfile failure'

   def outputfile_open(self, output_filename):
       try:
            open(output_filename,"w").close()
       except EnvironmentError:
            print 'open outputfile failure'
       else:
            self.outputfile = open(output_filename , 'w')


   def write_txt(self, output_filename):
       '''

            Write to given file
       '''
       self.outputfile_open(output_filename)
       #self.outputfile.write("\n".join(str(self.list_avg_Degree)))
       for num in self.list_avg_Degree:
            print >> self.outputfile, "{0:.3f}\n".format(num)


   def file_close(self):
       self.inputfile.close()
       self.outputfile.close()

   

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
    HashGraphObj.file_close()




if __name__ == "__main__":
    main(sys.argv[1:])