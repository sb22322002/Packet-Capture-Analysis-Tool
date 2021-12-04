#!/usr/bin/env python3
def compute(data):
    """Calculates three categories of metrics per node: 8 data size metrics,
    4 Time based metrics, and 1 Distance metric
    """

    counter = 0
    node_info = []
    # loop for every list element in list data
    for filedata in data:
        # variables for data size metrics
        sum_echo_requests_sent = 0
        sum_echo_requests_received = 0
        sum_echo_replies_sent = 0
        sum_echo_replies_received = 0
        total_echo_request_bytes_sent = 0
        total_echo_request_bytes_received = 0
        total_echo_request_data_sent = 0
        total_echo_request_data_received = 0

        # variables for sequence information
        seq_num = ""
        seq_time = 0.0

        # variables for RTT
        rtt_total = 0.0
        rtt_pair_count = 0

        # variables for reply delay
        reply_delay_total = 0.0
        reply_delay_pair_count = 0

        # variables for hop count
        request_ttl = 0
        hops = []

        # Node IPs
        ips = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]

        for line in filedata:
            # print(line)           # test to display fields in each line
            # print(len(filedata))  # testing for any loss of data

            # request sent
            if ips[counter] in line[2] and "request" in line[6].split(' ')[2]:
                sum_echo_requests_sent += 1
                total_echo_request_bytes_sent += int(line[5])
                total_echo_request_data_sent += (int(line[5]) - 42)  # subtract the headers

                # NOTE - RTT is specifically averaging time difference in requests sent and replies received
                # request will always be first in a sequence so store sequence number
                seq_num = line[7]
                seq_time = float(line[1])*1000
                request_ttl = int(line[8].split("=")[1].split(" ")[0])

            # request received
            if ips[counter] not in line[2] and "request" in line[6].split(' ')[2]:
                sum_echo_requests_received += 1
                total_echo_request_bytes_received += int(line[5])
                total_echo_request_data_received += (int(line[5]) - 42)  # subtract the headers

                # NOTE - Reply Delay is specifically averaging time difference in requests received and replies sent
                # request will always be first in a sequence so store sequence number
                seq_num = line[7]
                seq_time = float(line[1]) * 1000000

            # reply received
            if ips[counter] not in line[2] and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_received += 1

                # reply will always be second in sequence so pair with matching request and calculate time difference
                if line[7] in seq_num:
                    rtt_pair_count += 1
                    rtt_total += (float(line[1])*1000 - seq_time)
                    # print(str(float(line[1]) * 1000) + " - " + str(seq_time))
                    # print(rtt_total)
                    hops.append(request_ttl - (int(line[8].split("=")[1].split(" ")[0])) + 1)

            # reply sent
            if ips[counter] in line[2] and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_sent += 1

                # reply will always be second in sequence so pair with matching request and calculate time difference
                if line[7] in seq_num:
                    reply_delay_pair_count += 1
                    reply_delay_total += (float(line[1]) * 1000000 - seq_time)
                    # print(str(float(line[1]) * 1000000) + " - " + str(seq_time))
                    # print(rtt_total)

        counter += 1
        rtt = rtt_total / rtt_pair_count
        reply_delay = reply_delay_total / reply_delay_pair_count
        hops_avg = (sum(hops) / len(hops))
        throughput = total_echo_request_bytes_sent / rtt_total
        goodput = total_echo_request_data_sent / rtt_total

        # Add info to node_info list to print out to file later.
        node_info.append([sum_echo_requests_sent, sum_echo_requests_received, sum_echo_replies_sent,
                          sum_echo_replies_received, total_echo_request_bytes_sent, total_echo_request_data_sent,
                          total_echo_request_bytes_received, total_echo_request_data_received, round(rtt, 2),
                          round(throughput, 1), round(goodput, 1), round(reply_delay, 2), round(hops_avg, 2)])

    # Open the output file
    output_file = open('output.csv', "w")

    # Loop through node_info and write each field accordingly
    node_counter = 1
    for node in node_info:
        output_file.write("Node " + str(node_counter) + "\n\n")
        output_file.write("Echo Requests Sent, Echo Requests Received, Echo Replies Sent, Echo Replies Received, \n")
        item = str(node[0]) + "," + str(node[1]) + "," + str(node[2]) + "," + str(node[3]) + "\n"
        output_file.write(item)
        output_file.write("Echo Request Bytes Sent (bytes), Echo Request Data Sent (bytes)\n")
        item = str(node[4]) + "," + str(node[5]) + "\n"
        output_file.write(item)
        output_file.write("Echo Request Bytes Received (bytes), Echo Request Data Received (Bytes)\n")
        item = str(node[6]) + "," + str(node[7]) + "\n\n"
        output_file.write(item)
        item = "Average RTT (milliseconds)," + str(node[8]) + "\n"
        output_file.write(item)
        item = "Echo Request Throughput (kB/sec)," + str(node[9]) + "\n"
        output_file.write(item)
        item = "Echo Request Goodput (kB/sec)," + str(node[10]) + "\n"
        output_file.write(item)
        item = "Average Reply Delay (microseconds)," + str(node[11]) + "\n"
        output_file.write(item)
        item = "Average Echo Request Hop Count," + str(node[12]) + "\n\n"
        output_file.write(item)

        node_counter += 1

    # Close output file
    output_file.close()
