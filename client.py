import socket
import sys
from segment import Segment

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = "127.0.0.1"
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Argument Parser
args_list = (str(sys.argv))
port = int(sys.argv[1])
path = args_list[2]

def ThreeWayHandshakeClient():
    # Send SYN
    print("Three Way Handshake client start")
    print("Sending SYN")
    # SYN Segment
    msg = Segment()
    msg.set_flag("SYN")
    bytesToSend = msg.get_bytes()
    UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

    # Receive SYN-ACK
    SYNACK, address = UDPClientSocket.recvfrom(bufferSize)
    # Decode SYN-ACK
    msg = Segment()
    msg.load_segmentation(SYNACK)
    if msg.get_flag_type() == "SYN-ACK":
        print("SYN-ACK Received")
    else:
        return False    # Kalau gagal

    # Send ACK
    print("Sending ACK")
    # ACK Segment
    msg = Segment()
    msg.set_flag("ACK")
    bytesToSend = msg.get_bytes()
    UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

    # Done
    print("Three Way Handshake client done")

    return True

# Testing
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

# Handshake
print("Waiting to start handshake")
start_handshake, addr = UDPClientSocket.recvfrom(bufferSize)
ThreeWayHandshakeClient()