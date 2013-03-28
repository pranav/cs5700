
from struct import *
import random, socket

class IP:

    # Generate the header
  def generate_header(self):
    return pack('!BBHHHBBH4s4s', self.ihl_version, self.tos, self.tot_len, self.id, self.frag_off, self.ttl, self.protocol, self.check, self.saddr, self.daddr)

  def __init__(self, source_ip, destination_ip):
    self.source_ip = source_ip
    self.destination_ip = destination_ip
    self.ihl = 5
    self.version = 4
    self.tos = 0
    self.tot_len = 20 + 20
    self.id = self.random_id()
    self.flags = 2 << 13
    self.frag_off = self.flags + 0
    self.ttl = 255
    self.protocol = socket.IPPROTO_TCP
    self.check = 10
    self.saddr = socket.inet_aton(self.source_ip)
    self.daddr = socket.inet_aton(self.destination_ip)
    self.ihl_version = (self.version << 4) + self.ihl
    print "SOURCE: ", self.source_ip, " DEST: ", self.destination_ip


  # Returns a random IPv4 id
  def random_id(self):
    return random.randint(0, 65535)
