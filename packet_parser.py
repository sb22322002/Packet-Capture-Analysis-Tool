#!/usr/bin/env python3
import re


# Create_list - Takes in the string of data and returns a list of separate fields
def create_list(data):
    # split comma separated string into separate variables
    number = data.split(' ')[0]
    time = data.split(' ')[1]
    source = data.split(' ')[2]
    destination = data.split(' ')[3]
    protocol = data.split(' ')[4]
    length = data.split(' ')[5]

    type_holder = data.split(',')[0].split(' ')[6:]
    type = ""
    # loop to split Info field
    for field in type_holder:
        type += field + " "

    seq = data.split(',')[1]
    ttl = data.split(',')[2]

    # return statement
    return [number, time, source, destination, protocol, length, type, seq, ttl]


def parse():
    """Parses the filtered raw text files and reads packet fields from the summary line into memory. These fields will
    be used when computing metrics
    """

    f1 = open("Node1_filtered.txt", "r")
    f2 = open("Node2_filtered.txt", "r")
    f3 = open("Node3_filtered.txt", "r")
    f4 = open("Node4_filtered.txt", "r")
    # place all filtered files into a list for convenience
    files = [f1, f2, f3, f4]
    # create an empty list that will store a list of file data for every file
    big_list = []

    # loop for every file in list
    for i in files:
        ls = []
        # read each file line by line
        for line in i:
            # if the line is a header read the next line which will always be the summary line
            if "No." in line:
                line = i.readline()
                # format the summary line into a comma separated string
                new = re.sub("\s+", " ", line.strip())
                # call the create_list function and store result in ls
                ls.append(create_list(new))
        # store list of all data from file into big_list
        big_list.append(ls)

    return big_list
