#!/usr/bin/env python3
"""
Main script to run the electronics station assembly proccess
"""
# Constants for features being used
USE_PLC = True
USE_SPEECH = True
USE_ARM = True
USE_GRIPPER = True
USE_CAMERA = False

STATE_TO_RECORD = [
]

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
    import threading
    import pygame

# IP addresses
HOST = "192.168.0.128"  # The server's hostname or IP address
PORT = 20000  # The port used by the server
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
        "HOME": [85, 0], #100
        "PICK_ARDUINO": [31, 0],
        "PLACE_ARDUINO": [85, 0], #111
        "PICK_SHIELD": [42, 0],
        "PLACE_SHIELD":[85, 0], #111
        "PUSH_SHIELD": [85, 0], #111
        "PICK_DRIVER1": [85, 36], #111
        "PLACE_DRIVER1": [85, 0], #111
        "PICK_DRIVER2": [85, 36], #111
        "PLACE_DRIVER2": [75, 0],
        "PUSH_DRIVERS": [75, 40],
        "PICK_ASSEMBLY": [42, 0],
        "PLACE_ASSEMBLY": [75, 0],
        "SAFE_PICK_WIRE1": [35, 50],
        "PICK_WIRE1": [35, 79],
        "PLACE_WIRE1": [35, 50],
        "INSPECTION": [21, 40],
        "FINISH_ROUTINE":[85, 40] #111
    }
    ARM_STATES = {
        # [x, y, z, roll, pitch, yaw, speed]
        "HOME": ["G","J", 0, -70, -20, 0, 90, 0, 30],
        "BEFORE_PICK_ARDUINO": ["R","J", 84.4, -4.4, -17.2, -9.2, -19.4, 94.4, 50],
        "PICK_ARDUINO": ["Y","L", 11.4, 407.8, 164.2, -146.1, -0.8, 1.9, 40, "D"],
        "AFTER_PICK_ARDUINO": ["Y","L", 17.6, 349.4, 241, -139.1, 0.2, -0.8, 60, "D"],
        "BEFORE_PLACE_ARDUINO": ["R","J", 60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 60],
        "SAFE_PLACE_ARDUINO": ["Y","J", 59.7, -11, -24.9, 0.4, 37.3, 63.1, 45],
        "PLACE_ARDUINO": ["Y", "L", 170.525681, 249.492065, 99.094414, 177.167374, -1.720248, -0.846373, 20, "B"],
        "AFTER_PLACE_ARDUINO": ["Y","J", 60.1, -21.4, -24.4, 2.7, 44.8, 60.5, 40],

        "BEFORE_PICK_SHIELD": ["R","J", 111.5, 1.8, -17, 23.6, -14.9, -92.3, 50],
        "BEFORE_PICK_SHIELD_2": ["Y","J", 107.7, 9.5, -26.5, 23.5, -7.9, -95.3, 40],
        #"PICK_SHIELD": ["Y","L", -90.355515, 463.406311, 76.797081, 149.918246, 1.207738, -179.569843, 10, "B"],
        "PICK_SHIELD": ["Y", "L", -93.551994, 462.443207, 73.711197, 152.435078, -1.048284, -177.925053, 10, "B"],
        #"AFTER_PICK_SHIELD": ["Y", "L", -94.383446, 460.783752, 85.423676, 149.201648, 0.965892, -178.939991, 10, "B"],
        "AFTER_PICK_SHIELD": ["Y", "L", -95.727844, 460.338898, 83.701698, 152.000546, -1.614194, -177.821291, 10, "B"],
        #"AFTER_PICK_SHIELD_1": ["Y", "L", -186.881912, 461.522919, 85.664001, 149.161827, 0.994827, -178.875934, 15, "B"],
        "AFTER_PICK_SHIELD_1": ["Y", "L", -180.174911, 460.585846, 83.944649, 151.954538, -1.563716, -177.754025, 10, "B"],
        "AFTER_PICK_SHIELD_2": ["Y", "L", -180.174911, 460.585846, 203.944649, 151.954538, -1.563716, -177.754025, 10, "B"],
        #"AFTER_PICK_SHIELD_2": ["Y", "L", -186.70517, 461.664825, 206.178345, 149.14779, 1.030751, -178.865392, 40, "B"],
        "BEFORE_PLACE_SHIELD": ["R","J", 55.4, -27.1, -20.3, 5.7, 40.5, 54.4, 40],
        "SAFE_PLACE_SHIELD": ["Y","J", 59.045994, -16.6568, -18.754456, 8.428725, 30.932788, 52.975506, 20],
        #"PLACE_SHIELD": ["Y", "L", 166.146057, 238.252823, 104.573799, -173.658351, 1.296546, -0.807641, 10, "B"],
        "PLACE_SHIELD": ["Y", "L", 169.589066, 241.325531, 104.716736, -172.414231, -0.292323, -1.413659, 10, "B"],
        #"AFTER_PLACE_SHIELD": ["Y","L", 165.455994, 238.415649, 134.730347, -171.572384, -1.126435, -1.054987, 10, "B"],
        "AFTER_PLACE_SHIELD": ["Y", "L", 169.865692, 241.578568, 134.649994, -172.367764, -0.348015, -1.369312, 10, "B"],
        "BEFORE_PUSH_SHIELD": ["Y","J", 56.120471, -16.822499, -16.341616, 4.443975, 35.192386, 53.043229, 10],
        "PUSH_SHIELD": ["Y","L", 163.246918, 203.765717, 91.109421, 179.887491, 3.111562, -0.49303, 40, "B"],
        "AFTER_PUSH_SHIELD": ["Y","L", 158.322281, 203.671539, 110.043457, -178.116822, 1.237875, 0.805865, 30, "B"],
        "PUSH_SHIELD_1": ["Y","L", 162.38858, 213.386688, 91.28334, 178.692702, 3.040229, -0.224829, 40, "B"],
        "AFTER_PUSH_SHIELD_1": ["Y","L", 158.322281, 203.671539, 130.043457, -178.116822, 1.237875, 0.805865, 30, "B"],

        "BEFORE_PICK_ASSEMBLY": ["Y","J", 50.5, -26.2, -14.2, 1.6, 42.4, 229.4, 30],
        "PICK_ASSEMBLY": ["Y","L", 165.6, 242.8, 96.7, 0.1, -179.1, -0.1, 20, "B"],
        "AFTER_PICK_ASSEMBLY": ["Y","L", 165.6, 242.8, 116.7, 0.1, -179.1, -0.1, 10, "B"],
        "BEFORE_PLACE_ASSEMBLY": ["R","J", 2.5, -43.3, -12.8, 1, 57.1, 181, 20],
        "SAFE_PLACE_ASSEMBLY": ["Y","L", 244.305725, 40.191769, 62.90258, -179.99916, -4.214105, 178.844708, 50, "B"],
        "PLACE_ASSEMBLY": ["Y", "L", 243.971924, 41.629547, 34.812107, 179.998301, -4.089715, 178.973681, 10, "B"],
        "AFTER_PLACE_ASSEMBLY": ["Y","L", 244.305725, 40.191769, 67.90258, -179.99916, -4.214105, 178.844708, 20, "B"],

        "BEFORE_PICK_DRIVER1": ["R","J", 57.3, -32, -18.2, 2.1, 45, 54.5, 30],
        "BEFORE_PICK_DRIVER1_2": ["R","J", 62.9, 25.2, -86.5, -1.6, 64.8, 64.1, 30],
        "BEFORE_PICK_DRIVER1_3": ["Y","J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 20],
        #"PICK_DRIVER1": ["Y","J", 67.7, 53.6, -111.5, -23.3, 117, 65.6, 10],
        "PICK_DRIVER1": ["Y", "L", 254.388977, 494.096527, 16.190947, 115.929988, 3.396551, 0.216693, 10, "W"],
        "AFTER_PICK_DRIVER1": ["Y","J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 45],
        "AFTER_PICK_DRIVER1_2": ["R","J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 45],
        "BEFORE_PLACE_DRIVER1": ["R","J", 43.1, 6.7, -35, -45.8, 105.3, 61.8, 15],
        #"PLACE_DRIVER1": ["Y", "L", 235.664642, 64.211578, 46.34708, 95.117239, 8.211287, -2.162858, 10, "W"],
        "PLACE_DRIVER1": ["Y", "L", 235.384155, 65.557449, 40.092468, 95.103488, 8.269958, -2.154608, 10, "W"],
        "AFTER_PLACE_DRIVER1": ["Y","L", 234.400604, 63.246693, 59.849049, 93.624226, 7.684223, -2.34397, 30, "W"],
        "AFTER_PLACE_DRIVER1_2": ["R","J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 20],

        "BEFORE_PICK_DRIVER2": ["R","J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 15],
        #"PICK_DRIVER2": ["Y","J", 67.7, 53.6, -111.5, -23.3, 117, 65.6, 10],
        "PICK_DRIVER2": ["Y", "L", 254.388977, 494.096527, 16.190947, 115.929988, 3.396551, 0.216693, 10, "W"],
        "AFTER_PICK_DRIVER2": ["Y","J", 66.9, 51.7, -111, -22.5, 119.8, 64.9, 45],
        "AFTER_PICK_DRIVER2_2": ["R","J", 72.3, 14.6, -69.4, -26.1, 139.3, 63.5, 45],
        "BEFORE_PLACE_DRIVER2": ["R","J", 43.2, -1.6, -31.3, -49.1, 110.7, 59.1, 15],
        #"PLACE_DRIVER2": ["Y", "L", 234.69577, 44.756672, 46.316273, 92.170804, 6.639664, -1.443624, 10, "W"],
        "PLACE_DRIVER2": ["Y", "L", 234.996155, 45.579674, 40.625122, 84.736218, 7.573815, 1.396527, 10, "W"],
        "AFTER_PLACE_DRIVER2": ["Y","L", 234.031128, 43.744728, 92.815109, 92.178023, 6.663041, -1.457261, 30, "W"],
        "BEFORE_PUSH_DRIVERS": ["Y", "J", 17.317535, -44.302586, -23.341556, 0.903096, 69.800755, 17.710928, 30],
        "SAFE_PUSH_DRIVERS": ["Y","L", 248.399551, 7.757665, 48.735741, 179.882678, 3.054667, 1.653728, 40, "B"],
        "PUSH_DRIVERS": ["Y","L", 248.399551, 7.757665, 28.235741, 179.882678, 3.054667, 1.653728, 40, "B"],
        "AFTER_PUSH_DRIVERS": ["Y","L", 248.399551, 7.757665, 48.735741, 179.882678, 3.054667, 1.653728, 40, "B"],
        
        "INSPECTION": ["Y", "J", 21.5, -63.1, -33.1, 0.2, 96.7, 21.5, 40],
        "FINISH_ROUTINE": ["G","J", 0, -70, -20, 0, 90, 0, 30]
    }
    def __init__(self):
        """Initialize communications"""
        # PLC configs
        if USE_PLC:
            self.plc = snap7.client.Client()
            self.plc.connect(PLC_IP, RACK, SLOT)
            self.plc_action_data = None
            self.plc_light_data = None

        # Arm configs
        self.arm = XArmAPI(XARM_IP, do_not_open=True)
        self.arm.register_error_warn_changed_callback(self.handle_err_warn_changed)
        self.arm.connect()

        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0) # Position control
        self.arm.set_state(state=0)

        self.arduino_counter = 5
        self.shield_counter = 5
        self.driver_counter = 10
        self.fred_counter = 0

        self.list_states = list(self.ARM_STATES.keys())

        # Gripper configs
        if USE_GRIPPER:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Speech feedback
        if USE_SPEECH:
            pygame.mixer.init()
        # Camera
        if USE_CAMERA:
            self.inspection_result = 0

        self.current_state = "HOME"

    def run(self):
        """Main loop of the electronics station"""
        if self.current_state in STATE_TO_RECORD:
            self.record_state(self.current_state)
            self.current_state = self.list_states[self.list_states.index(self.current_state) + 1]

        elif self.current_state == "HOME":
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if USE_PLC:
                self.current_state = "WAIT_SENSOR"
            else:
                self.current_state = "BEFORE_PICK_ARDUINO"
                #self.current_state = "BEFORE_PICK_DRIVER1"
                #self.current_state = "BEFORE_PICK_WIRES"

        elif self.current_state == "WAIT_SENSOR":
            self.plc_action_data = self.plc.db_read(1, 0, 14)
            if self.plc_action_data[0] == 0b00000001:
                time.sleep(2)
                self.current_state = "BEFORE_PICK_ARDUINO"

        elif self.current_state == "AFTER_PICK_ARDUINO":
            self.send_arm_state(self.current_state)
            self.arduino_counter -= 1
            self.send_counter_data(self.arduino_counter, 4, 5)
            self.current_state = "BEFORE_PLACE_ARDUINO"

        elif self.current_state == "AFTER_PICK_SHIELD":
            self.send_arm_state(self.current_state)
            self.shield_counter -= 1
            self.send_counter_data(self.shield_counter, 6, 7)
            self.current_state = "AFTER_PICK_SHIELD_1"

        elif self.current_state == "AFTER_PICK_DRIVER1":
            self.send_arm_state(self.current_state)
            self.driver_counter -= 1
            self.send_counter_data(self.driver_counter, 8, 9)
            self.current_state = "AFTER_PICK_DRIVER1_2"

        elif self.current_state == "AFTER_PICK_DRIVER2":
            self.send_arm_state(self.current_state)
            self.driver_counter -= 1
            self.send_counter_data(self.driver_counter, 8, 9)
            self.current_state = "AFTER_PICK_DRIVER2_2"

        elif self.current_state == "INSPECTION":
            if not USE_CAMERA:
                self.current_state = "FINISH_ROUTINE"
                return
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            self.static_speech_feedback(self.current_state)
            time.sleep(2)

            self.arm.set_cgpio_digital(2, 1, delay_sec=0)
            self.get_camera_state()
            time.sleep(2)
            self.arm.set_cgpio_digital(2, 0, delay_sec=0)

            if self.inspection_result == 1:
                self.static_speech_feedback("PASS_INSPECTION")
                self.plc_action_data = self.plc.db_read(1, 0, 14)
                self.plc_action_data[12] = 0b00000001
                self.plc.db_write(1,0, self.plc_action_data)
                
                #self.static_speech_feedback("FINISH_ROUTINE")
                print("FrED is ready")
                self.fred_counter += 1
                self.send_counter_data(self.fred_counter, 2, 3)
                print("FrED is ready")

            else:
                self.static_speech_feedback("FAILED_INSPECTION")
                self.plc_action_data = self.plc.db_read(1, 0, 14)
                self.plc_action_data[12] = 0b00000010
                self.plc.db_write(1,0, self.plc_action_data)
                print("FrED is not ready")

            self.current_state = "FINISH_ROUTINE"
  
        elif self.current_state == "FINISH_ROUTINE":
            if not USE_PLC:
                self.current_state = "HOME"
            self.plc_action_data = self.plc.db_read(1, 0, 2)
            #self.static_speech_feedback(self.current_state)
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            if self.plc_action_data[0] == 0b00000000:
                time.sleep(2)
                self.plc_action_data = self.plc.db_read(1, 0, 14)
                self.plc_action_data[12] = 0b00000000
                self.plc.db_write(1,0, self.plc_action_data)
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

    def send_counter_data(self, data, bit1, bit2):
        """Send counter data to the PLC datablocks"""
        if not USE_PLC:
            return
        datatmp = bytearray(data.to_bytes(2,"big"))
        self.plc_action_data[bit1] = datatmp[0]
        self.plc_action_data[bit2] = datatmp[1]
        self.plc.db_write(1, 0, self.plc_action_data)

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
        x, y, z, roll, pitch, yaw, speed = self.ARM_STATES[state][2:9]
        light = self.ARM_STATES[state][0] 
        lineal = self.ARM_STATES[state][1] == "L"
        print(f"Sending arm to state: {state}")

        if USE_PLC:
            if light == "R":
                self.plc_light_data = self.plc.db_read(2, 0, 2)
                self.plc_light_data[0] = 0b00000010
                self.plc.db_write(2,0, self.plc_light_data)
            elif light == "Y":
                self.plc_light_data = self.plc.db_read(2, 0, 2)
                self.plc_light_data[0] = 0b00000100
                self.plc.db_write(2,0, self.plc_light_data)
            else:
                self.plc_light_data = self.plc.db_read(2, 0, 2)
                self.plc_light_data[0] = 0b00000001
                self.plc.db_write(2,0, self.plc_light_data)

        if lineal:
            tcp = self.ARM_STATES[state][9]
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
        th = threading.Thread(target=self.speak_th, args=(file_path,))
        th.start()

    def speak_th(self, filename):
        """Function to play the audio in a new thread"""
        pygame.mixer.music.load(filename)
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
            print(f"\"{state}\": [\"Y\", \"J\", {joint_position[1][0]}, {joint_position[1][1]}, {joint_position[1][2]}, {joint_position[1][3]}, {joint_position[1][4]}, {joint_position[1][5]}, 10],")
        
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
            print(f"\"{state}\": [\"Y\", \"L\", {lineal_position[1][0]}, {lineal_position[1][1]}, {lineal_position[1][2]}, {lineal_position[1][3]}, {lineal_position[1][4]}, {lineal_position[1][5]}, 10, \"{desired_tcp.upper()}\"],")

        print("Do you want to continue the program? (Y/N)")
        continue_program = input()
        if continue_program.upper() == "N":
            print("The program has been stopped, type Ctrl+C to exit")
            self.arm.disconnect()
            sys.exit()
        else:
            self.arm.set_mode(0) # Position control
            self.arm.set_state(0)
    
    def get_camera_state(self):
        """Get the camera result calling the trigger"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.settimeout(None)
            s.sendall(b"cmd Online")
            s.sendall(b"cmd trigger")

            data = s.recv(24)

        print(f"Received2 {data!r}")

        str1 = data.decode('UTF-8')
        self.inspection_result = float(str1)

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
