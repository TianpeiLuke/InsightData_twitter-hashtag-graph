# Insight Data Challenge
This is for Insight Data Challenge. Created by Tianpei Xie. 

## Overview
I implemented two methods. The naive implementation 'average\_degree\_naive.py' and the hash-table implemenation 'average\_degree\_hash.py'.

### Naive implementation
The naive implementation computes the total number of degrees as the twice of the total number of the edges. Since all hashtags in a tweet form a complete graph, it uses the 'edge\_update' function to compute the size of edges in an union of $n$ complete graphs. This function uses the inclusion-exclusion principle to compute the union of n graphs as the union of new graph and the existing graph. It requies recursively compute the intersection of new graph with each graph formed by the previous hashtags 

It uses the fact that the intersection of $n$ complete graphs is a complete graph with node as the intersection of all nodes. And the number of edges for a complete graph is $p(p-1)/2$ for $p$ as the number of nodes. The algorithm is implemented naively using the recursion. The complexity is exponential in size of tweets within the window

### Hash-table implementation
The hash-table implementation does not compute the edges. It maintained a hash-table of nodes with its node degree. It is efficient in storage, when the total number of nodes increases. Also it handles the graph growing procedure locally for each node. 


For graph growing, it distinguishes different cases as below:
  * For all hashtag nodes in a given tweet 
     - If this is a new node, its degree is the total number of hashtags in given tweet minus one. (degree of a fully connected graph)
     - If this node appears before, its degree increment includes two parts:
          1. The edges that connect to the new node. This part of degree increase is the number of new nodes.
          2. The edges that connect to an existing node that also in the same tweet. However, this edge does not appear in graph. In other word, the two end-nodes do not co-exist in previous tweets. This is the second part. 
          3. The edges that connect to an existing node in same tweet and this edge appear in the graph. Or, the two end-nodes co-exist in one of the previous tweets.  This part should not be included
      - As discussed above, for node appears before, we first add the the total number of hashtags minus one. Then we find those previous records in which at least two nodes are common with one of them the given node. We delete the number of common nodes minus one as the redundant degree. 
  *  I use a queue to maintain the sequence of input hashtags as well as its created time for time-window maintainance.  

For graph pruning, I simply delete the record in history queue. And refresh the status variables such as node\_list, node\_degree, and rebuild the graph squentially using the existing history record. That is not efficient, but easy to implement. 

Note that since the graph growing prcedure just take care of the new nodes and nodes that are shared between new graph and old graph. It is more efficient.

## Checklist 
The key to solve the degree counting problem is to answer the following questions:
  * How to extract "Created Time", "Hashtag" from a given tweet ? 
    - Done. See 'read\_parse.py' file
  * How to store the node degrees ?
    - Done. Using Hash table (dictionary in Python)
  * How to determine if a node is added to the graph ?
    - Done. Using the KeyError exception for visit the hash node 
  * How to compute the average degree ?
    - Done. Maintain num\_nodes and num\_total\_degree. Then their ratio is the result
  * How to read and save to text via command line ?
    - Done. Using getopt package in python. 
  * How to determine the time slot ?
    - Done. Using the maximum\_timestamp.
  * How to maintain data within a 60s time window ? 
    - Done. Compare with teh maximum\_timestamp.
  * How to deal with out of order tweets ?
    - Done. Just drop it.

