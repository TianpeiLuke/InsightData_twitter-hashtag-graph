#!/usr/bin/env bash

# example of the run script for running the word count

# I'll execute my programs, with the input directory tweet_input and output the files in the directory tweet_output
#echo "Type the input file name under './tweet_input/':"
#read input_file

#echo "Type the output file name under './tweet_output/':"
#read output_file

echo "Type [n] for the naive implementation or [h] for the hash implmentation, followed by [ENTER]:"

read choice

if [ $choice == n ]; then
   echo "Naive implementation"
   time python ./src/average_degree_naive.py -i ./tweet_input/tweets.txt -o ./tweet_output/output.txt
elif [ $choice == h ]; then
   echo "Hash-table implementation"
   time python ./src/average_degree_hash.py -i ./tweet_input/tweets.txt -o ./tweet_output/output.txt
else
   echo "Choose [n] or [h]"
fi 




