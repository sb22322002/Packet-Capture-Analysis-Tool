import re

# !/usr/bin/env python3
# taking file that needs to be parsed and outputting parsed list

# Create_list - Takes in the string of data and separates it into a list
def create_list(data):
    number = data.split(' ')[0]
    time = data.split(' ')[1]
    source = data.split(' ')[2]
    destination = data.split(' ')[3]
    protocol = data.split(' ')[4]
    length = data.split(' ')[5]

    type_holder = data.split(',')[0].split(' ')[6:]
    type = ""
    for field in type_holder:
            type += field + " "

    seq = data.split(',')[1]
    ttl = data.split(',')[2]

    return [number, time, source, destination, protocol, length, type, seq, ttl]

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
                ls.append(create_list(new))
        big_list.append(ls)

    return big_list


