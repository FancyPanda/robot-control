#! /usr/bin/python2.7

"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez 
"""

#####################<IMPORTS>##############################
import bluetooth
from random import randint
####################<FUNCTIONS>############################
def formatData(data):
    p1 = 1
    p2 = data.index("]")
    p3 = p2+2 
    p4 = len(data)-1
    left_val = data[p1:p2] 
    right_val = data[p3:p4]
    return (left_val,right_val)

def getSensorValues():
    return "["+str(randint(0,10))+"]["+str(randint(0,10))+"]["+str(randint(0,10))+"]["+str(randint(0,10))+"]"
##########################################################




######################<MAIN CODE>#########################

hostMACAddress = 'B8:27:EB:21:DD:94' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
left_val = 0
right_val = 0
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
	    formated_data = formatData(data)
            left_val = formated_data[0]
            right_val = formated_data[1] 
            print("DRIVE VALUES (L, R)") 
	    print(left_val, right_val)
	    sensor_values = getSensorValues()
	    print("SENSOR VALUES (FL, FR, BL, BR)")
            print(sensor_values)
            client.send(sensor_values) # Echo back to client
except: # Exception as e:
#    print(str(e))	
    print("Closing socket")
    client.close()
    s.close()

    
