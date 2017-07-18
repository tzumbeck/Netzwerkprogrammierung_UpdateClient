# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -- CLIENT CODE --


import socket, pickle, sys, time, json
from thread import *
from threading import Thread
from flask import *

def create_json_object():
    json_package = {}
    counter = 0

    for package in update_packages:
        json_package['update_package' + str(counter)] = package
        counter += 1
        
        
    return json.dumps(json_package)
        


    
def build_update_package(name, version, url, command):
    
    package = {}
    package['Name'] = name
    package['Version'] = version
    package['Url'] = version
    package['command'] = command
    #json_data = json.dumps(package)    
    #package_part_one = "{Name:" + name + ",Version:" + version + ",Checksum:"
    #package_part_two = ",URL:" + url + ",Command:" + command + "}"
    #checksum = sys.getsizeof(package_part_one) + sys.getsizeof(package_part_two)
    #package = package_part_one + str(checksum) + package_part_two
    return package
    
    
clients, count = [], 0
update_packages = []

update_packages.append(build_update_package("name1", "1.0.24", "https://update_my_client.de", "5"))
update_packages.append(build_update_package("name2", "1.0.24", "https://update_my_client.de", "5"))
update_packages.append(build_update_package("name3", "1.0.24", "https://update_my_client.de", "5"))

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

def start_flusk():
    app.run(host='0.0.0.0', port=5000, threaded=True)

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8895 # Arbitrary non-privileged port
 


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



def clientthread(conn):

    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        #print data
        if not data: 
            break
     
        conn.sendall(create_json_object())     
     
        #for package in update_packages:
         #  conn.sendall(package)
     
    #came out of loop
    conn.close()
    return  

    
    
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
    
    
start_new_thread(start_flusk, ())
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





