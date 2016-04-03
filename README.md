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
  * For all hashtag nodes in a given tweet 
     - If this is a new node, its degree is the total number of hashtags in given tweet minus one. (degree of a fully connected graph)
     - If this node appears before, its degree increment includes two parts:
          1. The edges that connect to the new node. This part of degree increase is the number of new nodes.
          2. The edges that connect to an existing node. However, this edge does not appear in graph. In other word, the two end-nodes do not co-exist in previous tweets. This is the second part. 
          3. The edges that connect to an existing node. Also, this edge appear in the graph. Or, the two end-nodes co-exist in one of the previous tweets. 

For graph pruning, we discuss cases as below:
   * At each step of graph growing, record the edge increase and the time into history FIFO queue. The top of the queue is the oldest step operations
   * Retrieve the time, if the time is out of current maximum timestamp - 60, pop the history queue, and reverse the corresponding operations.
