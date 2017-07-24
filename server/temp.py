# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -- CLIENT CODE --


import socket, pickle, sys, time, json, os
from threading import Thread
from flask import *
import netifaces as ni

interface_counter = 0

for interface in ni.interfaces():
    print("Interface " + str(interface_counter) + ": " + interface)
    interface_counter += 1

input_interface = input("\nBitte geben Sie ihr Netzwerkinterface an: ")

ni.ifaddresses(ni.interfaces()[int(input_interface)])
ip = ni.ifaddresses(ni.interfaces()[int(input_interface)])[ni.AF_INET][0]['addr']

print("\nihre Ip ist: " + ip + "\n")


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
    package['Url'] = url
    package['command'] = command
    #json_data = json.dumps(package)    
    #package_part_one = "{Name:" + name + ",Version:" + version + ",Checksum:"
    #package_part_two = ",URL:" + url + ",Command:" + command + "}"
    #checksum = sys.getsizeof(package_part_one) + sys.getsizeof(package_part_two)
    #package = package_part_one + str(checksum) + package_part_two
    return package
    
    
clients, count = [], 0
update_packages = []

update_packages.append(build_update_package("name1", "1.0.24", "http://" + ip + ":5000/update/update_package_1.txt.zip", "5"))
update_packages.append(build_update_package("name2", "1.0.24", "http://" + ip + ":5000/update/update_package_2.txt.zip", "5"))
update_packages.append(build_update_package("name3", "1.0.24", "http://" + ip + ":5000/update/update_package_3.txt.zip", "5"))

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

def start_flusk():
    app.run(ip, port=5000, threaded=True)

@app.route('/update/<path:filename>')
def downloads(filename):

    return send_from_directory('update_packages', filename)



HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8895 # Arbitrary non-privileged port
 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
s.listen(10)



def clientthread(conn):

    while True:
         
        #Receiving from client
        data = ""
        
        try:
            data = conn.recv(1024)
            data = bytes(data).decode(encoding='UTF-8')
        except:
            pass
        
        if not data: 
            break
     
        conn.sendall(create_json_object().encode())     
     
        #for package in update_packages:
         #  conn.sendall(package)
     
    #came out of loop
    conn.close()
    return  

    
    
def print_all_clients():
    
    counter = 3
    loop_counter = 0

    while 1:
        c = 0
        print("\n--------------print_all_clients--------------")
        for client in clients:
            if client.is_alive():
                print("client nr." + str(c) + " is alive")
            else:
                print("client nr." + str(c) + " is not alive" )
            c+=1
        print("---------------------------------------------\n")
        time.sleep(5)
        
        loop_counter += 1
        
        if loop_counter == 2:
            counter += 1
            update_packages.append(build_update_package("name" + str(counter), "1.0.24", "http://" + ip + ":5000/update/update_package_3.txt.zip", "5"))
            loop_counter = 0
            
    return
    
    
tFlusk = Thread(target = start_flusk)
tFlusk.start()

tcrint = Thread(target = print_all_clients)
tcrint.start()




while 1:

    conn, addr = s.accept()
    print("\n-----------------new_client------------------")
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    print("---------------------------------------------\n")
     
    t = Thread(target=clientthread, args=(conn,))
    t.start()
    clients.append(t)
        
    time.sleep(5)
    
 
        

    
s.close()





