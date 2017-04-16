#! /usr/bin/python2.7

"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez 
"""

#####################<IMPORTS>##############################
import bluetooth
from random import randint
import RPi.GPIO as GPIO
import time

###################<GLOBAL VARS>###########################
ULTRA_FL = (23,24)
ULTRA_FR = (23,24)
ULTRA_BL = (23,24)
ULTRA_BR = (23,24)
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
    dist_fl=distance(ULTRA_FL)
    dist_fr=distance(ULTRA_FR)
    dist_bl=distance(ULTRA_BL)
    dist_br=distance(ULTRA_BR)
    return "["+str(dist_fl)+"]["+str(dist_fr)+"]["+str(dist_bl)+"]["+str(dist_br)+"]"
def setUpUltrasonicSensor(sensor):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor[0], GPIO.OUT)
    GPIO.setup(sensor[1], GPIO.IN)
def distance(sensor):
    TRIG = sensor[0]
    ECHO = sensor[1]
    # set Trigger to HIGH
    GPIO.output(TRIG, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = round(((TimeElapsed * 34300) / 2),2)
 
    return distance

##########################################################




######################<MAIN CODE>#########################

hostMACAddress = 'B8:27:EB:4A:A5:58' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
left_val = 0
right_val = 0
setUpUltrasonicSensor(ULTRA_FL)
setUpUltrasonicSensor(ULTRA_FR)
setUpUltrasonicSensor(ULTRA_BL)
setUpUltrasonicSensor(ULTRA_BR)
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

    
