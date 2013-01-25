#!/usr/bin/python

import sys
import socket
import ssl

# Argument parsing
# Results in hostname, port, ssl
hostname = sys.argv[1]
sslHuh = False
port = 27993

if(sys.argv[2] == '-p'):
  port = int(sys.argv[3])
  if len(sys.argv) > 4 and sys.argv[4] == '-s':
    sslHuh = True
    NUID = sys.argv[5]
  else:
    NUID = sys.argv[4]

elif(sys.argv[2] == '-s'):
  sslHuh = True
  NUID = sys.argv[3]
  port = 27994

# Isn't this case covered in the first case?
elif(len(sys.argv) > 4 and sys.argv[4] == '-s'):
  sslHuh = True
  NUID = sys.argv[5]

else:
  port = 27993
  NUID = sys.argv[2]

# Set up the connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if(sslHuh):
  sock = ssl.wrap_socket(sock)

sock.connect((hostname, port))
sock.send("cs5700spring2013 HELLO "+NUID+'\n')


# Incoming message is like
# cs5700spring2013 STATUS [a number] [a math operator] [another number]\n
# [0]              [1]    [2]        [3]               [4]
def respondToMessage(msg):
  msg = msg.split()
  # Some sanity
  arg1 = msg[2]
  arg2 = msg[4]
  operator = msg[3]
  eq = eval(arg1+operator+arg2)
  #cs5700spring2013 [the solution]\n
  result = "cs5700spring2013 " + str(int(eq)) + "\n"
  #print result,
  return result

while True:
  msg = sock.recv(4096)
  if 'BYE' in msg:
    print msg.split()[1]
    sock.close()
    break
  elif len(msg) > 2:
    response = respondToMessage(msg)
    sock.send(response)
  else:
    break


