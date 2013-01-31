#!/usr/bin/python

import sys
import socket
import time

from HTMLParser import HTMLParser

username = sys.argv[1]
password = sys.argv[2]
hostname = "cs5700f12.ccs.neu.edu"
port = 80;

visited_links = []
secret_flags = []
link_queue = ["/fakebook"] # Start with /facebook
csrf_cookie = ""
sessionid = ""



# Parse links from HTMLParser constructed from given html document
# TODO: can we nest this inside the _get_new_links_ function?
class LinkParser( HTMLParser ):
    def handle_starttag( self, tag, attrs ):
        if tag == 'a':
            link = next( sub1 for sub1 in attrs if 'href' in sub1 )[1]

            # print link
            if not have_we_been_there_yet( link )
                link_queue.append( link )


# Create socket connection and return a socket
def connect():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((hostname, port))
  return sock

<<<<<<< HEAD:Project2/webcrawler.py
# Check to see if we've been to a link
def have_we_been_there_yet(link):
  return link in visited_links

# Hacky and stupid way to find flags using pattern matching but easier
# than parsing
def try_to_find_flags( html ):
    html2 = html.split("<h2 class='secret_flag' style=\"color:red\">")

    if len( html2 ) > 1:
        at = html2[1]
        print at[ 0:at.find( '</h2>' ) ].strip()


# Parse HTML to populate link queue with new links
def get_new_links( html ):
    parser = LinkParser()
    parser.feed( html )



def launch_thread():
  link = link_queue.pop()
  html = get_page(link) # Handles error messages
  try_to_find_flags( html ) # Will add to secret_flags
  get_new_links( html ) # Will add to link_queue






=======
# Checks if link is in visited_links
def have_we_been_there_yet(link):
  return link in visited_links

# Class for launching threads
class Launch_Thread(threading.Thread):
  def run(self):
    link = link_queue.pop()
    html = get_page(link) # Handles error messages
    try_to_find_flags(html) # Will add to secret_flags
    get_new_links(html) # Will add to link_queue
>>>>>>> 9f8aa5f191d5f31bb7e53d8c678ea37b478c8d52:Project2/webcrawler.py


# Connect to server and login
sock = connect()
do_login()

# Keep launching threads until we have 5 flags
while len(secret_flags) < 5:
  if len(link_queue) > 0:
    Launch_Thread().start()
  else:
    time.sleep(1) # Give it a chance to find more links

# Print flags at the end
for flag in secret_flags:
  print flag


