# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:37:36 2017

@author: timo
"""

import socket
import sys
import time
import json

installed_packages = []

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8895)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def sendInfo(cpu, gpu, ram):
    
    return
    

def build_package(args, v):
    package = "{"
    for x in range(len(v)):
        if x == len(v)-1:
            package +=  v[x] + ":" + args[x] 
        else:
            package +=  v[x] + ":" + args[x] + ","

    package += "}"
    return package
    
def print_installed_packages():
    for installed in installed_packages:
        #tmp_json = json.loads(installed[0])
        print >> str(installed)
        
    return
        
def install_package(json_package):
    #ig = json.dumps(json_package)    
    print "installed package " + json_package[1]['Name']
    
    installed_packages.append(json_package[1])
    #print >>sys.stderr, 'received "%s"' % ig['name']
    return 
    
def get_update_packages(packages):
    
    tmp = json.loads(packages)
    #print json.dumps(tmp['update_package1'], indent=4, sort_keys=True)

    
    for package_t in tmp.items():
        #print package_t[1]
        #fg = json.dumps(package_t[1])
        
        #print fg
        #install_package(fg)           
        if package_t[1] not in installed_packages:
            install_package(package_t)
            #installed_packages.append(package_t)        
            #print >>sys.stderr, 'received "%s"' % fg['Name']
        #print json.dumps(package_t[1], indent=4, sort_keys=True)       
        #print json.dumps(tmp['update_package1'], indent=4, sort_keys=True)
        #tmp = json.loads(package)
        #print json.dumps(package, indent=4, sort_keys=True)
        #tmp_json_package = json.loads(package)
        #print >>sys.stderr, 'received "%s"' % package['update_package1']
        #if tmp_json_package not in installed_packages:
         #   install_package(tmp_json_package) 
          #  print >> tmp_json_package[0]
    
    #print_installed_packages()
    return

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
        get_update_packages(data)        
        #print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()