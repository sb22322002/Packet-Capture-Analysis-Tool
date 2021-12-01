def compute(data) :
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
		for line in filedata:
			print(line)

			if(line[2] == "192.168.100.1" and line[6].split(' ')[2] == "request"):
				sum_echo_requests_sent += 1
				total_echo_request_bytes_sent += int(line[5])
			if (line[2] == "192.168.100.2" and line[6].split(' ')[2] == "reply"):
				sum_echo_replies_sent += 1
				total_echo_request_bytes_received += int(line[5])

			sum_frame += line[5]

			counter += 1

		print("Total requests: " + str(sum_echo_requests_sent))
		print("Total replies: " + str(sum_echo_replies_sent))
		print("Total Echo Request Bytes Sent: " + str(total_echo_request_bytes_sent))
		print("Total Echo Request Bytes Recieved: " + str(total_echo_request_bytes_received))
		print("End of a node")


def data_size(line):
	print("")

def time_metrics(line):
	print('Average ping round trip time (RTT), echo request throughput, echo request goodput, average reply delay')

def distance_metric(line):
	print('Average number of hops per request')

