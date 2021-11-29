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

# test
filter()
file = "Node1_filtered.txt"
l = []
parse(file, l)
print(l)

	
