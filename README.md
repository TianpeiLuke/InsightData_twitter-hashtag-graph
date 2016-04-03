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
  * How to compute the average degree ?
    - Done. Maintain num_nodes and num_total_degree. Then their ratio is the result
  * How to read and save to text via command line ?
    - Done. Using getopt package in python. 
  * How to determine the time slot ?
  * How to maintain data within a 60s time window ? 
  * How to deal with out of order tweets ?

## Graph structure 
To save for memeory, we store all degree information in hash table of nodes. Also, note that all hashtags in one tweet form a fully connected graph. We can judge from the node list if an edge is present. 

For graph growing, we disucss cases as below:
  * If new node is present in a tweet, for all hashtag nodes in given tweet 
     - If the node appears before, its degree will increase by the number of new nodes. Since they only need to add edges 
     - If it is a new node, its degree is the total number of hashtags in given tweet minus one. (degree of a fully connected graph)


