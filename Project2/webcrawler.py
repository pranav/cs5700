#!/usr/bin/python

import sys
import socket
import time

username = sys.argv[1]
password = sys.argv[2]
hostname = "cs5700f12.ccs.neu.edu"
port = 80;

visited_links = []
secret_flags = []
link_queue = ["/fakebook"] # Start with /facebook
csrf_cookie = ""
sessionid = ""

# Create socket connection and return a socket
def connect():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((hostname, port))
  return sock

def have_we_been_there_yet(link):
  return link in visited_links

def launch_thread():
  link = link_queue.pop()
  html = get_page(link) # Handles error messages
  try_to_find_flags() # Will add to secret_flags
  get_new_links() # Will add to link_queue








# Connect to server and login
sock = connect()
do_login()

# Keep launching threads until we have 5 flags
while len(secret_flags) < 5:
  if len(link_queue) > 0:
    launch_thread()
  else:
    time.sleep(1) # Give it a chance to find more links

# Print flags at the end
for flag in secret_flags:
  print flag
