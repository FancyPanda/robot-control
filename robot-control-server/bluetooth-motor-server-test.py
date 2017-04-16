#
# A Program used to test control of motors over bluetooth
#
##############<IMPORTS>#####################
import time
from dual_mc33926_rpi import motors, MAX_SPEED
import bluetooth
import RPi.GPIO as GPIO
##############<METHODS>#####################
def main():
    print("Initiating Motor Control Test")
    hostMACAddress = 'B8:27:EB:4A:5A:58'
    port = 3
    backlog = 1
    size = 1024
    s = bluetooth.BluetootSocket(bluetooth.RFCOMM)
    s.bind(hostMACAddress, port)
    s.listen(backlog)
    try:
        client, clientInfo = s.accept()
        motors.enable()
        motors.setSpeeds(0,0)
        if data:
            if data == "f":
                driveForward(2)
            elif data == "b":
                driveBackward(2)
            elif data == "q":
                client.close()
                s.close()
                quit
            else:
                stopMotors()
    except:
        print("Closing socket")
        client.close()
        s.close()
    finally:
        motors.setSpeeds(0,0)
        motors.disable()
def driveForward(time):
    test_forward_speeds = list(range(0,MAX_SPEED,1))+ \
    [MAX_SPEED] *200 + list(range(MAX_SPEED, 0, -1)) + [0]
    for s in test_forward_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)
def driveBackward(time):
    test_reverse_speeds = list(range(0,-MAX_SPEED,-1))+ \
    [-MAX_SPEED] *200 + list(range(-MAX_SPEED, 0, 1)) + [0]
    for s in test_reverse_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)
def stopMotors():
    motors.setSpeeds(0,0)
############################################
main()