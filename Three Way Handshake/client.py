import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Template sequence number
SEQ = 1

def ThreeWayHandshakeClient():
    # Connect to server
    s.connect((socket.gethostname(), 1234))

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
ThreeWayHandshakeClient()
s.close()