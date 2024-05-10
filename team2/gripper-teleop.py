#!/usr/bin/env python3
import socket
import time
from tkinter import Tk, Scale, HORIZONTAL, Label, Button

UDP_IP = "192.168.2.23"  # IP address of the ESP32
UDP_PORT = 1234            # Port number
MESSAGE = ""               # Initialize message

WIRE_LOWER_LIMIT = 0
WIRE_UPPER_LIMIT = 79
BOARD_LOWER_LIMIT = 15
BOARD_UPPER_LIMIT = 120

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gui = Tk()

def send_data(position, board_gripper= False):
    """Send the data to the ESP32 via socket"""
    data = str(position)
    if board_gripper:
        data = 'b' + data
    else:
        data = 'w' + data
    
    print(f"Sending instruction: {data}")
    sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
    time.sleep(0.1)

if __name__ == '__main__':
    # Init GUI
    gui.title("Gripper Teleop")
    gui.geometry("600x200")

    board_label = Label(gui, text="Board Gripper")
    board_label.pack()

    board_slider = Scale(gui, from_=BOARD_LOWER_LIMIT, to=BOARD_UPPER_LIMIT, orient=HORIZONTAL, length=500, resolution=1)
    board_slider.pack()

    wire_label = Label(gui, text="Wire Gripper")
    wire_label.pack()

    wire_slider = Scale(gui, from_=WIRE_LOWER_LIMIT, to=WIRE_UPPER_LIMIT, orient=HORIZONTAL, length=500, resolution=1)
    wire_slider.pack()

    last_board_position = board_slider.get()
    last_wire_position = wire_slider.get()

    #board_position_update = Button(gui, text="Update Board Position", command=lambda: send_data(board_slider.get(), board_gripper=True))

    while True:
        try:
            # Send data to ESP32
            board_position = board_slider.get()
            wire_position = wire_slider.get()

            if board_position != last_board_position:
                send_data(board_position, board_gripper=True)
                last_board_position = board_position

            if wire_position != last_wire_position:
                send_data(wire_position)
                last_wire_position = wire_position

            time.sleep(0.1)
            gui.update_idletasks()
            gui.update()
        except KeyboardInterrupt:
            break

sock.close()
