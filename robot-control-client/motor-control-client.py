##############<IMPORTS>##############
from bluetooth import *
from random import randint
import time
from pynput import keyboard
##############<Methods>##############
def on_press(key):
    if key == keyboard.Key.esc:
        client_socket.close()
        print("Closing Socket")
        return False
    client_socket.send(key.char)
#############<MAIN>#################
# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:4A:A5:58", 3))
print("Link Established")
print("------------------------------------")
try:
    with keyboard.Listener(
         on_press = on_press) as listener:
         listener.join()
         client_socket.close()
except: #Exception as e:
#    print(str(e))
    print("Closing Client")
    client_socket.close()
