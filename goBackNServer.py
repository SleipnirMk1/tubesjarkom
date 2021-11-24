import socket

# socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# bind server
server_socket.bind(('localhost', 8000))

bufferSize = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

#piece = getFileAsBinary("test.txt", bufferSize)
piece = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

#ntar dibenerin
n = 4               #window size
sb = 0              #sequence base
sm = n-1            #sequence max
sn = 0              #sequence number
nPack = len(piece)  #number of packet

print("Server up")

listen = True
while(listen):
    print("Server is listening")
    bytesAddressPair = server_socket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)
    sb = 0              #sequence base
    sm = n-1            #sequence max
    sn = 0              #sequence number

    server_socket.sendto(bytesToSend, address)
    if(address):
        print('Sending ', str(nPack) , ' Packet...')
        while sb < nPack:
            while(sb<=sn and sn<=min(sm,nPack-1)):
                #Proses ngirim packet
                #...
                #...
                print(sn)
                server_socket.sendto(str.encode(piece[sn]), address)
                sn+=1
            msg, address = server_socket.recvfrom(bufferSize)
            #ambil rn dari packet
            #rn = blablablablabla
            rn = int(msg)
            if(msg):
                print("Receive ACK on packet ", rn)
                sb = rn
                sm = rn + n - 1
        msg, address = server_socket.recvfrom(bufferSize)
        print(print("Receive ACK on packet ", rn))
        print('SELESAI')
        












