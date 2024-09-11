import base64
import socket
import sys
import time

# This script reproduces Apache TrafficServer blind tunneling bug

# A client hello packet captured from a real client with WireShark
# The client hello packet has key material as required by Kyber cipher

clienthello_b64 = "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"

clienthello = base64.b64decode(clienthello_b64, validate=True)

split_size = 1100

# Split the client hello into split_size parts
clienthello_split = [clienthello[i:i+split_size] for i in range(0, len(clienthello), split_size)]

def tcp_send_clienthello(dest_host, split=False):
    print("Sending ClientHello to " + dest_host + " in split mode: " + str(split))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((dest_host,443))
    if (split):
        for i in range(0, len(clienthello_split)):
            s.send(clienthello_split[i])
            time.sleep(0.05)
    else:
        s.send(clienthello)
    try:
        buff = s.recv(10240)
    except:
        print("No response received.")
        sys.exit(1)
    s.close()
    print("Response received.")

if len(sys.argv) < 2:
    print("Please provide destination address.")
    sys.exit(1)

# Get the command line argument
dest_host = sys.argv[1]

# Perform some action based on the argument
tcp_send_clienthello(dest_host, split=False)
tcp_send_clienthello(dest_host, split=True)
