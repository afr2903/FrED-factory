#!/usr/bin/env python3
import socket
import time
from xarm.wrapper import XArmAPI

# IP addresses
PLC_IP = '192.168.0.1'
XARM_IP = '192.168.1.201'
UDP_IP = "192.168.2.23"

UDP_PORT = 1234            # Port number
MESSAGE = ""               # Initialize message

class ElectronicsStation:
    """Class to handle of components (arm, gripper, plc, etc) of the electronics station"""
    GRIPPER_STATES = {
        # [board, wire]
        "HOME": [85, 40],
        "PICK_ARDUINO": [20, 40],
        "PLACE_ARDUINO": [85, 40],
        "PICK_WIRE": [85, 79]
    }
    ARM_STATES = {
        # [x, y, z, roll, pitch, yaw, speed]
        "HOME": [0, -70, -20, 0, 90, 0, 30],
        "BEFORE_PICK_ARDUINO": [84.4, -4.4, -17.2, -9.2, -19.4, 94.4, 30],
        "PICK_ARDUINO": [11.4, 407.8, 164.2, -146.1, -0.8, 1.9, 20],
        "AFTER_PICK_ARDUINO": [17.6, 349.4, 241, -139.1, 0.2, -0.8, 30],
        "BEFORE_PLACE_ARDUINO": [59.8, 0.8, -23.6, -8.9, 24.6, 68.8, 30],
        "PLACE_ARDUINO": [166.3, 287.4, 124.2, 176.8, 0.3, 1.5, 20],
        "AFTER_PLACE_ARDUINO": [166.3, 287.4, 145, 176.8, 0.3, 1.5, 20],
    }
    def __init__(self):
        """Initialize communications"""
        # Arm configs
        self.arm = XArmAPI(XARM_IP, do_not_open=True)
        self.arm.register_error_warn_changed_callback(self.handle_err_warn_changed)
        self.arm.connect()

        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0) # Position control
        self.arm.set_state(state=0)

        # Gripper configs
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

    def run(self):
        """Main loop of the electronics station"""
        if self.current_state == "HOME":
            self.send_arm_state(self.current_state)
            self.send_gripper_state(self.current_state)
            self.current_state = "BEFORE_PICK_ARDUINO"

        elif self.current_state == "BEFORE_PICK_ARDUINO":
            self.send_arm_state(self.current_state)
            self.current_state = "PICK_ARDUINO"
        
        elif self.current_state == "PICK_ARDUINO":
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
            self.send_arm_state(self.current_state, lineal=True)
            self.send_gripper_state(self.current_state)
            time.sleep(1)
            self.current_state = "AFTER_PLACE_ARDUINO"

        elif self.current_state == "AFTER_PLACE_ARDUINO":
            self.send_arm_state(self.current_state, lineal=True)
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
