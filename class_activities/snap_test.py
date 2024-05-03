import os
import sys
import time
import snap7
from configparser import ConfigParser
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

PLC_IP = '192.168.0.1'
XARM_IP = '192.168.1.201'

RACK = 0
SLOT = 1
plc = snap7.client.Client()

STATES = {
    "IDLE": 0,
    "WAIT_SENSOR": 1,
    "WAIT_ACTION": 2,
    "OK_ROUTINE": 3,
    "SCRAP_ROUTINE": 4,
    "SHUTDOWN": 100
}

class SnapArm:
    """Class to connect to the PLC and the xArm"""
    def __init__(self):
        # PLC configs
        self.plc = snap7.client.Client()
        self.plc.connect(PLC_IP, RACK, SLOT)

        # Arm configs
        self.arm = XArmAPI(XARM_IP, do_not_open=True)
        self.arm.register_error_warn_changed_callback(self.handle_err_warn_changed)
        self.arm.connect()

        # enable motion
        self.arm.motion_enable(enable=True)
        # set mode: position control mode
        self.arm.set_mode(0)
        # set state: sport state
        self.arm.set_state(state=0)

        self.current_state = STATES["IDLE"]
        self.sensor_state = None
        self.plc_action_data = None

        self.ok_counter = 0
        self.scrap_counter = 0

        self.run()
                            
    def handle_err_warn_changed(self, item):
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
        # TODO: Do different processing according to the error code

    def decimal_to_binary(self, decimal):

        binary = bin(decimal)[2:].zfill(16)  # Convert to binary and zero-fill to 16 bits

        text = binary
        position = 8

        # Check if the position is valid
        if position < len(text):
            part1 = text[:position]  # Characters before position 3
            part2 = text[position:]  # Characters at position 3 and onwards

            return [part1, part2]
        
        else:
            print("Position is out of range")

    def execute_ok_routine(self):

        self.arm.set_position(x=-52.2, y=330.8, z=-46.3, roll=-178.2, pitch=0.9, yaw=94.1, speed=100, wait=False)
        self.arm.set_cgpio_digital(0, 1)
        self.arm.set_position(x=-55.7, y=308.5, z=85, roll=-177.7, pitch=-0.6, yaw=92.8, speed=100, wait=False)
        self.arm.set_position(x=259.4, y=12.4, z=115.9, roll=179.6, pitch=-2.3, yaw=0.9, speed=100, wait=False)
        self.arm.set_position(x=286.7, y=24.4, z=-67.1, roll=179.8, pitch=-0.1, yaw=2.9, speed=100, wait=False)
        self.arm.set_cgpio_digital(0, 0)
        self.arm.set_position(x=259.4, y=12.4, z=115.9, roll=179.6, pitch=-2.3, yaw=0.9, speed=100, wait=False)
        self.arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)

        self.ok_counter += 1
        a, b = self.decimal_to_binary(self.ok_counter)

        self.plc_action_data[0] = int(a)
        self.plc_action_data[1] = int(b)
            
        self.plc.db_write(1, 0, self.plc_action_data)

    def execute_scrap_routine(self):

        self.arm.set_position(x=-52.2, y=330.8, z=-46.3, roll=-178.2, pitch=0.9, yaw=94.1, speed=100, wait=False)
        self.arm.set_cgpio_digital(0, 1)
        self.arm.set_position(x=-55.7, y=308.5, z=85, roll=-177.7, pitch=-0.6, yaw=92.8, speed=100, wait=False)
        self.arm.set_position(x=256.6, y=-145, z=77.8, roll=179.7, pitch=-2, yaw=-0.4, speed=100, wait=False)
        self.arm.set_position(x=272.9, y=-135.4, z=-89, roll=-179.1, pitch=-6.2, yaw=2.6, speed=100, wait=False)
        self.arm.set_cgpio_digital(0, 0)
        self.arm.set_position(x=256.6, y=-145, z=77.8, roll=179.7, pitch=-2, yaw=-0.4, speed=100, wait=False)
        self.arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)

        self.scrap_counter += 1
        
        a, b = self.decimal_to_binary(self.scrap_counter)
        self.plc_action_data[2] = int(a)
        self.plc_action_data[3] = int(b)

        plc.db_write(1, 0, self.plc_action_data)

    def run(self):
        while True:
            try:
                if self.current_state == STATES["IDLE"]:
                    self.arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)
                    print("Waiting for sensor...")
                    self.current_state = STATES["WAIT_SENSOR"]

                elif self.current_state == STATES["WAIT_SENSOR"]:
                    self.sensor_state = self.arm.get_cgpio_digital()
                    if self.sensor_state == (0, [1, 1, 1, 1, 1, 1, 1, 0]):
                        self.arm.set_position(x=-69.6, y=243.5, z=96.8, roll=179.8, pitch=0.8, yaw=92, speed=100, wait=False)
                        print("Waiting for action...")
                        self.current_state = STATES["WAIT_ACTION"]

                elif self.current_state == STATES["WAIT_ACTION"]:
                    self.plc_action_data = self.plc.db_read(1, 0, 5)
                    if self.plc_action_data[4] == 0b00000001:
                        self.current_state = STATES["OK_ROUTINE"]
                    elif self.plc_action_data[4] == 0b00000010:
                        self.current_state = STATES["SCRAP_ROUTINE"]

                elif self.current_state == STATES["OK_ROUTINE"]:
                    print("OK routine")
                    self.execute_ok_routine()
                    self.current_state = STATES["IDLE"]

                elif self.current_state == STATES["SCRAP_ROUTINE"]:
                    print("Scrap routine")
                    self.execute_scrap_routine()
                    self.current_state = STATES["IDLE"]

                elif self.current_state == STATES["SHUTDOWN"]:
                    #self.handle_shutdown()
                    break
                time.sleep(0.1)
            except KeyboardInterrupt:
                #self.handle_shutdown()
                self.arm.disconnect()
                break

if __name__ == "__main__":
    try:
        SnapArm()
    except Exception as e:
        print(e)
        sys.exit(1)