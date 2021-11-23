import socket
import argparse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Template sequence number
SEQ = 5

# Argument Parser
parser = argparse.ArgumentParser(description="Server")
parser.add_argument("port", type=int, help="Server port")    # variable name = port
parser.add_argument("path", type=str, help="Path berkas")    # variable name = path
args = parser.parse_args()
port = args.port
path = args.path

s.bind((socket.gethostname(), port))
s.listen(2) # Listen for up to 2 clients

# List of clients
client_list = []

def Listen():
    # Listen for first client
    clientsocket, address = s.accept()
    print("[!] Connection from {} estabished".format(address))
    client_list.append(clientsocket)

    # Ask if listen for more
    listen_more = input("[?] Listen more? (y/n): ")
    if listen_more == "n":
        listen_more = False
        
    # Listen for more clients
    while listen_more:
        clientsocket, address = s.accept()
        print("Connection from {} estabished".format(address))
        client_list.append(clientsocket)
        listen_more = input("[?] Listen more? (y/n): ")
        if listen_more == "n":
            listen_more = False

    print("{} Clients found:".format(len(client_list)))
    for i in range(len(client_list)-1):
        print("{}. {}".format(i+1, client_list[i]))

def ThreeWayHandshakeServer(clientsocket):

    print("Three Way Handshake server start with {}".format(clientsocket))

    # Receive SYN
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
    print("Three Way Handshake server done with {}".format(clientsocket))

    # Close connection, nanti hapus
    clientsocket.close()

# Testing
# Start server
print("Server start at port {}".format(port))
print("Listening to broadcast address for clients")

Listen()
for client in client_list:
    ThreeWayHandshakeServer(client)