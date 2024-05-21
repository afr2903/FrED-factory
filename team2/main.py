#!/usr/bin/env python3
"""
Main script to run the electronics station assembly proccess
"""
# Constants for features being used
USE_PLC = False
USE_SPEECH = False
USE_ARM = True
USE_GRIPPER = True

STATE_TO_RECORD = "BEFORE_PICK_WIRE1"

# Libraries imports
import socket
import time
from xarm.wrapper import XArmAPI
import os
import sys
from configparser import ConfigParser
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
if USE_GRIPPER:
    from tkinter import Tk, Scale, HORIZONTAL, Label, Button
    #from gripper_teleop import send_data
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

BOARD_TCP = [5.03, 39.81, 105.6, 0, 0, 0]
WIRE_TCP = [4.75, -130.62, 70.08, 0, 0, 0]

class ElectronicsStation:
    """Class to handle of components (arm, gripper, plc, etc) of the electronics station"""
    GRIPPER_STATES = {
        # [board, wire]
        "HOME": [111, 0],
        "PICK_ARDUINO": [31, 0],
        "PLACE_ARDUINO": [111, 0],
        "PICK_SHIELD": [45, 0],
        "PLACE_SHIELD":[111, 0],
        "PUSH_SHIELD": [111, 0],
        "PICK_DRIVER1": [111, 40],
        "PLACE_DRIVER1": [111, 0],
        "PICK_DRIVER2": [111, 40],
        "PLACE_DRIVER2": [75, 0],
        "PUSH_DRIVERS": [75, 40],
        "PICK_ASSEMBLY": [42, 0],
        "PLACE_ASSEMBLY": [75, 0],
        "PICK_WIRE": [111, 79],
        "FINISH_ROUTINE":[111, 40]
    }
    ARM_STATES = {
        # [x, y, z, roll, pitch, yaw, speed]
        "HOME": ["J", 0, -70, -20, 0, 90, 0, 30],
        "BEFORE_PICK_ARDUINO": ["J", 84.4, -4.4, -17.2, -9.2, -19.4, 94.4, 40],
        "PICK_ARDUINO": ["L", 11.4, 407.8, 164.2, -146.1, -0.8, 1.9, 30, "D"],
        #"PICK_ARDUINO": ["L", 49.733051, 463.314362, 79.767365, -145.079216, 1.329606, 0.099007, 10, "B"],
        "AFTER_PICK_ARDUINO": ["L", 17.6, 349.4, 241, -139.1, 0.2, -0.8, 40, "D"],
        "BEFORE_PLACE_ARDUINO": ["J", 60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 50],
        "SAFE_PLACE_ARDUINO": ["J", 59.7, -11, -24.9, 0.4, 37.3, 63.1, 35],
        "PLACE_ARDUINO": ["J", 60, -7.8, -23.8, 0.4, 32.3, 61.4, 15],
        "AFTER_PLACE_ARDUINO": ["J", 60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 30],
        "BEFORE_PICK_SHIELD": ["J", 111.5, 1.8, -17, 23.6, -14.9, -92.3, 40],
        "BEFORE_PICK_SHIELD_2": ["J", 107.7, 9.5, -26.5, 23.5, -7.9, -95.3, 20],
        #"PICK_SHIELD_0": ["J", 109.7, 12.1, -29.4, 35.8, -5.9, -108.1, 15],
        #"PICK_SHIELD": ["J", 111.4, 17.9, -30.3, 35.8, -16.6, -108.1, 15],
        #"PICK_SHIELD": ["L", -120.925568, 423.625702, 61.362858, 152.175184, 2.62598, -178.750342, 10, "B"],
        "PICK_SHIELD": ["L", -90.355515, 463.406311, 76.797081, 149.918246, 1.207738, -179.569843, 10, "B"],
        #"AFTER_PICK_SHIELD": ["J", 111.6, 13.4, -27.4, 35.8, -16.6, -108.2, 15],
        "AFTER_PICK_SHIELD": ["L", -96.649063, 441.632538, 119.793488, 146.556072, -0.534512, -178.378778, 10, "B"],
        "AFTER_PICK_SHIELD_1": ["J", 110.4, -6.9, -17.5, 35.8, -4.4, -108.4, 20],
        "BEFORE_PLACE_SHIELD": ["J", 55.4, -27.1, -20.3, 5.7, 40.5, 54.4, 30],
        #"SAFE_PLACE_SHIELD": ["J", 59, -17.9, -18.7, 5.3, 32.1, 54, 15],
        "SAFE_PLACE_SHIELD": ["J", 59.045994, -16.6568, -18.754456, 8.428725, 30.932788, 52.975506, 10],
        #"PLACE_SHIELD": ["J", 59.6, -13.8, -18.7, 6.8, 28.2, 52.3, 5],
        #"PLACE_SHIELD": ["L", 165.455994, 238.415649, 104.730347, -171.572384, -1.126435, -1.054987, 10, "B"],
        "PLACE_SHIELD": ["L", 166.866608, 238.500671, 104.299072, -172.7454, -0.211651, 0.152178, 10, "B"],
        "AFTER_PLACE_SHIELD": ["L", 165.455994, 238.415649, 134.730347, -171.572384, -1.126435, -1.054987, 10, "B"],
        #"AFTER_PLACE_SHIELD": ["J", 57.6, -19.9, -13.7, 3.1, 28.4, 53.6, 15],
        "BEFORE_PUSH_SHIELD": ["J", 56.120471, -16.822499, -16.341616, 4.443975, 35.192386, 53.043229, 10],
        #"PUSH_SHIELD": ["J", 55.7, -13.5, -16.5, 0.5, 34.4, 53.3, 45],
        "PUSH_SHIELD": ["L", 163.246918, 203.765717, 91.109421, 179.887491, 3.111562, -0.49303, 50, "B"],
        "AFTER_PUSH_SHIELD": ["L", 158.322281, 203.671539, 110.043457, -178.116822, 1.237875, 0.805865, 50, "B"],
        #"AFTER_PUSH_SHIELD": ["J", 55.7, -19.9, -16.5, 0.5, 34.4, 53.3, 15],
        #"PUSH_SHIELD_1": ["J", 55.7, -18, -11, 2.9, 28.9, 52.9, 45],
        "PUSH_SHIELD_1": ["L", 162.38858, 213.386688, 91.28334, 178.692702, 3.040229, -0.224829, 50, "B"],
        "AFTER_PUSH_SHIELD_1": ["L", 158.322281, 203.671539, 130.043457, -178.116822, 1.237875, 0.805865, 20, "B"],
        #"AFTER_PUSH_SHIELD_1": ["J", 55.7, -22, -11, 2.9, 28.9, 52.9, 45],
        #"PUSH_SHIELD_2": ["J", 55.7, -13.5, -16.5, 0.5, 34.4, 53.3, 45],
        #"AFTER_PUSH_SHIELD_2": ["J", 55.7, -19.9, -16.5, 0.5, 34.4, 53.3, 15],
        #"PUSH_SHIELD_3": ["J", 55.7, -18, -11, 2.9, 28.9, 52.9, 45],
        #"AFTER_PUSH_SHIELD_3": ["J", 55.7, -22, -11, 2.9, 28.9, 52.9, 45],
        "BEFORE_PICK_ASSEMBLY": ["J", 50.5, -26.2, -14.2, 1.6, 42.4, 229.4, 20],
        "PICK_ASSEMBLY": ["L", 165.6, 242.8, 96.7, 0.1, -179.1, -0.1, 10, "B"],
        "AFTER_PICK_ASSEMBLY": ["L", 165.6, 242.8, 116.7, 0.1, -179.1, -0.1, 10, "B"],
        "BEFORE_PLACE_ASSEMBLY": ["J", 2.5, -43.3, -12.8, 1, 57.1, 181, 20],
        "SAFE_PLACE_ASSEMBLY": ["L", 244.305725, 40.191769, 62.90258, -179.99916, -4.214105, 178.844708, 50, "B"],
        #"PLACE_ASSEMBLY": ["L", 244.305725, 40.191769, 37.90258, -179.99916, -4.214105, 178.844708, 10, "B"],
        "PLACE_ASSEMBLY": ["L", 243.833069, 40.104698, 37.80267, -179.984779, -3.509137, 178.904066, 10, "B"],
        "AFTER_PLACE_ASSEMBLY": ["L", 244.305725, 40.191769, 67.90258, -179.99916, -4.214105, 178.844708, 20, "B"],

        "BEFORE_PICK_DRIVER1": ["J", 57.3, -32, -18.2, 2.1, 45, 54.5, 30],
        "BEFORE_PICK_DRIVER1_2": ["J", 62.9, 25.2, -86.5, -1.6, 64.8, 64.1, 20],
        "BEFORE_PICK_DRIVER1_3": ["J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 15],
        "PICK_DRIVER1": ["J", 67.7, 53.6, -111.5, -23.3, 117, 65.6, 5],
        "AFTER_PICK_DRIVER1": ["J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 15],
        "AFTER_PICK_DRIVER1_2": ["J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20],
        "BEFORE_PLACE_DRIVER1": ["J", 43.1, 6.7, -35, -45.8, 105.3, 61.8, 15],
        #"PLACE_DRIVER1": ["J", 70.9, 16.9, -62.3, -22.6, 126, 70.2, 5],
        "PLACE_DRIVER1": ["L", 234.400604, 63.246693, 49.849049, 93.624226, 7.684223, -2.34397, 10, "W"],
        "AFTER_PLACE_DRIVER1": ["L", 234.400604, 63.246693, 59.849049, 93.624226, 7.684223, -2.34397, 10, "W"],
        #"AFTER_PLACE_DRIVER1": ["J", 71.6, 20.3, -66.2, -26.1, 130.4, 63.4, 15],
        "AFTER_PLACE_DRIVER1_2": ["J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20],
        "BEFORE_PICK_DRIVER2": ["J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 15],
        "PICK_DRIVER2": ["J", 67.7, 53.6, -111.5, -23.3, 117, 65.6, 5],

        "AFTER_PICK_DRIVER2": ["J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 15],
        "AFTER_PICK_DRIVER2_2": ["J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20],
        #"BEFORE_PLACE_DRIVER2": ["J", 71.2, 15.9, -59.8, -25.5, 127.7, 67.6, 15],
        "BEFORE_PLACE_DRIVER2": ["J", 43.2, -1.6, -31.3, -49.1, 110.7, 59.1, 15],
        #"PLACE_DRIVER2": ["J", 71.1, 16.2, -59.5, -25.5, 126.4, 67.7, 5],
        #"PLACE_DRIVER2": ["L", 155.649597, 246.34613, 114.931549, 93.542178, 5.443844, 1.686444, 10, "W"],
        "PLACE_DRIVER2": ["L", 234.031128, 43.744728, 49.815109, 92.178023, 6.663041, -1.457261, 10, "W"],
        "AFTER_PLACE_DRIVER2": ["L", 234.031128, 43.744728, 90.815109, 92.178023, 6.663041, -1.457261, 10, "W"],
        #"AFTER_PLACE_DRIVER2": ["J", 71.2, 15.9, -59.8, -25.5, 127.7, 67.6, 15],
        #"AFTER_PLACE_DRIVER2_2": ["J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20],
        "BEFORE_PUSH_DRIVERS": ["J", 10.9, -34.3, -10.9, 0.5, 48.2, 8.9, 20],
        #"SAFE_PUSH_DRIVERS": ["J", 55.4, -22.7, -13.5, 2.6, 33.9, 52.5, 10],
        #"SAFE_PUSH_DRIVERS": ["L", 153.657837, 212.775848, 48, -179.937052, 1.545267, -1.324507, 20, "B"],
        "SAFE_PUSH_DRIVERS": ["L", 248.399551, 7.757665, 48.735741, 179.882678, 3.054667, 1.653728, 20, "B"],
        #"PUSH_DRIVERS": ["J", 55.4, -15.1, -16, 2.6, 31.7, 52.6, 45],
        #"PUSH_DRIVERS": ["L", 153.657837, 212.775848, 99.344131, -179.937052, 1.545267, -1.324507, 40, "B"],
        "PUSH_DRIVERS": ["L", 248.399551, 7.757665, 32.735741, 179.882678, 3.054667, 1.653728, 40, "B"],
        "AFTER_PUSH_DRIVERS": ["L", 248.399551, 7.757665, 48.735741, 179.882678, 3.054667, 1.653728, 20, "B"],
        #"AFTER_PUSH_DRIVERS": ["L", 153.657837, 212.775848, 125.344131, -179.937052, 1.545267, -1.324507, 20, "B"],
        #"AFTER_PUSH_DRIVERS": ["J", 55.4, -22.7, -13.5, 2.6, 33.9, 52.5, 10],
        #"PUSH_DRIVERS_2": ["J", 55.4, -15.1, -16, 2.6, 31.7, 52.6, 45],
        #"AFTER_PUSH_DRIVERS_2": ["J", 55.4, -22.7, -13.5, 2.6, 33.9, 52.5, 10],
        #"PICK_ASSEMBLY": ["L", 163.859833, 251.218689, 100.386856, -178.933172, -2.240265, -179.576833, 10, "B"],
        "BEFORE_PICK_WIRE1": ["J", 57.3, -32, -18.2, 2.1, 45, 54.5, 20],
        "PICK_WIRE1": ["J", 34.4, -4.4, -35, 13.7, 57.6, 114.8, 10],
        "FINISH_ROUTINE": ["J", 0, -70, -20, 0, 90, 0, 30]
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

        self.arduino_counter = 0

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
        x, y, z, roll, pitch, yaw, speed = self.ARM_STATES[state][1:8]
        lineal = self.ARM_STATES[state][0] == "L"
        print(f"Sending arm to state: {state}")
        if lineal:
            tcp = self.ARM_STATES[state][8]
            if tcp == "B":
                self.arm.set_tcp_offset(BOARD_TCP)
            elif tcp == "W":
                self.arm.set_tcp_offset(WIRE_TCP)
            else:
                self.arm.set_tcp_offset([0,0,0,0,0,0])
            self.arm.set_mode(0) # Position control
            self.arm.set_state(state=0)
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

    def record_state(self, state):
        """Record a new state for the arm and gripper"""
        print(f"Recording state: {state}")
        self.arm.set_mode(2) # Joint teaching mode
        self.arm.set_state(0)
        print("The arm is now in MANUAL mode, press enter to record the position...")
        input()
        print("Do you want to record a joint or lineal position? (J/L)")
        movement_type = input()
        if movement_type.upper() == "J": # Joint position
            joint_position = self.arm.get_servo_angle()
            print("Joint position recorded, paste the following line in the ARM_STATES dictionary:")
            print(f"\"{state}\": [\"J\", {joint_position[1][0]}, {joint_position[1][1]}, {joint_position[1][2]}, {joint_position[1][3]}, {joint_position[1][4]}, {joint_position[1][5]}, 10],")
        
        elif movement_type.upper() == "L": # Lineal position
            print("Which is the desired TCP, board or wire gripper? (B/W)")
            desired_tcp = input()
            if desired_tcp.upper() == "B":
                self.arm.set_tcp_offset(BOARD_TCP)
            elif desired_tcp.upper() == "W":
                self.arm.set_tcp_offset(WIRE_TCP)
            else:
                self.arm.set_tcp_offset([0,0,0,0,0,0])
            lineal_position = self.arm.get_position()
            print("Lineal position recorded, paste the following line in the ARM_STATES dictionary:")
            print(f"\"{state}\": [\"L\", {lineal_position[1][0]}, {lineal_position[1][1]}, {lineal_position[1][2]}, {lineal_position[1][3]}, {lineal_position[1][4]}, {lineal_position[1][5]}, 10, \"{desired_tcp.upper()}\"],")

        print("Do you want to continue the program? (Y/N)")
        continue_program = input()
        if continue_program.upper() == "N":
            print("The program has been stopped, type Ctrl+C to exit")
            self.arm.disconnect()
            sys.exit()
        else:
            self.arm.set_mode(0) # Position control
            self.arm.set_state(0)

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
                #self.current_state = "BEFORE_PICK_ARDUINO"
                self.current_state = "BEFORE_PICK_DRIVER1"

        elif self.current_state == "WAIT_SENSOR":
            self.plc_action_data = self.plc.db_read(1, 0, 14)
            if self.plc_action_data[0] == 0b00000001:
                time.sleep(2)
                self.current_state = "BEFORE_PICK_ARDUINO"
   
        elif self.current_state == "BEFORE_PICK_ARDUINO":
           self.send_arm_state(self.current_state)
           self.current_state = "PICK_ARDUINO"
        
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

            if self.current_state is STATE_TO_RECORD:
                self.record_state(STATE_TO_RECORD)
                self.current_state = self.list_states[self.list_states.index(self.current_state) + 1]
                return

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
        if item['error_code'] != 0:
            print("f")
            self.arm.disconnect()
            sys.exit()

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
