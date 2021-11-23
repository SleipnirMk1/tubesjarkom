import struct

class Segment:
  def __init__(self) -> None:
      self.seqnumber = 0
      self.acknumber = 0
      self.checksum = 0
      self.flag = 0b00000000
      self.data = b''
      self.bytes = b''

  def load_bytes(self, bytes):
    self.bytes = bytes

  def load_segmentation(self, bytes):
      self.load_bytes(bytes)
      pass

  def load_data(self, data):
    self.data = data

  def get_flag_type(self):
    if(self.flag == 0b00000000):
      return "NONE"
    elif(self.flag == 0b00000001):
      return "FIN"
    elif(self.flag == 0b00001000):
      return "ACK"
    elif(self.flag == 0b00000010):
      return "SYN"

  def get_data(self):
    return self.data

  def generate_checksum(self):
    # generate checksum using other bytes
    # convert to 16-bit integers
    # calculate sum
    
    print("Converting message bytes into 16-bit chunks")
    message_in_16bit = [self.bytes[i:i+16] for i in range(0, len(self.bytes), 16)]
    print(message_in_16bit)
    print("Taking the sum of chunks and applying one's complement")
    print("Storing checksum")
    self.checksum = ~(sum(message_in_16bit) & 0xFF)
    print(self.checksum)
  
  def validate_checksum(self):
    # check using checksum
    # add checksum to final sum total
    # check if there is any 0 -> corrupt
    
    total = (self.checksum + self.get_bytes()) & 0xFF
    print(total)

  def get_bytes(self):
    seq_bytes = struct.pack("i", self.seqnumber)
    ack_bytes = struct.pack("i", self.acknumber)
    flag_bytes = struct.pack("b", self.flag)
    empty_bytes = struct.pack("x")
    self.checksum = self.generate_checksum()
    data_bytes = self.data
    checksum_bytes = struct.pack("H", self.checksum)

    message_bytes = seq_bytes + ack_bytes + flag_bytes + empty_bytes + checksum_bytes + data_bytes
    return message_bytes

  def set_flag(self, flag):
    if(flag == "SYN"):
      print("Flag set to SYN")
      self.flag = 0b00000010
    elif(flag == "ACK"):
      print("Flag set to ACK")
      self.flag = 0b00001000
    elif(flag == "FIN"):
      print("Flag set to FIN")
      self.flag = 0b00000001
    else:
      print("Invalid flag input")
      print("Flag set to NONE")
      self.flag = 0b00000000

  def set_headers(self, sequence_number, ack_number):
    self.seqnumber = sequence_number
    self.acknumber = ack_number