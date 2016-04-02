# -*- coding: utf-8 -*-
from __future__ import with_statement
import os, sys
import json
import getopt

class HashtagDegree:
   '''
    This is the main class that contains Hashtags Graph
   '''
   def __init__(self):
       self.num_node = 0
       self.total_degree = 0
       self.nodeDegree_hash = []
       self.nodeTime_hash = []
       self.output = []

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
           hashtag_one_tweet, created_at_one_tweet  = parse_tweet(tweet_line)
       
       #add code here
       


   def graph_grow(self):
       '''
       
       ''' 
       #add code here
       return

   def graph_prune(self, time_stamp):
       return

   def check_new_node(self, list_hashtag):
       return True

   def inputfile_open(self, input_filename):
       try:
            self.inputfile = open(input_filename)
       except EnvironmentError:
            print 'open inputfile failure'

   def outputfile_open(self, output_filename):
       try:
            self.outputfile = open(output_filename)
       except EnvironmentError:
            print 'open outputfile failure'

   def write_txt(self, output_filename):
       self.outputfile_open(output_filename)
       #add code here

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
    HashGraphObj = HashtagDegree()
    #print("Graph construct")
    #HashGraphObj.graph_construct(inputfile)
    print("Running ... ")
    HashGraphObj.run(inputfile)
    print("Write to " + outputfile)
    HashGraphObj.write_txt(outputfile)
    HashGraphObj.file_close()




if __name__ == "__main__":
    main(sys.argv[1:])