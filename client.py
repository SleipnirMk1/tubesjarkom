import socket
import sys

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = "127.0.0.1"
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Template sequence number, ganti jadi pake segment
SEQ = 1

# Argument Parser
args_list = (str(sys.argv))
port = int(sys.argv[1])
path = args_list[2]

def ThreeWayHandshakeClient():
    # Send SYN
    print("Three Way Handshake client start")
    print("Sending SYN")
    msg = str(SEQ)
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

    # Receive SYN-ACK
    SYNACK = UDPClientSocket.recvfrom(bufferSize)
    print("Receiving SYN-ACK")

    # Decode SYN-ACK
    receive = SYNACK[0]
    receive_arr = [int(i) for i in receive.split() if i.isdigit()]

    SYN = receive_arr[0]
    ACK = receive_arr[1]
    print("SYN: {}, ACK: {}".format(SYN, ACK))

    # Send ACK
    print("Sending ACK")
    ACK = SYN + 1
    msg = str(ACK)
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

    # Done
    print("Three Way Handshake client done")

# Testing
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, (serverAddressPort, port))

# Handshake
print("Waiting to start handshake")
start_handshake, addr = UDPClientSocket.recvfrom(bufferSize)
ThreeWayHandshakeClient()