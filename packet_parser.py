#!/usr/bin/env python3
from filter_packets import *

# taking file that needs to be parsed and outputting parsed list
def parse(fileName, list):
    filtered = open(fileName, "r")
    line = filtered.readline()

    while line:
        list.append(line.strip().split())
        line = filtered.readline()

    filtered.close()

# calling filtered function from filter_packets
filter()

# redirecting parsed data to list for each filtered file
list1 = []
list2 = []
list3 = []
list4 = []

parse("Node1_filtered.txt", list1)
parse("Node2_filtered.txt", list2)
parse("Node3_filtered.txt", list3)
parse("Node4_filtered.txt", list4)

	
