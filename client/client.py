# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:37:36 2017

@author: timo
"""

import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8893)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def sendInfo(cpu, gpu, ram):
    
    return
    

def build_package(args, v):
    package = "{"
    for x in range(len(v)):
        if x == len(v)-1:
            package +=  v[x] + ":" + args[x] 
            print "test"
        else:
            package +=  v[x] + ":" + args[x] + ","

    package += "}"
    return package

try:
    
    # Send data
    message = 'blabla'
    sock.sendall(build_package(["cpu","gpu","ram"],["CPU","GPU","RAM"]))
    time.sleep(5)
    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()