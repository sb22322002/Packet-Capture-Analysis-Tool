from typing import Any


def compute(data):
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

        for line in filedata:

            if 'request' in line[6]:
                time1 = float(line[1])
                print("request: " + str(line[1]) + " seq: " + line[7])
                print(line)
                seq = line[7]
                for line2 in filedata:
                    rtt = 0
                    if 'reply' in line2[6] and line2[7] == seq:
                        time2 = float(line2[1])
                        print("reply: " + str(line2[1]) + " seq: " + line2[7])
                        print(line2)
                        rtt = time2 - time1
                        print("rtt: " + str(rtt))
                        counter += 1
                        sum_rtt += rtt
                        break
                        # print(counter)

                #print(sum_rtt)
                #break


        trtt = (sum_rtt / counter)
        print(trtt)
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
        #print("Average RTT (ms) " + str(avg_rtt))
        print("End of a node")
        break
