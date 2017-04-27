##############<IMPORTS>##############
from bluetooth import *
from pynput import keyboard
from random import randint
import time
import threading
##############<GLOBAL VARS>##########
MAX_SPEED = 480  # <-- figure out how to make it get instantiated before call to main
CUR_SPEED = 240
##############<Methods>##############
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
def on_press(key):
    global CUR_SPEED
    parsed_vals = "[0][0]"
    print(key)
    if key.char =='q':
        client_socket.send(key)
        client_socket.close()
        print("Socket Closed")
        return False
    elif key == keyboard.Key.esc:
        client_socket.send("q")
        client_socket.close()
        print("Socket Closed")
        return False
    elif key.char== 'w':
        parsed_vals =parse_motor_values(CUR_SPEED, CUR_SPEED)
    elif key.char == 's':
        parsed_vals =parse_motor_values(-CUR_SPEED, -CUR_SPEED)
    elif key.char == 'a':
        parsed_vals =parse_motor_values(-CUR_SPEED, CUR_SPEED)
    elif key.char == 'd':
        parsed_vals =parse_motor_values(CUR_SPEED, -CUR_SPEED)
    elif key.char == '-':
        if(CUR_SPEED>0):
            CUR_SPEED -= 10
    elif key.char== '=':
        if(CUR_SPEED<MAX_SPEED):
            CUR_SPEED += 10
    print("DRIVE VALUES (L,R):")
    print(parsed_vals)
    client_socket.send(parsed_vals)
def on_release(key):
    print("key released")
    client_socket.send('stop')
def parse_motor_values(val1,val2):
    drive_values = "["+str(val1)+"]["+str(val2)+"]"
    return drive_values
def keyboard_thread():
    with keyboard.Listener(on_press = on_press, onr_release = on_release) as listener:
        listener.join()
    client_socket.close()
    quit
def sensor_thread():
    while 1:    #<-- figure out how to get ultrasonic values and control motors
        input_vals = "[0][0][0][0]" #client_socket.recv(1024).decode('ascii')
        if input_vals: 
            front_left, front_right, back_left, back_right = formatData(input_vals)
            print("SENSOR VALUES (FL,FR,BL,BR)")
            print("FL: "+front_left+", FR: "+front_right+", BL: "+back_left+", BR: "+back_right)
        time.sleep(20/60)

#############<MAIN>#################
# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:4A:A5:58", 3))
print("Link Established")
print("------------------------------------")

try:
    with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()
    #s_thread = threading.Thread(target=sensor_thread)
    #s_thread.start()
    #k_thread = threading.Thread(target=keyboard_thread)
    #k_thread.daemon = True
    #k_thread.start()
    #s_thread.join()
    #k_thread.join()
except Exception as e:
    print(str(e))
    print("Closing Client")
    client_socket.close()
