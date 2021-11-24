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
      self.data = self.bytes[12:]
      self.seqnumber, self.acknumber, self.flag, self.checksum = struct.unpack("IIBxH", bytes[0:12])

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
    elif(self.flag == 0b00001010):
      return "SYN-ACK"

  def get_data(self):
    return self.data

  def generate_checksum(self):
    # generate checksum using other bytes
    # convert to 16-bit integers
    # calculate sum
    
    print("Converting message bytes into 16-bit chunks")
    message_in_16bit = [self.data[i:i+2] for i in range(0, len(self.data), 2)]
    for chunk in message_in_16bit:
      if len(chunk) == 1:
        chunk += struct.pack("x")
    print(message_in_16bit)
    print("Taking the sum of chunks and applying one's complement")
    print("Storing checksum")
    self.checksum = ~(sum(message_in_16bit) & 0xFFFF)
    print(self.checksum)
  
  def is_checksum_valid(self):
    # check using checksum
    # add checksum to final sum total
    # check if there is any 0 -> corrupt
    
    total = (self.checksum + self.get_bytes()) & 0xFFFF
    print(total)
    return total == 0xFFFF

  def get_bytes(self):
    if self.bytes == b'':
      seq_bytes = struct.pack("I", self.seqnumber)
      ack_bytes = struct.pack("I", self.acknumber)
      flag_bytes = struct.pack("B", self.flag)
      empty_bytes = struct.pack("x")
      data_bytes = self.data
      self.checksum = self.generate_checksum()
      checksum_bytes = struct.pack("H", self.checksum)

      message_bytes = seq_bytes + ack_bytes + flag_bytes + empty_bytes + checksum_bytes + data_bytes
      self.bytes = message_bytes
      return message_bytes

    return self.bytes

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
    elif(flag == "SYN-ACK"):
      print("Flag set to SYN-ACK")
      self.flag = 0b00001010
    else:
      print("Invalid flag input")
      print("Flag set to NONE")
      self.flag = 0b00000000

  def set_headers(self, sequence_number, ack_number):
    self.seqnumber = sequence_number
    self.acknumber = ack_number