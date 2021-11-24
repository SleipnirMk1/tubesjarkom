import socket
import sys
from segment import Segment

# ngeGet file jadi binary, dipotong potong jadi beberapa bagian sesuai size
def getFileAsBinary(file, size):
    piece = []
    try:
        reader = open(file, "rb")
        while True:
            tmpPiece = reader.read(size)
            if(tmpPiece == b''):
                break
            else:
                piece.append(tmpPiece)
        reader.close()
        return piece
    except Exception as e:
        print(e)
        return piece
class Server:
  def __init__(self, port, file_path) -> None:
    # init server
    self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # allow broadcast
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # 
    #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # bind server
    print("Server start at port {}".format(port))
    self.server.bind(('localhost', port))
    self.server.setblocking(1)
    # parsed arguments
    self.port = port
    self.file_path = file_path
    # list of clients
    self.connections = []
    # recv buffer size
    self.buffer_size = 2**16
  
  def listen(self):
    print("Listening to broadcast address for clients")
    listening_for_clients = True
    while listening_for_clients:
      msg, addr = self.server.recvfrom(self.buffer_size)
      print("[!] SYN received from {}".format(addr))
      # add to list of clients
      self.connections.append(addr)
      # check if more clients
      listen_more = input("[?] Listen more? (y/n): ")
      if listen_more == "n":
        listening_for_clients = False

    # print list of clients found
    print("{} Clients found:".format(len(self.connections)))
    for i in range(len(self.connections)):
      print("{}. {}".format(i+1, self.connections[i]))

  def three_way_handshake(self, address):
      # Send SYN-ACK
      print("Sending SYN-ACK to {}".format(address))
      # SYN-ACK Segment
      msg = Segment()
      msg.set_flag("SYN-ACK")
      bytesToSend = msg.get_bytes()
      self.server.sendto(bytesToSend, address)

      # Receive ACK
      ACK, address = self.server.recvfrom(self.buffer_size)
      # Decode SYN
      msg = Segment()
      msg.load_segmentation(ACK)
      if msg.get_flag_type() == "ACK":
          print("ACK Received from {}".format(address))
      else:
          return False    # Kalau gagal
        
      # Done
      print("Three Way Handshake server done with {}".format(address))

  def send_file(self):
    # handshake to all clients in list
    for client in self.connections:
      self.three_way_handshake(client)
      n = 4               #window size
      sb = 0              #sequence base
      sm = n-1            #sequence max
      sn = 0              #sequence number
      piece = getFileAsBinary(self.file_path, 32768)
      print(piece)
      nPack = len(piece)  #number of packet
      print("Sending ", str(nPack), ' Packet to client ', client)
      while sb < nPack:
        while(sb<=sn and sn<=min(sm,nPack-1)):
          msg = Segment()
          msg.set_flag("ACK")
          msg.set_headers(sn,0)
          msg.load_data(piece[sn])
          bytesToSend = msg.get_bytes()
          self.server.sendto(bytesToSend, client)
          print("[Segment SEQ=", sn, "] Sent")
          sn+=1
        msg, address = self.server.recvfrom(self.buffer_size)
        #ambil rn dari packet
        #rn = blablablablabla
        message = Segment()
        message.load_segmentation(msg)
        if(message.get_flag_type()=="ACK"):
          if(message.get_acknumber() >= sb):
            print("[Segment SEQ=", message.get_acknumber(),"] Acked")
            sb = message.get_acknumber() + 1
            sm = message.get_acknumber() + n
          else:
            print("[Segment SEQ=", message.get_acknumber(),"] NOT ACKED. Duplicate Ack found.")
            sn = sb
      print('FINISHED SENDING FILE TO ', client)
      msg = Segment()
      msg.set_flag("FIN")
      msg.set_headers(nPack,0)
      bytesToSend = msg.get_bytes()
      self.server.sendto(bytesToSend, client)
    # ambil file dan segmentasi
    # kirim pake algoritma Go-Back-N

if __name__ == "__main__":
  # parse arguments
  args_list = (str(sys.argv))
  server_socket = Server(int(sys.argv[1]), sys.argv[2])
  # listen
  server_socket.listen()
  # send
  server_socket.send_file()
