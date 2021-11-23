import socket
import sys

class Server:
  def __init__(self, port, file_path) -> None:
    # init server
    self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # allow broadcast
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # 
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # bind server
    self.server.bind(('localhost', port))
    self.server.setblocking(0)

    self.port = port
    self.file_path = file_path
  
  def listen(self):
    listening_for_clients = True
    while listening_for_clients:
      connections = []
      msg, addr = self.server.recvfrom(2**16)

  def send_file(self):
    # three way handshake
    # ambil file dan segmentasi
    # kirim pake algoritma Go-Back-N
    pass

  def three_way_handshake(self):
    pass



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
  args_list = (str(sys.argv))
  server_socket = Server()
  server_socket.listen()
  server_socket.send_file()