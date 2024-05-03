import os
import sys
import time
import snap7
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

contador_ok = 0
contador_scrap = 0
binary = 0
data_counter = [0, 0]


IP = '192.168.0.1'

RACK = 0
SLOT = 1
plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

# Initialize flag
task_running = False

def handle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    # TODO: Do different processing according to the error code

if __name__ == "__main__":
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

def decimal_to_binary(decimal):
    global binary 
    global data_counter

    binary = bin(decimal)[2:].zfill(16)  # Convert to binary and zero-fill to 16 bits

    text = f"0b{binary}"
    position = 10

    # Check if the position is valid
    if position < len(text):
        part1 = text[:position]  # Characters before position 3
        part2 = f"0b{text[position:]}"  # Characters at position 3 and onwards

        data_counter = [part1, part2]
        
    else:
        print("Position is out of range")

def run_task():
    global task_running
    global data_counter
    global data
    

    if arm.get_cgpio_digital() == (0, [1, 1, 1, 1, 1, 1, 1, 0]):  # agregar el cgpio CI7

        arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)
        arm.set_position(x=-69.6, y=243.5, z=96.8, roll=179.8, pitch=0.8, yaw=92, speed=100, wait=False)


        data = plc.db_read(1, 0, 5)
        print(data)
    
        if data[4] == 0b00000001:  # OK
            print(data)

            arm.set_position(x=-52.2, y=330.8, z=-46.3, roll=-178.2, pitch=0.9, yaw=94.1, speed=100, wait=False)
            arm.set_cgpio_digital(0, 1)
            arm.set_position(x=-55.7, y=308.5, z=85, roll=-177.7, pitch=-0.6, yaw=92.8, speed=100, wait=False)
            arm.set_position(x=259.4, y=12.4, z=115.9, roll=179.6, pitch=-2.3, yaw=0.9, speed=100, wait=False)
            arm.set_position(x=286.7, y=24.4, z=-67.1, roll=179.8, pitch=-0.1, yaw=2.9, speed=100, wait=False)
            arm.set_cgpio_digital(0, 0)
            arm.set_position(x=259.4, y=12.4, z=115.9, roll=179.6, pitch=-2.3, yaw=0.9, speed=100, wait=False)
            arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)

            global contador_ok
            contador_ok += 1
            decimal_to_binary(contador_ok)

            data[2] = data_counter[0]
            data[3] = data_counter[1]
            
            plc.db_write(1, 0, data)

        elif data[4] == 0b00000010:  # SCRAP

            arm.set_position(x=-52.2, y=330.8, z=-46.3, roll=-178.2, pitch=0.9, yaw=94.1, speed=100, wait=False)
            arm.set_cgpio_digital(0, 1)
            arm.set_position(x=-55.7, y=308.5, z=85, roll=-177.7, pitch=-0.6, yaw=92.8, speed=100, wait=False)
            arm.set_position(x=256.6, y=-145, z=77.8, roll=179.7, pitch=-2, yaw=-0.4, speed=100, wait=False)
            arm.set_position(x=272.9, y=-135.4, z=-89, roll=-179.1, pitch=-6.2, yaw=2.6, speed=100, wait=False)
            arm.set_cgpio_digital(0, 0)
            arm.set_position(x=256.6, y=-145, z=77.8, roll=179.7, pitch=-2, yaw=-0.4, speed=100, wait=False)
            arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=100, wait=False)

            global contador_scrap
            contador_scrap += 1
            decimal_to_binary(contador_scrap)

            data[0] = data_counter[0]
            data[1] = data_counter[1]

            plc.db_write(1, 0, data)

        # Task finished, reset flag
        task_running = False

arm = XArmAPI(ip, do_not_open=True)
arm.register_error_warn_changed_callback(handle_err_warn_changed)
arm.connect()

# enable motion
arm.motion_enable(enable=True)
# set mode: position control mode
arm.set_mode(0)
# set state: sport state
arm.set_state(state=0)




while True:
    if not task_running:
        print('hello')
        run_task()
        # Set flag to indicate task is running
        task_running = True
    

    arm.disconnect()

