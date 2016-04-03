import json
import os

 def graph_grow(hashtags, num_nodes, num_total_degree, hash_nodeDegree):
    if len(hashtags) == 1:
        return (num_nodes, num_total_degree, hash_nodeDegree)
    num_newnodes = len(set(hashtags)-set(hash_nodeDegree.keys()))
    if num_newnodes == 0:
        return (num_nodes, num_total_degree, hash_nodeDegree)
    num_nodes = num_nodes + num_newnodes
    for hashtag in hashtags:
        try:
            hash_nodeDegree[hashtag] = hash_nodeDegree[hashtag] + num_newnodes
        except KeyError:    
            hash_nodeDegree[hashtag] = len(hashtags) - 1
            num_total_degree = num_total_degree + len(hashtags) - 1
        else:    
            num_total_degree = num_total_degree + num_newnodes
    return (num_nodes, num_total_degree, hash_nodeDegree)


def read_tweet_one(txtfile):
    '''
        Read one line of the tweet.txt file and parse it by json 
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