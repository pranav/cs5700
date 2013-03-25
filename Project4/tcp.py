
"""
  TCP Variant known as Shoe
  Wraps over Socket class
  Redefines connect, send, recv, close
"""

import socket, random, time
from struct import *

# Shoe class represents a socket
class Shoe:


  # Returns a new socket using raw socket
  def socket(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)


  # The initial connection that will do the 3 way handshake
  def connect(self, hostport):
    self.destination_hostname = hostport[0]
    self.destination_port = hostport[1]
    self.destination_ip = self.get_destination_ip()
    self.destination_ip_hex = socket.inet_aton(self.destination_ip)
    self.local_ip = self.get_local_ip()
    self.local_ip_hex = socket.inet_aton(self.local_ip)
    self.local_port = 0
    self.sock.bind(('0.0.0.0', self.local_port))
    self.local_port = self.sock.getsockname()[1]

    self.send_inital_syn()
    synackts = self.read_packet()
    self.send_ack(synackts[0], old_ts = synackts[2])
    ack = self.read_packet()
    self.send_ack(ack[0]-1, old_ts = ack[2])
    self.read_packet()

  # Get the local machines IP address
  def get_local_ip(self):
    return socket.gethostbyname(socket.gethostname())


  # Get the destination's IP address
  def get_destination_ip(self):
    return socket.gethostbyname(self.destination_hostname)


  # Send a packet to the destination
  def send(self):
    print "SEND"


  # Receive a packet from the destination
  def recv(self):
    print "RECV"


  # Close this connection
  def close(self):
    self.sock.close()


  # Send the initial SYN packet
  def send_inital_syn(self):
    # Flags for the packet
    flags = { 'syn': 1 }
    # The packet itself
    packet = TCP(source_ip = self.local_ip_hex, destination_ip = self.destination_ip_hex, data='', flags = flags)
    # Socket library to send the packet
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    self.sock.connect((self.destination_ip, self.destination_port))
    self.sock.send(packet.generate_packet())


  # Read the synack from the server and return a tuple containing seq num and ack num
  # '!HHLLBBH'
  def read_packet(self):
    (rawpacket, port) = self.sock.recvfrom(4096)
    packet = unpack('!HHLLBBHHH', rawpacket[20:40])
    source_port = packet[0]
    destination_port = packet[1]
    seq_num = packet[2]
    ack_num = packet[3]
    data_offset = packet[4]
    flags = self.parse_flags(packet[5])
    window_size = packet[6]
    checksum = packet[7]
    urg_ptr = packet[8]

      # Options
      # TODO: search through options
      # 1. find option 8 - search through octets 41-(41+ (data-offset - 5)) inclusive
      #   1. check first byte for option number
      #      - if not 8, read next byte and move to next octet accordingly
      #      - if 8, read next byte, then the next 4 are TSval, following 4 are TSecr
      tsval = self.get_tsval( rawpacket, data_offset, 41 )

      if not tsval:
        tsval = 0

    return (seq_num, ack_num, tsval)

  # Parses the TSVal from the raw packet

  def get_tsval(self, rawpacket, data_offset, i ):
    if i < len(rawpacket):
      kind = unpack('!B', rawpacket[i])

      if kind == 0:
        return False
      elif kind == 8 :
        length = unpack('!B', rawpacket[i+1])
        tsval = unpack('!I', rawpacket[i+2:i+6])

        return tsval
      elif kind in (11, 12, 13, 16, 17, 20, 21, 22, 23, 24, 25, 26, 29):
        return self.get_tsval( rawpacket, data_offset, i+1 )
      else:
        length = unpack('!B', rawpacket[i+1])[0]

        return self.get_tsval( rawpacket, data_offset, i + length )
    else:
      return False



  # Parses the flag octet from a TCP header
  def parse_flags(self,rawoctet):
    return {
        'cwr': (rawoctet >> 1 != 0),
        'urg': (rawoctet >> 2 != 0),
        'ece': (rawoctet >> 3 != 0),
        'ack': (rawoctet >> 4 != 0),
        'psh': (rawoctet >> 5 != 0),
        'rst': (rawoctet >> 6 != 0),
        'syn': (rawoctet >> 7 != 0),
        'fin': (rawoctet >> 8 != 0)
    }


  # Send the ack after the synack
  def send_ack(self,t, old_ts = 0):
    flags = { 'ack': 1 }
    packet = TCP(source_ip = self.local_ip_hex, destination_ip = self.destination_ip_hex, data='', flags = flags, old_ts = old_ts)
    packet.ack_seq = t+1
    self.sock.send(packet.generate_packet())




###############################################################################
############## TCP CLASS ######################################################
###############################################################################

# Represents a tcp packet
class TCP:

  # Constructor.
  # a = TCP(source_ip, destination_ip, data, flags)
  def __init__(self, source_ip, destination_ip, data, flags, old_ts = 0):
    # Source port (0 => open port)
    self.source_port = 0
    # Destination port (always 80 for HTTP)
    self.destination_port = 80
    # Sequence number (start at random, need to increment later on)
    self.sequence = self.random_sequence()
    # Acknowledgment sequence (this will become sequence number of received packets)
    self.ack_seq = 0
    # Data offset (size of TCP header in 32-bit words)
    self.data_offset = 5
    # Flags
    self.fin = 0
    self.syn = 0
    self.rst = 0
    self.psh = 0
    self.ack = 0
    self.urg = 0
    self.ece = 0
    self.cwr = 0
    self.ns = 0
    # size of the receive window (in bytes) that sender of this segment is willing to receive
    self.window_size = 1500
    # Checksum
    self.checksum = 0
    # offset from sequence number indicating last urgent data byte
    self.urg_ptr = 0
    self.offset_res = (self.data_offset << 4) + 0
    self.data = ''
    self.protocol = socket.IPPROTO_TCP
    # Overrides
    self.destination_ip = destination_ip
    self.source_ip = source_ip
    self.data = data
    # Try to set the syn flag
    try: self.syn = flags['syn']
    except: self.syn = 0
    # Try to set the ack flag
    try: self.ack = flags['ack']
    except: self.ack = 0
    # Try to set the fin flag
    try: self.fin = flags['fin']
    except: self.fin = 0
    # Compact the flags
    self.flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5) + (self.ece << 6) + (self.cwr << 7) + (self.ns << 8)


    # TCP Option TIMESTAMP: only happens on intial SYN, or when received a TSopt
    self.TSval = int(time.time())
    if not self.ack == 0:
      self.TSecr = 0# tsecr doesn't matter
    else:
      self.TSecr = old_ts

  # Takes all the necessary variables and pack them together into the header
  def generate_header(self):
    return pack('!HHLLBBHHH', self.source_port, self.destination_port, self.sequence, self.ack_seq, self.offset_res, self.flags, self.window_size, self.checksum, self.urg_ptr)


  # Get the checksum of a packet
  def do_checksum(self, psh):
    result = 0
    for i in range( 0, len(psh), 2):
      a = ord(psh[i]) + (ord(psh[i+1]) << 8)
      result = result + a
    result = (result >> 16) + (result & 0xffff);
    result = result + (result >> 16);
    result = ~result & 0xffff
    return result


  # Generate a packet
  def generate_packet(self):
    tcp_header = pack('!HHLLBBHHHBBLLBB', self.source_port, self.destination_port, self.sequence, self.ack_seq, self.offset_res, self.flags, self.window_size, self.checksum, self.urg_ptr, 8, 10, self.TSval, self.TSecr, 0, 0)
    tcp_length = len(tcp_header) + len(self.data)
    psh = pack('!4s4sBBH' , self.source_ip, self.destination_ip, 0, self.protocol, tcp_length);
    psh = psh + tcp_header + self.data
    cksum = self.do_checksum(psh)
    tcp_header = pack('!HHLLBBH' , self.source_port, self.destination_port, self.sequence, self.ack_seq, self.offset_res, self.flags,  self.window_size) + pack('H' , cksum) + pack('!HBBLLBB' , self.urg_ptr, 8, 10, self.TSval, self.TSecr, 0, 0)
    return tcp_header + self.data


  # Generate a random seq number
  def random_sequence(self):
    return random.randint(100, 1000000)




























"""

DO THIS LATER...

class IP:
  # Internet header length (howm many 32bit words are the header)
  self.ihl = 5
  # Version (IPv4)
  self.ver = 4
  # Type of Service
  self.ip_tos = 0
  # Size of the entire packet
  self.ip_total_len = 0
  # ID of this ip datagram
  self.ip_id = self.random_ip_id()
  # Fragment offset (we aren't using this)
  self.ip_frag_off = 0
  # IP Time to live
  self.ip_ttl = 255
  # This is TCP 
  self.ip_proto = socket.IPPROTO_TCP
  # 16bit Checksum
  self.ip_check = 0
  # Source IP
  self.source_ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
  # Destination IP
  self.ip_destination = 'help me'
  self.ip_ihl_ver = (version << 4) + self.ihl

  def __init__(self, destination):
    self.ip_destination = socket.inet_aton(destination)

  def get_header(self):
    return pack('!BBHHHBBH4s4s', self.ip_ihl_ver, self.ip_tos, self.ip_total_len, self.ip_id, self.ip_frag_off, ip_ttl, self.ip_proto, self.ip_check, self.ip_destination)

  def random_ip_id(self):
    return random.randint(100,6000)

"""
