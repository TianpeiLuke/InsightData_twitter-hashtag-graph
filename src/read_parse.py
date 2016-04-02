import json
import os




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