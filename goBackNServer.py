import socket
from segment import Segment

def getFileAsBinary(file, size):
    piece = []
    try:
        reader = open(file, "rb")
    except IOError:
        print('Unable to open', file)
        return piece
    while True:
        tmpPiece = reader.read(size)
        if(tmpPiece == b''):
            break
        else:
            piece.append(tmpPiece)
    return piece
    
serverAddressPort= ("127.0.0.2", 12345)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
UDPClientSocket.bind(serverAddressPort)
bufferSize = 128

#piece = getFileAsBinary("test.txt", bufferSize)
piece = ['yes', 'bisa', 'seharusnya', 'ya', 'disini', 'mah', 'cuma', 'buat', 'ngebacot', 'yaudah', 'gas', 'dikit', 'lagi', 'selesai']

#ntar dibenerin
n = 4               #window size
sb = 0              #sequence base
sm = n-1            #sequence max
sn = 0              #sequence number
nPack = len(piece)  #number of packet

addr = ("127.0.0.2", 12345)

print('Sending ', str(nPack) , ' Packet...')
while sb < nPack:
    print('a')
    msg, addr = UDPClientSocket.recvfrom(bufferSize)
    #ambil rn dari packet
    #rn = blablablablabla
    rn = int(msg)
    print('b')
    if(True):
        print("Receive ACK on packet ", rn)
        sb = rn
        sm = rn + n - 1
    print('b')
    while(sb<=sn and sn<=sm):
        print('c')
        #Proses ngirim packet
        #...
        #...
        UDPClientSocket.sendto(str.encode(piece[sn]), addr)
        print('d')
        sn+=1
print('SELESAI')
        












