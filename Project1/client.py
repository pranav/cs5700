#!/usr/bin/python

import sys
import socket

# Argument parsing
# Results in hostname, port, ssl
hostname = sys.argv[1]

if(sys.argv[2] == '-p'):
  port = int(sys.argv[3])
  if sys.argv[4] == '-s':
    ssl = True
  else:
    NUID = sys.argv[4]

elif(sys.argv[2] == '-s'):
  ssl = True
  sys.argv[3] = NUID

else:
  NUID = sys.argv[2]

# Set up the connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostname, port))
sock.send("cs5700spring2013 HELLO "+NUID+'\n')


# Incoming message is like
# cs5700spring2013 STATUS [a number] [a math operator] [another number]\n
# [0]              [1]    [2]        [3]               [4]
def respondToMessage(msg):
  #print msg
  msg = msg.split()
  # Some sanity
  arg1 = msg[2]
  arg2 = msg[4]
  operator = msg[3]
  eq = eval(arg1+operator+arg2)
  #cs5700spring2013 [the solution]\n
  result = "cs5700spring2013 " + str(eq)
  #print result
  return result

while True:
  msg = sock.recv(2048)
  if(msg.split()[2] == "BYE"):
    print msg.split()[1]
    sock.close()
    break
  else:
    response = respondToMessage(msg)
    sock.send(response)


