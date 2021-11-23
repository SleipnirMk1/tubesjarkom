import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(2) # Listen for up to 2 clients

# Template sequence number
SEQ = 5

def ThreeWayHandshakeServer():
    # Accept client connection
    clientsocket, address = s.accept()
    print("Connection from {} estabished".format(address))

    # Receive SYN
    print("Three Way Handshake server start")
    SYN = clientsocket.recv(1024)
    print("Receiving SYN")

    # Decode SYN
    receive = SYN.decode('utf-8')
    receive_arr = [int(i) for i in receive.split() if i.isdigit()]
    SYN = receive_arr[0]
    print("SYN: ", SYN)

    # Send SYN-ACK
    print("Sending SYN-ACK")
    ACK = SYN + 1
    clientsocket.send(("SYN: {} , ACK: {}".format(SEQ,ACK)).encode("utf-8"))

    # Receive ACK
    ACK = clientsocket.recv(1024)
    print("Receiving ACK")

    # Decode ACK
    receive = ACK.decode('utf-8')
    receive_arr = [int(i) for i in receive.split() if i.isdigit()]
    ACK = receive_arr[0]
    print("ACK: ", ACK)
    
    # Done
    print("Three Way Handshake server done")
    clientsocket.close()

# Testing
# Start server
print("Server start")

# Always listen
while True:
    ThreeWayHandshakeServer()