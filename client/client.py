# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:37:36 2017

@author: timo
"""

import socket
import sys
import time
import json
import urllib.request
import zipfile
import cpuinfo
import platform
import psutil
import math

installed_packages = []

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8895)

sock.connect(server_address)


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

    
    installed_packages.append(json_package[1])
    urllib.request.urlretrieve(json_package[1]['Url'], 'downloaded_packages/' + json_package[1]['Name'] + '-' + json_package[1]['Version'] + '.zip')
    zipfile.ZipFile('downloaded_packages/' + json_package[1]['Name'] + '-' + json_package[1]['Version'] + '.zip' , 'r').extractall('installed_packages/')
    print("installed package " + json_package[1]['Name'])
    #print >>sys.stderr, 'received "%s"' % ig['name']
    return 
    
def get_update_packages(packages):
    
    tmp = json.loads(packages)
    #print json.dumps(tmp['update_package1'], indent=4, sort_keys=True)

    
    for package_t in tmp.items():
          
        if package_t[1] not in installed_packages:
            install_package(package_t)

    return


while(True):

        ram = psutil.virtual_memory()
        ram = ram.total / 1024 ** 3
        ram = math.ceil(ram * 100) / 100
        
        sock.sendall(bytes(build_package(["get_update_packages",platform.uname().node ,cpuinfo.get_cpu_info().get('brand'),"NVIDIA GTX 680",str(ram)],["REQUEST","HOSTNAME","CPU","GPU","RAM"]), 'utf-8'))
        time.sleep(5)
        # Look for the response
        amount_received = 0
    
        data = sock.recv(1024)
        data = bytes(data).decode(encoding='UTF-8')
            #print data
        if not data: 
   
            break
    
        get_update_packages(data)        
            #print >>sys.stderr, 'received "%s"' % data

sock.close()
        








