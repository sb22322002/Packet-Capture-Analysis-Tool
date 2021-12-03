#!/usr/bin/env python3
def compute(data):
    """Calculates three categories of metrics per node: 8 data size metrics,
    4 Time based metrics, and 1 Distance metric
    """

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

        for line in filedata:
            # print(line)           # test to display fields in each line
            # print(len(filedata))  # testing for any loss of data

            # request sent
            if "192.168.100.1" in line[2] and "request" in line[6].split(' ')[2]:
                sum_echo_requests_sent += 1
                total_echo_request_bytes_sent += int(line[5])
                total_echo_request_data_sent += (int(line[5]) - 42)  # subtract the headers

                # NOTE - RTT is specifically averaging time difference in requests sent and replies received
                # request will always be first in a sequence so store sequence number
                seq_num = line[7]
                seq_time = float(line[1])*1000
                request_ttl = int(line[8].split("=")[1].split(" ")[0])

            # request received
            if "192.168.100.1" not in line[2] and "request" in line[6].split(' ')[2]:
                sum_echo_requests_received += 1
                total_echo_request_bytes_received += int(line[5])
                total_echo_request_data_received += (int(line[5]) - 42)  # subtract the headers

                # NOTE - Reply Delay is specifically averaging time difference in requests received and replies sent
                # request will always be first in a sequence so store sequence number
                seq_num = line[7]
                seq_time = float(line[1]) * 1000000

            # reply received
            if "192.168.100.1" not in line[2] and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_received += 1

                # reply will always be second in sequence so pair with matching request and calculate time difference
                if line[7] in seq_num:
                    rtt_pair_count += 1
                    rtt_total += (float(line[1])*1000 - seq_time)
                    # print(str(float(line[1]) * 1000) + " - " + str(seq_time))
                    # print(rtt_total)
                    hops.append(request_ttl - (int(line[8].split("=")[1].split(" ")[0])) + 1)

            # reply sent
            if "192.168.100.1" in line[2] and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_sent += 1

                # reply will always be second in sequence so pair with matching request and calculate time difference
                if line[7] in seq_num:
                    reply_delay_pair_count += 1
                    reply_delay_total += (float(line[1]) * 1000000 - seq_time)
                    # print(str(float(line[1]) * 1000000) + " - " + str(seq_time))
                    # print(rtt_total)

        rtt = rtt_total / rtt_pair_count
        reply_delay = reply_delay_total / reply_delay_pair_count
        hops_avg = (sum(hops) / len(hops))
        throughput = total_echo_request_bytes_sent / rtt_total
        goodput = total_echo_request_data_sent / rtt_total

        # print results
        print("Total requests sent: " + str(sum_echo_requests_sent))
        print("Total replies sent: " + str(sum_echo_replies_sent))
        print("Total requests received: " + str(sum_echo_requests_received))
        print("Total replies received: " + str(sum_echo_replies_received))
        print("Total Echo Request Bytes Sent: " + str(total_echo_request_bytes_sent))
        print("Total Echo Request Bytes Received: " + str(total_echo_request_bytes_received))
        print("Total Echo Request Data Sent: " + str(total_echo_request_data_sent))
        print("Total Echo Request Data Received: " + str(total_echo_request_data_received))
        print()
        print("Average RTT (ms): " + str(round(rtt, 2)))
        print("Echo Request Throughput (kB/sec): " + str(round(throughput, 1)))
        print("Echo Request Goodput (kB/sec): " + str(round(goodput, 1)))
        print("Average Reply Delay (μs): " + str(round(reply_delay, 2)))
        print()
        print("Average Echo Request Hop Count: " + str(round(hops_avg, 2)))
        print("End of a node\n")

#########################################################
# Results for Node 1 should be working I'm going to bed
# https://c.tenor.com/m4DT6JjGu7sAAAAM/boogie-dance.gif
#########################################################
