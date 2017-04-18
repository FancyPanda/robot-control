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
#   hostMACAddress = 'B8:27:EB:4A:5A:58'
    port = 3
    backlog = 1
    size = 1024
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind(("",port)) # ((hostMACAddress, port))
    s.listen(backlog)
    motors.enable()
    motors.setSpeeds(0,0)
    try:
        client, clientInfo = s.accept()
        while(1):
            print("test1")
            data = client.recv(1024)
            if data:
                if data == "w":
                    print("forward")
                    driveForward(MAX_SPEED/2)
                elif data == "s":
                    print("reverse")
                    driveBackward(MAX_SPEED/2)
                elif data == "q":
                    print("quit")
                    client.close()
                    s.close()
                    break
                else:
                    print('stopped')
                    stopMotors()
            else:
                print('no data')
                stopMotors()
                time.sleep(0.005)
            time.sleep(1/60)
            print("cyle")
    except Exception as e:
        print(str(e))
        print("Closing socket")
        motors.setSpeeds(0,0)
        motors.disable()
        client.close()
        s.close()
        quit
    finally:
#        print("closing test")
        motors.setSpeeds(0,0)
        motors.disable()
#        client.close()
#        s.close()
#        quit
def driveForward(speed):
    motors.motor1.setSpeed(speed)
    time.sleep(0.005)
def driveBackward(speed):
    motors.motor1.setSpeed(-speed)
    time.sleep(0.005)
def stopMotors():
    motors.setSpeeds(0,0)
############################################
main()
