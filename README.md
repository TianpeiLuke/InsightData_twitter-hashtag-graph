# Insight Data Challenge
This is for Insight Data Challenge. Created by Tianpei Xie. 

## Solution strategy 
The key to solve the degree counting problem is to answer the following questions:
  * How to extract "Created Time", "Hashtag" from a given tweet ? 
    - Done. See read_parse.py file
  * How to store the node degrees ?
    - Done. Using Hash table (dictionary in Python)
  * How to determine if a node is added to the graph ?
    - Done. Using the KeyError exception for visit the hash node 
  * How to determine the time slot ?
  * How to maintain data within a 60s time window ? 
  * How to deal with out of order tweets ?
