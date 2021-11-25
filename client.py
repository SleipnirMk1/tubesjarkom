import socket
import sys
from segment import Segment

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8000)
bufferSize          = 2**16

# Create a UDP socket at client side
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Argument Parser
args_list = (str(sys.argv))
port = int(sys.argv[1])
path = sys.argv[2]

def receive_file():
    piece = []
    prev_ack = -1
    rn = 0
    print('Waiting for server to send packet...')
    while(True):
        packet, addr = UDPClientSocket.recvfrom(bufferSize)
        msg = Segment()
        msg.load_segmentation(packet)
        # If the sender is different, pass
        if(addr != serverAddressPort):
            print('THERE IS ANOTHER CONNECTION')
            continue
        # If the flag is FIN, finished
        if(msg.get_flag_type() == "FIN"):
            break
        
        message = Segment()
        message.set_flag("ACK")
        # changing and keep data if valid and seqnumber == rn
        if(msg.is_checksum_valid() and msg.get_seqnumber() == rn):
            print("[Segment SEQ=",msg.get_seqnumber(),"] Received")
            piece.append(msg.get_data())
            prev_ack = rn
            rn+=1
            message.set_headers(rn,prev_ack)
            bytesToSend = message.get_bytes()
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            print("Ack sent")
        else:
            if(msg.is_checksum_valid()):
                print("[Segment SEQ=",msg.get_seqnumber(),"] Segment damaged")
            else:
                print("[Segment SEQ=",msg.get_seqnumber(),"] Segment not valid")
            message.set_headers(rn,prev_ack)
            bytesToSend = message.get_bytes()
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            print("Ack the latest Acked sequence")
    print("File completely received")
    print("Saving file to the requested directory ", path)
    try:
        writer = open(path, "wb")
        for binary in piece:
            writer.write(binary)
        writer.close()
    except Exception as e:
        print(e)
    
    
        

def ThreeWayHandshakeClient():
    # Send SYN
    UDPClientSocket.settimeout(5)
    try:
        print("Three Way Handshake client start")
        print("Sending SYN")
        # SYN Segment
        msg = Segment()
        msg.set_flag("SYN")
        # SEQ = 0
        SEQ = 0
        msg.set_headers(SEQ, 0)
        bytesToSend = msg.get_bytes()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        # Receive SYN-ACK
        SYNACK, address = UDPClientSocket.recvfrom(bufferSize)
        # Decode SYN-ACK
        msg = Segment()
        msg.load_segmentation(SYNACK)
        if msg.get_flag_type() == "SYN-ACK" and msg.get_acknumber() == (SEQ+1):
            print("Correct SYN-ACK Received")
        else:
            return False    # Kalau gagal

        # Get server SEQ
        server_SEQ = msg.get_seqnumber()
        ACK = server_SEQ + 1

        # Send ACK
        print("Sending ACK")
        # ACK Segment
        msg = Segment()
        msg.set_flag("ACK")
        msg.set_headers(0, ACK)
        bytesToSend = msg.get_bytes()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        # Done
        print("Three Way Handshake client done")
        UDPClientSocket.settimeout(None)

        return True

    except socket.timeout:
        print("Socket timeout")

# three way
connected = ThreeWayHandshakeClient()

# Go-Back-N ARQ
if connected:
    receive_file()


