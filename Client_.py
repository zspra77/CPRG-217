#Client.py
#Send a file to server
#Marcel Tozser March 14/21

import socket
import sys

s = socket.socket()
s.connect(("192.168.98.1",5000))
file = open ("system_info.txt", "rb")

line = file.read(1024)
print("Sending file...")
while (line):
    s.send(line)
    line = file.read(1024)
print("Finished sending file.")
      
s.close()

print("Connection closed.")
