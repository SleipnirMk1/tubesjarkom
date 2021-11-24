import socket
from segment import Segment

serverAddressPort   = ("127.0.0.1", 12345)
bufferSize          = 1024
sizeAllowed         = 32768

piece = []          #data yang sudah diambil
rn = 0              #request number
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
UDPClientSocket.bind(serverAddressPort)
while (True):
    msg, addr = UDPClientSocket.recvfrom(bufferSize)
    
    #cek bener gak dari server yang sama <--- ini belum
    
    #if(is_checksum_valid and get_seq_number()==rn):
    if(True):
        #ini cuma buat test
        if(msg=='selesai'):
            print('Yes selesai')
            break
        #if(fin):
            #break
        #Proses decode packet
        #...
        #...
        #...
        #piece.append(...)
        print('Menerima Packet ', rn)
        print('isinya: ', msg)
        rn+=1
    else:
        print('Terjadi error pada packet ', rn)
    print('Mengirim ACK dengan request number ', rn)
    #proses ngirim ack
    #packet = Segment()
    #packet.set_flag("ACK")
    #packet.set_headers(rn,rn)
    #server.sendto(packet.get_bytes, address)

    #ini cuma buat ngecek
    msgFromClient       = str(rn)
    bytesToSend         = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print('Berhasil mengirim ACK')

#end while
#Harusnya selesain handshake dulu di sini

#Proses pembentukan file
#...
#...
#...
print('selesai')
