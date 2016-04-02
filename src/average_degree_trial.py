# -*- coding: utf-8 -*-
import os, sys
import json

class HashtagDegree:
'''

    This is the main class that contains Hashtags Graph
'''

   def __init__(self, filename):
       self.file_open(filename)
       self.node_hash = []
       hashtag_one_tweet, created_at_one_tweet  = read_tweet_one(self.txtfile)


   def file_open(self, filename):
       with open(filename) as txtfile:
            self.txtfile = txtfile
            return True
       except:
            print 'open textfile failure'
            return False

   def file_close(self):
       self.txtfile.close()

   



def read_tweet_one(txtfile):
    '''
       Read one line of the tweet.txt file and parse it by json·
       The extracted "created_at" and "hashtags" are returned
       txtfile is the file handle created before calling the function

    '''
    #with open(filename) as txtfile: 
    tweet_line = txtfile.readline().replace('\n','')
    jsonObj = json.loads(tweet_line)
    created_at = jsonObj.get("created_at")
    hashtag_list = jsonObj.get("entities").get("hashtags")
    hashtag_txt_list = [ hashtag_list[i].get('text') for i in range(len(hashtag_list)) ]

    return (hashtag_txt_list, created_at)