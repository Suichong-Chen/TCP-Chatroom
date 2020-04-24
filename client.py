# client
'''
1. read in 3 arguments: host address, port number, username: if any missing, print message and exit
2. connect to the port at the give host address
3. set up connection to be TCP and IPv4
4. read input messages from user and send them to the server
5. if receive the signal interrupt (SIGINT), close the client program
'''

import socket
import sys
import select

if len(sys.argv) != 4:
    print("should input host address, port number, and username")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])
user_name = str(sys.argv[3])

def user_prompt(message):
    sys.stdout.write("<You>")
    sys.stdout.write(message)
    sys.stdout.flush()

# creates connection to server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if (server < 0):
        perror("socket")
        exit()

# try to connect to the port at the given host address
try:
    server.connect((ip, port))
except:
    print("no connection")
    exit()

def run_clients(server):
    while True:
        sockets_list = [sys.stdin, server]

        read_sockets, write_sockets, error_sockets = select.select(sockets_list, [], [])
        
        for sock in read_sockets:
            if sock == server:  # receiving message from server
                msg = sock.recv(4096)
                if (msg != "SIGINT"):
                    print(msg)
                else:
                    exit()
            else:   # sending message to server
                msg = sys.stdin.readline()
                server.send(msg)
                user_prompt(msg)

run_clients(server)
server.close()

