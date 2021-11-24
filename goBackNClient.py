import socket

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8000)
bufferSize          = 1024

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

piece = []          #data yang sudah diambil
rn = 0              #request number

UDPClientSocket.bind(('127.0.0.2', 12345))
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msg, addr = UDPClientSocket.recvfrom(bufferSize)
print(msg)
print(addr)

print('Listening...')
while (True):
    msg, addr = UDPClientSocket.recvfrom(bufferSize)
    
    #cek bener gak dari server yang sama <--- ini belum
    
    #if(is_checksum_valid and get_seq_number()==rn):
    if(True):
        #ini cuma buat test
        if(msg==b'13'):
            print('Mengirim ACK dengan request number ', rn)
            msgFromClient       = str(rn+1)
            bytesToSend         = str.encode(msgFromClient)
            UDPClientSocket.sendto(bytesToSend, addr)
            print('Yes selesai')
            break
        #if(fin):
            #break
        #Proses decode packet
        #...
        #...
        #...
        #piece.append(...)
        print('Menerima Packet ', rn+1)
        print('isinya: ', msg)
        rn+=1
    print('Mengirim ACK dengan request number ', rn+1)
    #proses ngirim ack
    #packet = Segment()
    #packet.set_flag("ACK")
    #packet.set_headers(rn,rn)
    #server.sendto(packet.get_bytes, address)

    #ini cuma buat ngecek
    msgFromClient       = str(rn+1)
    bytesToSend         = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, addr)
    print('Berhasil mengirim ACK')
print('selesai')
