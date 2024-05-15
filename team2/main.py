#!/usr/bin/env python3
"""
Main script to run the electronics station assembly proccess
"""
# Libraries imports
import socket
import time
from xarm.wrapper import XArmAPI
import os
import sys
import snap7
import pygame
from configparser import ConfigParser
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

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
        "HOME": [85, 40],
        "PICK_ARDUINO": [18, 40],
        "PLACE_ARDUINO": [85, 40],
        "PICK_WIRE": [85, 79],
        "PICK_SHIELD": [37, 40],
        "PLACE_SHIELD":[85, 40],
        "FINISH_ROUTINE":[85, 40]
    }
    ARM_STATES = {
        # [x, y, z, roll, pitch, yaw, speed]
        "HOME": [0, -70, -20, 0, 90, 0, 30], #JOINT
        "BEFORE_PICK_ARDUINO": [84.4, -4.4, -17.2, -9.2, -19.4, 94.4, 30], #JOINT
        "PICK_ARDUINO": [11.4, 407.8, 164.2, -146.1, -0.8, 1.9, 20], #LINEAR
        "AFTER_PICK_ARDUINO": [17.6, 349.4, 241, -139.1, 0.2, -0.8, 30], #LINEAR
        "BEFORE_PLACE_ARDUINO": [59.8, 0.8, -23.6, -8.9, 24.6, 68.8, 30], #JOINT
        "PLACE_ARDUINO": [166.3, 287.4, 124.2, 176.8, 0.3, 1.5, 20], #LINEAR
        "AFTER_PLACE_ARDUINO": [166.3, 287.4, 165, 176.8, 0.3, 1.5, 20], #LINEAR
        "BEFORE_PICK_SHIELD":[111.5, 1.8, -17, 23.6, -14.9, -92.3, 30], #JOINT
        "BEFORE_PICK_SHIELD_2": [107.7, 9.5, -26.5, 23.5, -7.9, -95.3, 20], #JOINT
        "PICK_SHIELD": [-86.7, 372.2, 146.1, 0.8, -172.9, -45.6, 15], #LINEAR
        "PICK_SHIELD_0": [109.7, 12.1, -29.4, 35.8, -5.9, -108.1, 15], #JOINT
        "PICK_SHIELD_1": [111.4, 17.9, -30.3, 35.8, -16.6, -108.1, 15], #JOINT
        "AFTER_PICK_SHIELD": [111.6, 13.4, -27.4, 35.8, -16.6, -108.2, 15], #JOINT
        "AFTER_PICK_SHIELD_1": [110.4, -6.9, -17.5, 35.8, -4.4, -108.4, 20], #JOINT
        "BEFORE_PLACE_SHIELD":[57.2, -5.9, -18.6, 3, 21.7, 52.8, 30], #JOINT
        "BEFORE_PLACE_SHIELD_1":[60.7, -0.1, -14.8, 6.1, 7.3, 53.7, 20], #JOINT
        #"PLACE_SHIELD": [156.9, 265.4, 147.1, -173.6, -1.6, -4.2, 15], #LINEAR
        "BEFORE_PLACE_SHIELD_T":[55.4, -27.1, -20.3, 5.7, 40.5, 54.4, 20], #JOINT
        "PLACE_SHIELD": [59.1, -13.8, -17.1, 4.8, 21.5, 56.9, 15], #JOINT
        "AFTER_PLACE_SHIELD": [60, -3.3, -15.9, 3.7, 13, 55.3, 15], #JOINT
        "AFTER_PLACE_SHIELD_T":[55.4, -27.1, -20.3, 5.7, 40.5, 54.4, 20], #JOINT
        "FINISH_ROUTINE":[0, -70, -20, 0, 90, 0, 30] #JOINT
    }
    def __init__(self):
        """Initialize communications"""
        # PLC configs
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

        # Gripper configs
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Speech feedback
        pygame.mixer.init()
        self.current_state = "HOME"

    def send_gripper_state(self, state):
        """Send the data to the ESP32 via socket"""
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
    
            self.plc_action_data = self.plc.db_read(1, 0, 2)
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if self.plc_action_data[0] == 0b00000001:
                time.sleep(2)
                #self.plc_light_data = 0b00000001
                #self.plc.db_write(1,0,self.plc_action_data)
                #self.current_state = "BEFORE_PICK_ARDUINO"
                self.current_state = "BEFORE_PICK_SHIELD"
   
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

        elif self.current_state == "BEFORE_PLACE_ARDUINO":
            self.send_arm_state(self.current_state)
            self.current_state = "PLACE_ARDUINO"
        
        elif self.current_state == "PLACE_ARDUINO":
            self.static_speech_feedback(self.current_state)
            self.send_arm_state(self.current_state, lineal=True)
            self.send_gripper_state(self.current_state)
            time.sleep(1)
            self.current_state = "AFTER_PLACE_ARDUINO"

        elif self.current_state == "AFTER_PLACE_ARDUINO":
            self.send_arm_state(self.current_state, lineal=True)
            self.current_state = "BEFORE_PICK_SHIELD"

        elif self.current_state == "BEFORE_PICK_SHIELD":
            self.send_arm_state(self.current_state)
            self.current_state = "BEFORE_PICK_SHIELD_2"
        
        elif self.current_state == "BEFORE_PICK_SHIELD_2":
            self.send_arm_state(self.current_state)
            self.current_state = "PICK_SHIELD_0"
        
        elif self.current_state == "PICK_SHIELD_0":
            self.static_speech_feedback("PICK_SHIELD")
            self.send_arm_state(self.current_state)
            self.current_state = "PICK_SHIELD_1"
        
        elif self.current_state == "PICK_SHIELD_1":
            self.send_arm_state(self.current_state)
            self.send_gripper_state("PICK_SHIELD")
            time.sleep(1)
            self.current_state = "AFTER_PICK_SHIELD"

        elif self.current_state == "PICK_SHIELD":
            self.static_speech_feedback(self.current_state)
            self.send_arm_state(self.current_state, lineal=True)
            self.send_gripper_state(self.current_state)
            time.sleep(1)
            self.current_state = "AFTER_PICK_SHIELD"
        
        elif self.current_state == "AFTER_PICK_SHIELD":
            self.send_arm_state(self.current_state)
            self.current_state = "AFTER_PICK_SHIELD_1"
        
        elif self.current_state == "AFTER_PICK_SHIELD_1":
            self.send_arm_state(self.current_state)
            self.current_state = "BEFORE_PLACE_SHIELD_T"

        elif self.current_state == "BEFORE_PLACE_SHIELD":
            self.send_arm_state(self.current_state)
            self.current_state = "BEFORE_PLACE_SHIELD_1"
        
        elif self.current_state == "BEFORE_PLACE_SHIELD_1":
            self.send_arm_state(self.current_state)
            self.current_state = "PLACE_SHIELD"
        
        elif self.current_state == "BEFORE_PLACE_SHIELD_T":
            self.send_arm_state(self.current_state)
            self.current_state = "PLACE_SHIELD"

        elif self.current_state == "PLACE_SHIELD":
            self.static_speech_feedback(self.current_state)
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            time.sleep(1)
            self.current_state = "AFTER_PLACE_SHIELD_T"

        elif self.current_state == "AFTER_PLACE_SHIELD":
            self.send_arm_state(self.current_state)
            self.current_state = "FINISH_ROUTINE"
        
        elif self.current_state == "AFTER_PLACE_SHIELD_T":
            self.send_arm_state(self.current_state)
            self.current_state = "FINISH_ROUTINE"

        elif self.current_state == "FINISH_ROUTINE":
            self.plc_action_data = self.plc.db_read(1, 0, 2)
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if self.plc_action_data[0] == 0b00000000:
                time.sleep(2)
                self.current_state = "HOME"
          



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
