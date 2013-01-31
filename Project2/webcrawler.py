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

# Handle all login related things
def do_login():
  headers = get_headers("/account/login") # Send get request to get cookies
  set_cookies(headers) # Save those 2 cookies
  headers = generate_login_headers() # Create a new POST request to login with the cookies
  headers = send(headers) # Send the POST request to the server
  set_cookies(headers) # Save any updated cookies. We should be logged in now.










# Connect to server and login
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


