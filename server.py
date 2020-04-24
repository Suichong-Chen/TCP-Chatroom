# server
'''
1. read in port number: if not provided, print a message and exit
2. set up server to work with TCP, IPv4
3. MAX_CLIENTS = 5
4. processClients: read from each client
5. close when SIGINT is sent to the program
6. create threads in a detached state
'''

import socket
import sys
import thread

# exit if port number not received from user
if len(sys.argv) != 3:
    print("port number or IP address not received")
    exit()

port = int(sys.argv[1])
ip = int(sys.argv[2])

def start(port, ip):
    # AF_INET indicates the usage of IPv4, SOCK_STREAM indicates TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (server < 0):
        perror("socket")
        exit()

    # bind the IP address with the given port number
    server.bind(ip, port)

    server.listen(5)

    return server


clients_list = []
server = start(port, ip)

def broadcast(client_server, msg):
    for client in clients_list:
        # don't send the msg to the master server and the client who sends the msg to master
        if client != server and client != client_server:
            try:
                client.send(msg)
            except: # client may interrupt by pressing ctrl+c, thus remove the client from the list of connection
                client.close()
                clients_list.remove(client)
                

def processClients(client, addr):
    client.send("Let's start chatting on port " + str(port))
    while True:
        try:
            msg = client.recv(4096)
            if msg:
                print('<' + str(addr) + '>' + msg)
                broadcast(client, ('<' + str(addr) + '>' + msg))
            else:
                clients_list.remove(client)
        except:
            continue

while True:
    sockId, addr = server.accept()
    clients_list.append(sockId)
    print(str(addr) + "has entered the room")
    broadcast(sockId, "has entered the room")
    start_new_thread(processClients, (sockId, addr))

sockId.close()
server.close()
    
            
    



