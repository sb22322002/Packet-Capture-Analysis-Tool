from typing import Any


def compute(data):
    node_info = []

    for filedata in data:
        sum_echo_requests_sent = 0
        sum_echo_requests_received = 0
        sum_echo_replies_sent = 0
        sum_echo_replies_received = 0
        total_echo_request_bytes_sent = 0
        total_echo_request_bytes_received = 0
        total_echo_request_data_sent = 0
        total_echo_request_data_received = 0

        sum_frame = 0
        sum_rtt = 0
        counter = 0

        src_time = 0
        destination_time = 0

        current_sequence = ""
        for line in filedata:
            # print(line)
            # print(len(filedata))

            if "192.168.100.1" in line[2] and line[6].split(' ')[2] == "request":
                sum_echo_requests_sent += 1
                total_echo_request_bytes_sent += int(line[5])
                total_echo_request_data_sent += (int(line[5]) - 42) # subtract the headers

                current_sequence = line[7]
                src_time = float(line[1])
            if line[2] == "192.168.100.1" and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_sent += 1
            if "192.168.100.1" not in line[2] and "request" in line[6].split(' ')[2]:
                sum_echo_requests_received += 1
                total_echo_request_bytes_received += int(line[5])
                total_echo_request_data_received += (int(line[5]) - 42) # subtract the headers

            if "192.168.100.1" not in line[2] and "reply" in line[6].split(' ')[2]:
                sum_echo_replies_received += 1

                #if (line[7] == current_sequence):
                    #sum_rtt += float(line[1]) / src_time

        hops = []
        for line in filedata:

            if 'request' in line[6]:
                time1 = float(line[1])
                #print("request: " + str(line[1]) + " seq: " + line[7])
                #print(line)
                seq = line[7]

                request_ttl = line[8].split('=')[1].split(" ")[0]
                for line2 in filedata:
                    rtt = 0
                    if 'reply' in line2[6] and line2[7] == seq:
                        time2 = float(line2[1])
                        #print("reply: " + str(line2[1]) + " seq: " + line2[7])
                        rtt = time2 - time1
                        #print("rtt: " + str(rtt))
                        counter += 1
                        sum_rtt += rtt

                        reply_ttl = line2[8].split('=')[1].split(" ")[0]
                        current_hops = (int(request_ttl) - int(reply_ttl)) + 1
                        hops.append(current_hops)
                        # print(counter)


                #print(sum_rtt)
                #break

        print("Sum rtt: " + str(sum_rtt))
        avg_rtt = (sum_rtt / counter) * 1000
        print("Average RTT: " + str(avg_rtt))

        throughput = (total_echo_request_bytes_sent / sum_rtt) / 1000
        goodput = (sum_echo_requests_sent / sum_rtt) / 1000

        avg_delay = (sum_rtt / counter) * 1000000 # I think... (time of reply - time of request) / counter (num of exchanges) * 1000000

        avg_hops = sum(hops) / len(hops)

        #print(sum_rtt)
        #avg_rtt = sum_rtt/counter

        print("Total requests sent: " + str(sum_echo_requests_sent))
        print("Total replies sent: " + str(sum_echo_replies_sent))
        print("Total requests received: " + str(sum_echo_requests_received))
        print("Total replies received: " + str(sum_echo_replies_received))
        print("Total Echo Request Bytes Sent: " + str(total_echo_request_bytes_sent))
        print("Total Echo Request Bytes Recieved: " + str(total_echo_request_bytes_received))
        print("Total Echo Request Data Sent: " + str(total_echo_request_data_sent))
        print("Total Echo Request Data Recieved: " + str(total_echo_request_data_received))
        print("Average RTT (ms): " + str(avg_rtt))
        print("Echo Request Throughput (kB/sec): " + str(throughput))
        print("Echo Request Goodput (kB/sec): " + str(goodput))
        print("Average Reply Delay (us): " + str(avg_delay))
        print("Average Echo Request Hop Count: " + str(avg_hops))

        node_info.append([sum_echo_requests_sent, sum_echo_requests_received, sum_echo_replies_sent, sum_echo_replies_received, total_echo_request_bytes_sent, total_echo_request_data_sent, total_echo_request_bytes_received, total_echo_request_data_received, avg_rtt, throughput, goodput, avg_delay, avg_hops])
        print("End of a node")
        break

    output_file = open('output.csv', "w")

    node_counter = 1
    for node in node_info:
        output_file.write("Node " + str(node_counter) + "\n\n")
        output_file.write("Echo Requests Sent, Echo Requests Recieved, Echo Replies Sent, Echo Replies Recieved, \n")
        item = str(node[0]) + "," + str(node[1]) + "," + str(node[2]) + "," + str(node[3]) + "\n"
        output_file.write(item)
        output_file.write("Echo Request Bytes Sent (bytes), Echo Request Data Sent (bytes)\n")
        item = str(node[4]) + "," + str(node[5]) + "\n"
        output_file.write(item)
        output_file.write("Echo Request Bytes Recived (bytes), Echo Request Data Recieved (Bytes)\n")
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
        item = "Average Echo Request Hop Count," + str(node[12]) + "\n"
        output_file.write(item)

    output_file.close()
