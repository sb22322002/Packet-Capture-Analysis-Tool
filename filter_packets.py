#!/usr/bin/env python3
import contextlib


def filter():
    """Filters the raw text files so that only ICMP Echo Request and ICMP Echo Reply packets remain.
    This filtered data is redirected to _filtered.txt files for each raw text file
    """

    count = 1
    f1 = open("Node1.txt", "r")
    f2 = open("Node2.txt", "r")
    f3 = open("Node3.txt", "r")
    f4 = open("Node4.txt", "r")
    # place all files into a list for convenience
    files = [f1, f2, f3, f4]

    # loop for every file in list
    for i in files:
        # create an emtpy text file to store filtered data
        new_file = "Node" + str(count) + "_filtered.txt"
        nf = open(new_file, "w")
        nf.close()
        # read each file line by line
        for line in i:
            # search for headers containing ICMP and Echo (ping)
            if "ICMP" and "Echo (ping)" in line:
                # redirect all stout to _filtered text file using contextlib
                with open(new_file, 'a') as f:
                    with contextlib.redirect_stdout(f):
                        # print formatted header
                        print("No.".ljust(8) + "Time".ljust(15) + "Source".ljust(22) + "Destination".ljust(
                            22) + "Protocol Length Info")
                        # print header info
                        print(line, end="")
                        while "No." not in line:
                            # print each line until a new frame is read
                            line = i.readline()
                            if "No." not in line:
                                print(line, end="")
        count += 1  # increment count for new_file name
    # print(count)  # test to make sure all files were read
