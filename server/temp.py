# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -- CLIENT CODE --


import socket, pickle, sys, time
from thread import *
from threading import Thread

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8893 # Arbitrary non-privileged port
 
clients, count = [], 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)

def build_update_package(name, version, url, command):
    package_part_one = "{Name:" + name + ",Version:" + version + ",Checksum:"
    package_part_two = ",URL:" + url + ",Command:" + command + "}"
    checksum = sys.getsizeof(package_part_one) + sys.getsizeof(package_part_two)
    package = package_part_one + str(checksum) + package_part_two
    return package

def clientthread(conn):

    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        #print data
        reply = build_update_package("name", "1.0.24", "https://update_my_client.de", "5")
        if not data: 
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
    
def print_all_clients():
    while 1:
        c = 0
        print "\n--------------print_all_clients--------------"
        for client in clients:
            if client.is_alive():
                print "client nr." + str(c) + " is alive"
            else:
                print "client nr." + str(c) + " is not alive" 
            c+=1
        print "---------------------------------------------\n"
        time.sleep(5)

    return

start_new_thread(print_all_clients,())


while 1:

    conn, addr = s.accept()
    print "\n-----------------new_client------------------"
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    print "---------------------------------------------\n"
     
    t = Thread(target=clientthread, args=(conn,))
    t.start()
    clients.append(t)
        
    time.sleep(5)
    
s.close()





