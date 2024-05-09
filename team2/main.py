#!/usr/bin/env python3
import socket
import time

UDP_IP = "192.168.34.23"  # IP address of the ESP32
UDP_PORT = 1234            # Port number
MESSAGE = ""               # Initialize message

class ElectronicsStation:
    """Class to handle of components (arm, gripper, plc, etc) of the electronics station"""
    GripperStates = {
        "HOME": [100, 40],
        "PICK_ARDUINO": [80, 40],
        "PLACE_ARDUINO": [110, 40]
    }
    def __init__(self):
        """Initialize communications"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.current_state = "HOME"

    def send_gripper_state(self, state):
        """Send the data to the ESP32 via socket"""
        board_position, wire_position = self.GripperStates[state]
        print(f"Sending gripper to state: {state}")
        # Send board finger position
        message = 'b' + str(board_position)
        self.sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(0.2)
        # Send wire finger position
        message = 'w' + str(wire_position)
        self.sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(0.2)

    def run(self):
        """Main loop of the electronics station"""
        self.send_gripper_state("HOME")
        time.sleep(3)
        self.send_gripper_state("PICK_ARDUINO")
        time.sleep(3)
        self.send_gripper_state("PLACE_ARDUINO")
        time.sleep(3)

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
