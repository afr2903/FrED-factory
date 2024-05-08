#!/usr/bin/env python3
import socket
import time

UDP_IP = "192.168.18.23"  # IP address of the ESP32
UDP_PORT = 1234            # Port number
MESSAGE = ""               # Initialize message

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

instructions = {
    "HOME": 0,
    "PICK_ARDUINO": 1,
    "PLACE_ARDUINO": 2,
    "PICK_RAMPS": 3,
    "PLACE_RAMPS": 4,
    "PICK_DRIVER": 5,
    "PLACE_DRIVER": 6,
    "PICK_WIRE": 7,
    "PLACE_WIRE": 8,
    "PICK_ASSEMBLY": 9,
    "PLACE_ASSEMBLY": 10
}

def main():
    for name, value in instructions.items():
        print(f"Sending instruction: {name}")
        message = str(value)
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(2)
    time.sleep(3)

if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break

sock.close()
