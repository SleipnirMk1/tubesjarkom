import socket
import sys
from segment import Segment

# ngeGet file jadi binary, dipotong potong jadi beberapa bagian sesuai size
def getFileAsBinary(file, size):
    reader = open(file, "rb")
    piece = []
    while True:
        tmpPiece = file.read(size)
        if(tmpPiece == b''):
            break
        else:
            piece.append(tmpPiece)
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
      print("[!] Connection from {} estabished".format(addr))
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
    # send message to start handshake
      message = str.encode("START HANDSHAKE")
      self.server.sendto(message, address)
      print("Three Way Handshake server start")

      # Receive SYN
      SYN, address = self.server.recvfrom(self.buffer_size)
      # Decode SYN
      msg = Segment()
      msg.load_segmentation(SYN)
      if msg.get_flag_type() == "SYN":
          print("SYN Received from {}".format(address))
      else:
          return False    # Kalau gagal

      # Send SYN-ACK
      print("Sending SYN-ACK")
      # SYN-ACK Segment
      msg = Segment()
      msg.set_flag("SYN-ACK")
      bytesToSend = msg.get_bytes()
      self.server.sendto(bytesToSend, (serverAddressPort, port))

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
    # ambil file dan segmentasi
    # kirim pake algoritma Go-Back-N



# bufferSize = 1024
# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)

# print("Server up")


# listen = True
# while(listen):
#   print("Server is listening")
#   bytesAddressPair = server_socket.recvfrom(bufferSize)
#   message = bytesAddressPair[0]
#   address = bytesAddressPair[1]

#   clientMsg = "Message from Client:{}".format(message)
#   clientIP = "Client IP Address:{}".format(address)

#   print(clientMsg)
#   print(clientIP)

#   server_socket.sendto(bytesToSend, address)

if __name__ == "__main__":
  # parse arguments
  args_list = (str(sys.argv))
  server_socket = Server(int(sys.argv[1]), args_list[2])
  # listen
  server_socket.listen()
  # send
  server_socket.send_file()
