#!/usr/bin/env python3
"""
Main script to run the electronics station assembly proccess
"""
# Constants for features being used
USE_PLC = False
USE_SPEECH = True
USE_ARM = True
USE_GRIPPER = True

# Libraries imports
import socket
import time
from xarm.wrapper import XArmAPI
import os
import sys
from configparser import ConfigParser
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
if USE_PLC:
    import snap7
if USE_SPEECH:
    import pygame

# IP addresses
PLC_IP = '192.168.1.101'
XARM_IP = '192.168.1.201'
UDP_IP = "192.168.2.23"

UDP_PORT = 1234            # Port number
MESSAGE = ""               # Initialize message

RACK = 0
SLOT = 1

class ElectronicsStation:
    """Class to handle of components (arm, gripper, plc, etc) of the electronics station"""
    GRIPPER_STATES = {
        # [board, wire]
        "HOME": [85, 0],
        "PICK_ARDUINO": [18, 0],
        "PLACE_ARDUINO": [85, 0],
        "PICK_SHIELD": [37, 0],
        "PLACE_SHIELD":[85, 0],
        "PUSH_SHIELD": [85, 0],
        "PICK_DRIVER1": [85, 40],
        "PLACE_DRIVER1": [85, 0],
        "PICK_DRIVER2": [85, 40],
        "PLACE_DRIVER2": [85, 0],
        "PUSH_DRIVERS": [85, 40],
        "PICK_WIRE": [85, 79],
        "FINISH_ROUTINE":[85, 40]
    }
    ARM_STATES = {
        # [x, y, z, roll, pitch, yaw, speed]
        "HOME": [0, -70, -20, 0, 90, 0, 30], #JOINT
        "BEFORE_PICK_ARDUINO": [84.4, -4.4, -17.2, -9.2, -19.4, 94.4, 30], #JOINT
        "PICK_ARDUINO": [11.4, 407.8, 164.2, -146.1, -0.8, 1.9, 20], #LINEAR
        "AFTER_PICK_ARDUINO": [17.6, 349.4, 241, -139.1, 0.2, -0.8, 30], #LINEAR
        "BEFORE_PLACE_ARDUINO": [60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 30], #JOINT
        "SAFE_PLACE_ARDUINO": [59.7, -11, -24.9, 0.4, 37.3, 63.1, 15], #JOINT
        "PLACE_ARDUINO": [60, -7.8, -23.8, 0.4, 32.3, 61.4, 15], #JOINT
        #"PLACE_ARDUINO": [169.3, 290, 205.2, 178.9, -5.7, -1.3, 15], #LINEAR
        "AFTER_PLACE_ARDUINO": [60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 30], #JOINT
        "BEFORE_PICK_SHIELD":[111.5, 1.8, -17, 23.6, -14.9, -92.3, 30], #JOINT
        "BEFORE_PICK_SHIELD_2": [107.7, 9.5, -26.5, 23.5, -7.9, -95.3, 20], #JOINT
        #"PICK_SHIELD": [-86.7, 372.2, 146.1, 0.8, -172.9, -45.6, 15], #LINEAR
        "PICK_SHIELD_0": [109.7, 12.1, -29.4, 35.8, -5.9, -108.1, 15], #JOINT
        "PICK_SHIELD": [111.4, 17.9, -30.3, 35.8, -16.6, -108.1, 15], #JOINT
        "AFTER_PICK_SHIELD": [111.6, 13.4, -27.4, 35.8, -16.6, -108.2, 15], #JOINT
        "AFTER_PICK_SHIELD_1": [110.4, -6.9, -17.5, 35.8, -4.4, -108.4, 20], #JOINT
        #"BEFORE_PLACE_SHIELD":[57.2, -5.9, -18.6, 3, 21.7, 52.8, 30], #JOINT
        #"BEFORE_PLACE_SHIELD_1":[60.7, -0.1, -14.8, 6.1, 7.3, 53.7, 20], #JOINT
        #"PLACE_SHIELD": [156.9, 265.4, 147.1, -173.6, -1.6, -4.2, 15], #LINEAR
        "BEFORE_PLACE_SHIELD":[55.4, -27.1, -20.3, 5.7, 40.5, 54.4, 20], #JOINT
        "SAFE_PLACE_SHIELD": [59, -17.9, -18.7, 5.3, 32.1, 54, 15], #JOINT
        "PLACE_SHIELD": [59.7, -16.5, -14.8, 10.4, 21.9, 51.5, 5], #JOINT
        "AFTER_PLACE_SHIELD": [57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15], #JOINT
        "PUSH_SHIELD": [57.2, -13.6, -16.5, 3.2, 31.2, 52.7, 15], #JOINT
        "AFTER_PUSH_SHIELD": [57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15], #JOINT
        "PUSH_SHIELD_1": [57.9, -12, -17.9, 2.3, 32.7, 53.6, 45], #JOINT
        "AFTER_PUSH_SHIELD_1": [57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15], #JOINT
        "PUSH_SHIELD_2": [56.1, -13.5, -14, 2.2, 28.8, 53.6, 45], #JOINT
        "AFTER_PUSH_SHIELD_2": [57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15], #JOINT
        "PUSH_SHIELD_3": [57.9, -12, -17.9, 2.3, 32.7, 53.6, 45], #JOINT
        "AFTER_PUSH_SHIELD_3": [57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15], #JOINT
        "BEFORE_PICK_DRIVER1": [57.3, -32, -18.2, 2.1, 45, 54.5, 30], #JOINT
        "BEFORE_PICK_DRIVER1_2": [62.9, 25.2, -86.5, -1.6, 64.8, 64.1, 20], #JOINT
        "BEFORE_PICK_DRIVER1_3": [66.9, 51.7, -111, -22.5, 119.8, 64.9, 15], #JOINT
        "PICK_DRIVER1": [67.5, 54.1, -111.3, -23.2, 115.2, 65.4, 5], #JOINT
        "AFTER_PICK_DRIVER1": [66.9, 51.7, -111, -22.5, 119.8, 64.9, 15], #JOINT
        "AFTER_PICK_DRIVER1_2": [72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20], #JOINT
        "BEFORE_PLACE_DRIVER1": [72.3, 25.5, -69.9, -26, 134.6, 63.5, 15], #JOINT
        "PLACE_DRIVER1": [71.4, 21.9, -65.7, -25.8, 127.8, 63.4, 5], #JOINT
        "AFTER_PLACE_DRIVER1": [72.3, 25.5, -69.9, -26, 134.6, 63.5, 15], #JOINT
        "AFTER_PLACE_DRIVER1_2": [72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20], #JOINT
        "BEFORE_PICK_DRIVER2": [66.9, 51.7, -111, -22.5, 119.8, 64.9, 15], #JOINT
        "PICK_DRIVER2": [67.5, 54.1, -111.3, -23.2, 115.2, 65.4, 5], #JOINT
        "AFTER_PICK_DRIVER2": [66.9, 51.7, -111, -22.5, 119.8, 64.9, 15], #JOINT
        "AFTER_PICK_DRIVER2_2": [72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20], #JOINT
        "BEFORE_PLACE_DRIVER2": [70.4, 15.9, -59.6, -25.5, 127.7, 67.7, 15], #JOINT
        "PLACE_DRIVER2": [70.5, 16, -58.7, -24.5, 124.1, 67.6, 5], #JOINT
        "AFTER_PLACE_DRIVER2": [70.4, 15.9, -59.6, -25.5, 127.7, 67.7, 15], #JOINT
        "AFTER_PLACE_DRIVER2_2": [72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20], #JOINT
        "BEFORE_PUSH_DRIVERS": [57.3, -32, -18.2, 2.1, 45, 54.5, 20], #JOINT
        "SAFE_PUSH_DRIVERS": [56.9, -17.3, -18.5, 2.1, 31.3, 54.5, 10], #JOINT
        "PUSH_DRIVERS": [56.4, -13, -17.3, 2.1, 30.2, 54.5, 45], #JOINT
        "AFTER_PUSH_DRIVERS": [56.9, -17.3, -18.5, 2.1, 31.3, 54.5, 15], #JOINT
        "PUSH_DRIVERS_2": [56.4, -13, -17.3, 2.1, 30.2, 54.5, 45], #JOINT
        "AFTER_PUSH_DRIVERS_2": [56.9, -17.3, -18.5, 2.1, 31.3, 54.5, 15], #JOINT
        "BEFORE_PICK_WIRE1": [57.3, -32, -18.2, 2.1, 45, 54.5, 20], #JOINT
        "PICK_WIRE1": [34.4, -4.4, -35, 13.7, 57.6, 114.8, 10],
        "FINISH_ROUTINE":[0, -70, -20, 0, 90, 0, 30] #JOINT
    }
    def __init__(self):
        """Initialize communications"""
        # PLC configs
        if USE_PLC:
            self.plc = snap7.client.Client()
            self.plc.connect(PLC_IP, RACK, SLOT)
            self.plc_action_data = None
       # self.plc_light_data = None

        # Arm configs
        self.arm = XArmAPI(XARM_IP, do_not_open=True)
        self.arm.register_error_warn_changed_callback(self.handle_err_warn_changed)
        self.arm.connect()

        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0) # Position control
        self.arm.set_state(state=0)

        self.list_states = list(self.ARM_STATES.keys())

        # Gripper configs
        if USE_GRIPPER:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Speech feedback
        if USE_SPEECH:
            pygame.mixer.init()
        self.current_state = "HOME"

    def send_gripper_state(self, state):
        """Send the data to the ESP32 via socket"""
        if not USE_GRIPPER:
            return
        board_position, wire_position = self.GRIPPER_STATES[state]
        print(f"Sending gripper to state: {state}")
        # Send board finger position
        message = 'b' + str(board_position)
        self.sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(0.2)
        # Send wire finger position
        message = 'w' + str(wire_position)
        self.sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(0.2)

    def send_arm_state(self, state, lineal=False):
        """Send the data to the xArm"""
        x, y, z, roll, pitch, yaw, speed = self.ARM_STATES[state]
        print(f"Sending arm to state: {state}")
        if lineal:
            self.arm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, speed=speed, wait=True)
        else:
            self.arm.set_servo_angle(angle=[x, y, z, roll, pitch, yaw], speed=speed, wait=True)
    
    def static_speech_feedback(self, state):
        """Play the static audio files with feedback"""
        if not USE_SPEECH:
            return
        file_path = f"speech-feedback/{state}.opus"
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def run(self):
        """Main loop of the electronics station"""
        if self.current_state == "HOME":
           # self.plc_light_data = bytearray(0b00001000)
            #self.plc.db_write(1,0, self.plc_light_data) 
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if USE_PLC:
                self.current_state = "WAIT_SENSOR"
            else:
                self.current_state = "BEFORE_PICK_ARDUINO"
                #self.current_state = "BEFORE_PICK_DRIVER1"

        elif self.current_state == "WAIT_SENSOR":
            self.plc_action_data = self.plc.db_read(1, 0, 2)
            if self.plc_action_data[0] == 0b00000001:
                time.sleep(2)
                self.current_state = "BEFORE_PICK_ARDUINO"
   
        elif self.current_state == "BEFORE_PICK_ARDUINO":
            self.send_arm_state(self.current_state)
            self.current_state = "PICK_ARDUINO"
        
        elif self.current_state == "PICK_ARDUINO":
            self.static_speech_feedback(self.current_state)
            self.send_arm_state(self.current_state, lineal=True)
            self.send_gripper_state(self.current_state)
            time.sleep(1)
            self.current_state = "AFTER_PICK_ARDUINO"

        elif self.current_state == "AFTER_PICK_ARDUINO":
            self.send_arm_state(self.current_state, lineal=True)
            self.current_state = "BEFORE_PLACE_ARDUINO"

        elif self.current_state == "BEFORE_PICK_WIRE1":
            self.send_arm_state(self.current_state)
            self.current_state = "HOME"

        elif self.current_state == "FINISH_ROUTINE":
            self.plc_action_data = self.plc.db_read(1, 0, 2)
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if self.plc_action_data[0] == 0b00000000:
                time.sleep(2)
                self.current_state = "HOME"

        else:
            if self.current_state not in self.ARM_STATES:
                print(f"Invalid state: {self.current_state}")

            if self.current_state in self.GRIPPER_STATES:
                self.static_speech_feedback(self.current_state)
                self.send_arm_state(self.current_state)
                self.send_gripper_state(self.current_state)
                time.sleep(1)
            else:
                self.send_arm_state(self.current_state)
            # Get next state index
            self.current_state = self.list_states[self.list_states.index(self.current_state) + 1]

        time.sleep(0.1)

    def handle_err_warn_changed(self, item):
        """Handle error and warning messages"""
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

    def close(self):
        """Close all connections"""
        self.sock.close()

if __name__ == '__main__':
    station = ElectronicsStation()

    while True:
        try:
            station.run()
        except KeyboardInterrupt:
            station.close()
            break
