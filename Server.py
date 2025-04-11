#Server.py
#Receive a file from client
#Marcel Tozser March 14/21

import socket
import sys

s = socket.socket()
s.bind(("192.168.98.1",5000))

s.listen(5) 

print("Waiting for connection...")

connection, address = s.accept()

file = open("ReceivedFile.txt","wb")

while (True):       
    
    line = connection.recv(1024)
    print("Receiving file...")
    while (line): 
        file.write(line)
        line = connection.recv(1024)
    break

file.close()
print("Done receiving file")

s.close()
print("Connection closed.")
