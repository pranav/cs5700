#!/usr/bin/python

import sys
import socket
import time
import threading

from HTMLParser import HTMLParser
from urlparse import urlparse

username = sys.argv[1]
password = sys.argv[2]
hostname = "cs5700f12.ccs.neu.edu"
port = 80;

visited_links = []
secret_flags = []
link_queue = ["/fakebook/"] # Start with /facebook
cookies = [] # An array of tuples. a tuple is a (name_of_cookie, value_of_cookie)


# Parse links from HTMLParser constructed from given html document
# TODO: can we nest this inside the _get_new_links_ function?
class LinkParser( HTMLParser ):
    def handle_starttag( self, tag, attrs ):
        if tag == 'a':
            o = urlparse( next( sub1 for sub1 in attrs if 'href' in sub1 )[1] )

            # get just the directory...
            link = o.path

            print link
            if not have_we_been_there_yet( link ):
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
  print "login"
  headers = get_headers("/accounts/login/?next=/fakebook/") # Send get request to get cookies
  set_cookies(headers) # Save those 2 cookies
  headers = generate_login_headers() # Create a new POST request to login with the cookies
  headers = send(headers) # Send the POST request to the server
  print headers
  set_cookies(headers) # Save any updated cookies. We should be logged in now.
  print "login complete"

# Get the requested page and send all the cookies while doing it
def get_page(link):
  headers = """GET {link} HTTP/1.1
Host: cs5700f12.ccs.neu.edu
{cookies}


  """.format(link=link, cookies=stringify_cookies())
  reply = send(headers)
  return reply.split("\r\n\r\n")[1]

# Generate cookie header from the cookies variable
def stringify_cookies():
  cookie_s = "Cookie: "
  for c in cookies:
    cookie_s += c[0] + "=" + c[1] + "; "
  return cookie_s

# Simple function that sends some headers
def get_headers(link):
  headers = """
GET {link} HTTP/1.1
Host: cs5700f12.ccs.neu.edU



  """.format(link=link)
  reply = send(headers)
  return reply

# Just send a message to the server and return the reply
def send(raw):
  sock = connect()
  sock.send(raw)
  return sock.recv(10000)


# Uses raw headers, and gets cookies out of them
def set_cookies(headers):
  global cookies # Need this to modify global variables
  for line in headers.split('\n'):
    if line.find("Set-Cookie") >= 0:
      cookie_name = line.split()[1].split('=')[0]
      cookie_value = line.split()[1].split('=')[1].split(';')[0]
      cookies.append((cookie_name, cookie_value))


def generate_login_headers():
  cookie_s = ""
  cookie_h = ""
  for cookie in cookies:
    cookie_s = cookie_s + cookie[0] + "=" + cookie[1]
    cookie_s = cookie_s + ";"

    if cookie[0] == "csrftoken":
        cookie_h = "csrfmiddlewaretoken=" + cookie[1]


  data = """username={username}&password={password}&{cookie_h}&next=%2Ffakebook%2F""".format(username=username,password=password,cookie_h=cookie_h)
  content_length = len( data )

  headers = """POST /accounts/login HTTP/1.1
  Host: cs5700f12.ccs.neu.edu
  Connection: keep-alive
  Content-Length: {content_length}
  Cache-Control: max-age=0
  Accept: text/html,application/xhtml+xml,application/xml
  Origin: http://cs5700f12.ccs.neu.edu
  User-Agent: Mozilla/5.0 (X11; Linux i686)
  Content-Type: application/x-www-form-urlencoded
  Referer: http://cs5700f12.ccs.neu.edu/accounts/login/?next=/fakebook/
  Accept-Encoding: identity
  Accept-Language: en-US,en;q=0.8
  Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
  Cookies:{cookie_s}
  Content-Encoding: identity

  {data}


  """.format(cookie_s=cookie_s,content_length=content_length,data=data)
  print headers

  return headers

# Connect to server and login
do_login()


# Keep launching threads until we have 5 flags
while len(secret_flags) < 5 and False:
  if len(link_queue) > 0:
    link = link_queue.pop()
    html = get_page(link) # Handles error messages
    try_to_find_flags(html) # Will add to secret_flags
    get_new_links(html) # Will add to link_queue
    #    Launch_Thread().start()
  else:
    time.sleep(1) # Give it a chance to find more links

# Print flags at the end
for flag in secret_flags:
  print flag


