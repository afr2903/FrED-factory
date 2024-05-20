#!/usr/bin/env python3

"""
Debugging the code to receive the camera feedback
"""

import os
import sys
import time
import socket

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.reset(wait=True)

print("Arm safe position")

arm.set_servo_angle(angle=[0.0, -80.0, -10.0, 0.0, 90.0, 0.0], speed=50, wait=True, radius=20.0)
time.sleep(5)
                            
print("Arm ready, moving to inspection position...")

arm.set_position(x=-69.6, y=243.5, z=96.8, roll=179.8, pitch=0.8, yaw=92.0, speed=100, wait=True)

time.sleep(2)

print("Sending trigger...")

arm.set_cgpio_digital(2, 1)

print("Trigger sent, waiting for camera feedback...")

time.sleep(1)

HOST = "192.168.1.125"  # The server's hostname or IP address
PORT = 20000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.settimeout(None)
    s.sendall(b"cmd Online")
    s.sendall(b"cmd trigger")
    data = s.recv(24) #IMPORTANTE REVISAR EL TAMAÑO DEL STRING PARA SELECCIONAR LOS BYTES ADECUADOS

print(f"Received2 {data!r}")

str1 = data.decode('UTF-8')
t=str1.split(" ")   #IMPORTANTE REVISAR CUAL ES EL CARACTER USADO PARA DELIMITAR CADA DATO
x, y, th = float(t[0]), float(t[1]), float(t[2])

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 1024

x_centered = x - IMAGE_WIDTH / 2
y_centered = y - IMAGE_HEIGHT / 2

x_mm = x_centered / 8.9790
y_mm = y_centered / 8.9790

ARM_OFFSET_X = 90
x_mm = x_mm + ARM_OFFSET_X

ARM_OFFSET_Y = 3
y_mm = y_mm + ARM_OFFSET_Y

print(f"X: {x_mm} Y: {y_mm} Th: {th}")

print("Moving to the detected object...")

arm.set_position(x=-69.6 + x_mm, y=243.5 + y_mm, z=96.8, roll=179.8, pitch=0.8, yaw=92.0 + th, speed=100, wait=True)

print("Object reached")


arm.disconnect()