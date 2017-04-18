##############<IMPORTS>##############
from bluetooth import *
from random import randint
import time
from pynput import keyboard
##############<Methods>##############
def on_press(key):
    if key == "q":
        client_socket.send(key)
        client_socket.close()
        print("Closing Socket")
        return False
    if key == keyboard.Key.esc:
        client_socket.send("q")
        client_socket.close()
        print("Closing Socket")
        return False
    try:
        print(str(key.char))
        client_socket.send(str(key.char))
    except AttributeError:
        print(str(key))
        client_socket.send(str(key))
def on_release(key):
    client_socket.send("turn that s*** off boi")
#############<MAIN>#################
# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:4A:A5:58", 3))
print("Link Established")
print("------------------------------------")
try:
    with keyboard.Listener(on_press = on_press, on_release=on_release) as listener:
         listener.join()
except Exception as e:
    print(str(e))
    print("Closing Client")
    client_socket.close()
