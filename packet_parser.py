import re

# !/usr/bin/env python3
# taking file that needs to be parsed and outputting parsed list
def parse():
    f1 = open("Node1_filtered.txt", "r")
    f2 = open("Node2_filtered.txt", "r")
    f3 = open("Node3_filtered.txt", "r")
    f4 = open("Node4_filtered.txt", "r")
    files = [f1, f2, f3, f4]
    big_list = []

    for i in files:
        ls = []
        for line in i:
            if "No." in line:
                line = i.readline()
                new = re.sub("\s+", " ", line.strip())
                ls.append(new)
    print(ls)
    big_list.append(ls)
    return big_list

parse()

