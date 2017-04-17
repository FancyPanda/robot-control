##############<IMPORTS>##############
from bluetooth import *
from random import randint
import time
##############<Methods>##############
#############<MAIN>#################
# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:4A:A5:58", 3))
print("Link Established")
print("------------------------------------")

try:
    while 1:
        text = input("Send data!")
        if text =="q":
            print("Quitting...")
            client_socket.close()
            quit 
        client_socket.send(text)
except: #Exception as e:
#    print(str(e))
    print("Closing Client")
    client_socket.close()
