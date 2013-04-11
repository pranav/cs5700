
"""
  TCP Variant known as Shoe
  Wraps over Socket class
  Redefines connect, send, recv, close
"""

import socket, random, time

from struct import *
from ip import *

def get_ts():
  return int("".join(repr(time.time())[-11:-1].split(".")))



# Shoe class represents a socket
class Shoe:

  def get_ts(self):
    return get_ts()


  # Returns a new socket using raw socket
  def socket(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  # Generate a random seq number
  def random_sequence(self):
    return random.randint(100, 10000000)

  def get_open_port(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


  # The initial connection that will do the 3 way handshake
  def connect(self, hostport):
    self.destination_hostname = hostport[0]
    self.destination_port = hostport[1]
    self.destination_ip = self.get_destination_ip()
    self.destination_ip_hex = socket.inet_aton(self.destination_ip)
    self.local_ip = self.get_local_ip()
    self.local_ip_hex = socket.inet_aton(self.local_ip)
    self.local_port = self.get_open_port()

    self.data = ""
    self.sequence = self.random_sequence()

    #> ERIC: we need to bind to something that is not 0.0.0.0.
    self.recv_sock = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP )
    self.recv_sock.bind((self.local_ip, self.local_port))
    self.recv_sock.setblocking(1)

    self.do_handshake()


  def do_handshake(self):
    self.send_initial_syn()
    self.read_packet()
    self.send_ack()

    # TODO: make sure that we're okay to send--how?

  # Send the initial SYN packet
  def send_initial_syn(self):
    # Flags for the packet
    flags = { 'syn': 1 }

    # The packet itself
    packet = TCP(self.local_ip_hex, self.local_port, self.destination_ip_hex, flags, self.sequence)
    self.last_reply_seq = packet.sequence
    
    # Socket library to send the packet
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    ip = IP(self.local_ip, self.destination_ip)
    self.sock.sendto(ip.generate_header() + packet.generate_syn_packet(), (self.destination_ip, 0))


  # Read the synack from the server and return a tuple containing seq num and ack num
  # '!HHLLBBH'
  # RETURNS: data
  # Side effects: sets self.last_reply_seq, last_reply_ack, last_tsval, last_tsecr
  def read_packet(self):
    #time.sleep(20)
    (rawpacket, addy) = self.recv_sock.recvfrom(4096)
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

    if flags['rst'] == 1:
      self.do_handshake()
      self.data = ""
    else:
      # Timestamp
      ts = self.get_tsval( rawpacket, data_offset, 40 )

      self.last_reply_seq = packet[2]
      self.last_reply_ack = packet[3]

      if ts and len(ts) == 2:
        self.last_tsval = ts[0]
        self.last_tsecr = ts[1]
      elif ts and len(ts) == 1:
        self.last_tsval = ts[0]
        self.last_tsecr = 0
      else:
        self.last_tsval = 0
        self.last_tsecr = 0


      # Data
      data = ""
      for i in range( len(rawpacket) - (40 + data_offset)):
        data = data + rawpacket[i + 40 + data_offset]

      self.data = data

  # Parses the TSVal from the raw packet
  def get_tsval(self, rawpacket, data_offset, i):
    if i < len(rawpacket):
      kind = unpack('!B', rawpacket[i])[0]
      if kind == 8:
        (kind, length, timestamp, echo) = unpack('!BBLL', rawpacket[i:i+10])
        return (timestamp, echo)
      else:
        return self.get_tsval(rawpacket, data_offset, i+1)


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
  def send_ack(self):
    flags = { 'ack': 1 }
    packet = TCP(self.local_ip_hex, self.local_port, self.destination_ip_hex, flags, self.sequence, old_ts = self.last_tsval)
    packet.TSval = self.get_ts()
    packet.ack_seq = self.last_reply_seq
    packet.sequence = self.last_reply_ack

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    ip = IP(self.local_ip, self.destination_ip)
    self.sock.sendto(ip.generate_header() + packet.generate_syn_packet(), (self.destination_ip, 0))



  # Send the ack after the synack
  def rest_ack(self):
    flags = { 'ack': 1 }
    packet = TCP(self.local_ip_hex, self.local_port, self.destination_ip_hex, flags, self.sequence, old_ts = self.last_tsval)
    packet.TSval = self.get_ts()
    packet.ack_seq = self.last_reply_seq
    packet.sequence = self.last_reply_ack

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    ip = IP(self.local_ip, self.destination_ip)
    self.sock.sendto(ip.generate_header() + packet.generate_syn_packet(), (self.destination_ip, 0))


  # Get the local machines IP address
  #> ERIC: this is where we need to change something
  def get_local_ip(self):
    return socket.gethostbyname(socket.gethostname())


  # Get the destination's IP address
  def get_destination_ip(self):
    return socket.gethostbyname(self.destination_hostname)

  # Receive a packet from the destination
  def recv(self):
    return "RECV: " + self.data


  # Close this connection
  def close(self):
    self.sock.close()

  # Send a packet to the destination
  def send(self, data):
    flags = { 'psh': 1, 'ack': 1 }
    #flags = { 'psh': 1 }
    packet = TCP( self.local_ip_hex, self.local_port, self.destination_ip_hex, flags, self.sequence, data=data)
    packet.TSval = self.get_ts()
    packet.TSecr = self.last_tsval
    packet.ack_seq = self.last_reply_seq + len(self.data)
    packet.sequence = self.last_reply_ack

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    ip = IP(self.local_ip, self.destination_ip)
    self.sock.sendto(ip.generate_header() + packet.generate_packet(), (self.destination_ip, 0))

    self.read_packet()
    self.rest_ack()
    







###############################################################################
############## TCP CLASS ######################################################
###############################################################################

# Represents a tcp packet
class TCP:

  # Constructor.
  # a = TCP(source_ip, destination_ip, data, flags)
  def __init__(self, source_ip, source_port, destination_ip, flags, sequence, data = '' ,old_ts = 0):
    # Source port (0 => open port)
    self.source_port = source_port
    # Destination port (always 80 for HTTP)
    self.destination_port = 80
    # Sequence number (start at random, need to increment later on)
    self.sequence = sequence
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
    self.window_size = 1024
    # Checksum
    self.checksum = 0
    # offset from sequence number indicating last urgent data byte
    self.urg_ptr = 0
    self.protocol = socket.IPPROTO_TCP
    # Overrides
    self.destination_ip = destination_ip
    self.source_ip = source_ip
    self.data = data
    # Try to set the syn flag
    try: 
      self.syn = flags['syn']
      self.data_offset = 8
    except: self.syn = 0
    # Try to set the ack flag
    try:
      self.ack = flags['ack']
      self.data_offset = 8
    except: self.ack = 0
    # Try to set the fin flag
    try: self.fin = flags['fin']
    except: self.fin = 0

    try: self.psh = flags['psh']
    except: self.psh = 0
    # Compact the flags
    self.flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5) + (self.ece << 6) + (self.cwr << 7) + (self.ns << 8)

    self.offset_res = (self.data_offset << 4) + 0
    # TCP Option TIMESTAMP: only happens on intial SYN, or when received a TSopt
    self.TSval = get_ts()
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

    if len(self.data) % 2 == 1:
      self.data = self.data + ' '

    tcp_length = len(tcp_header) + len(self.data)
    psh = pack('!4s4sBBH' , self.source_ip, self.destination_ip, 0, self.protocol, tcp_length);
    psh = psh + tcp_header + self.data
    cksum = self.do_checksum(psh)
    tcp_header = pack('!HHLLBBH' , self.source_port, self.destination_port, self.sequence, self.ack_seq, self.offset_res, self.flags,  self.window_size) + pack('H' , cksum) + pack('!HBBLLBB' , self.urg_ptr, 8, 10, self.TSval, self.TSecr, 0, 0)
    return tcp_header + self.data


  # Generate a packet
  def generate_syn_packet(self):
    offset = 8
    offset_res = (offset << 4) + 0
    tcp_header = pack('!HHLLBBHHHBBLLBB', self.source_port, self.destination_port, self.sequence, self.ack_seq, offset_res, self.flags, self.window_size, self.checksum, self.urg_ptr, 8, 10, self.TSval, self.TSecr, 4, 2 )

    while len(tcp_header) % 32 != 0:
      tcp_header = tcp_header + pack('!B', 0)



    tcp_length = len(tcp_header) + len(self.data)
    psh = pack('!4s4sBBH' , self.source_ip, self.destination_ip, 0, self.protocol, tcp_length);
    psh = psh + tcp_header
    cksum = self.do_checksum(psh)
    tcp_header = pack('!HHLLBBH' , self.source_port, self.destination_port, self.sequence, self.ack_seq, offset_res, self.flags,  self.window_size) + pack('H' , cksum) + pack('!HBBLLBB' , self.urg_ptr, 8, 10, self.TSval, self.TSecr, 4, 2)

    while len(tcp_header) % 32 != 0:
      tcp_header = tcp_header + pack('!B', 0)

    return tcp_header



























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
