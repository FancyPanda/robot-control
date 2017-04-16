##############<IMPORTS>##############
from bluetooth import *
from random import randint
import time
##############<Methods>##############
def getDriveValues():
    val_right = 0
    val_left = 0
    ######<method 1 (random vals)>##
    #val_right = randint(0,100)
    #val_left = randint(0,100)
    ###############################
    drive_values =(val_left, val_right) 
    return drive_values
def formatData(data):
    p1 =1
    p2=data.index("]")
    p3 = p2+2
    p4 = p3+data[p3:].index("]")
    p5 = p4+2
    p6 = p5+data[p5:].index("]")
    p7 = p6+2
    p8 = len(data)-1
    return data[p1:p2], data[p3:p4], data[p5:p6], data[p7:p8]
#############<MAIN>#################
# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:4A:A5:58", 3))
print("Link Established")
print("------------------------------------")

try:
    while 1: 
        drive_values = getDriveValues()
        print("DRIVE VALUES (L,R):")
        print(drive_values[0], drive_values[1])
        drive_values = "["+str(drive_values[0])+"]["+str(drive_values[1])+"]"
        client_socket.send(drive_values)
        input_vals = client_socket.recv(1024).decode('ascii')
        if input_vals: 
            front_left, front_right, back_left, back_right = formatData(input_vals)
            print("SENSOR VALUES (FL,FR,BL,BR)")
            print("FL: "+front_left+", FR: "+front_right+", BL: "+back_left+", BR: "+back_right)
        time.sleep(.01)
except: #Exception as e:
#    print(str(e))
    print("Closing Client")
    client_socket.close()
