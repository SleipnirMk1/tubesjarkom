import socket
import argparse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Template sequence number
SEQ = 1

# Argument Parser
parser = argparse.ArgumentParser(description="Client")
parser.add_argument("port", type=int, help="Client port")
parser.add_argument("path", type=str, help="Path penyimpanan berkas")
args = parser.parse_args()
port = args.port
path = args.path

def ThreeWayHandshakeClient():

    # Send SYN
    print("Three Way Handshake client start")
    print("Sending SYN")
    s.send(("SYN: {}".format(SEQ)).encode("utf-8"))

    # Receive SYN-ACK
    SYNACK = s.recv(1024)
    print("Receiving SYN-ACK")

    # Decode SYN-ACK
    receive = SYNACK.decode('utf-8')
    receive_arr = [int(i) for i in receive.split() if i.isdigit()]

    SYN = receive_arr[0]
    ACK = receive_arr[1]
    print("SYN: {}, ACK: {}".format(SYN, ACK))

    # Send ACK
    print("Sending ACK")
    ACK = SYN + 1
    s.send(("ACK: {}".format(ACK)).encode("utf-8"))

    # Done
    print("Three Way Handshake client done")
    
# Testing
# Connect to server
s.connect((socket.gethostname(), port))
ThreeWayHandshakeClient()
s.close() # Hapus close nya nanti