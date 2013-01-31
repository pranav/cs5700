#!/usr/bin/python

import sys
import socket

username = sys.argv[1]
password = sys.argv[2]
hostname = "cs5700f12.ccs.neu.edu"
port = 80;

visited_links = []
secret_flags = []

# Create socket connection and return a socket
def connect():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((hostname, port))
  return sock

def have_we_been_there_yet(link):
  return link in visited_links



sock = connect()


while len(secret_flags) < 5:

