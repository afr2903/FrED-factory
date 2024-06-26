"""
Script for the trajectory generation challenge, using the Ufactory xArm6
"""

# Libraries imports
import os
import sys
import time

from openai import OpenAI
from dotenv import load_dotenv
import pygame
from xarm.wrapper import XArmAPI

# Current directory path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# Load environment variables for the OpenAI API Key
load_dotenv()

# XARM IP address
XARM_IP = '192.168.1.203'

# State machine states
STATES = {
    "IDLE": 0,
    "WAIT_SENSOR": 1,
    "PICK_AND_PLACE": 2,
    "SHUTDOWN": 100
}

class SnapArm:
    """Class to connect to the PLC and the xArm"""
    def __init__(self):
        # Arm configs
        self.arm = XArmAPI(XARM_IP, do_not_open=True)
        self.arm.register_error_warn_changed_callback(self.handle_err_warn_changed)
        self.arm.connect()

        self.arm.motion_enable(enable=True) # Enable motion
        self.arm.set_mode(0) # Position control mode
        self.arm.set_state(state=0) 

        self.current_state = STATES["IDLE"]
        self.iteration = 0 # Current pick and place iteration
        self.cube_height = 45 # Height of the cube in `mm`

        # Speeds for the xArm
        self.pick_speed = 100
        self.default_speed = 200

        pygame.mixer.init() # Initialize the mixer for the audio playback

        # Text-to-speech feature client
        self.speech_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
        )
        self.run() # Main iteration
    
    def handle_err_warn_changed(self, item):
        """Log the error encountered with the arm"""
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

    def pick_and_place_routine(self):
        """Routine to pick and place the cube"""
        # Arm positions
        self.arm.set_position(
            x=-52.2, y=330.8, z=-46.3, roll=-178.2, pitch=0.9, yaw=94.1,
            speed=self.pick_speed, wait=False)
        print("Picking cube...")
        self.arm.set_cgpio_digital(5, 1) # Close the gripper
        self.arm.set_position(
            x=-55.7, y=308.5, z=85, roll=-177.7, pitch=-0.6, yaw=92.8,
            speed=self.default_speed, wait=False)
        self.arm.set_position(
            x=259.4, y=12.4, z=145.9, roll=179.6, pitch=-2.3, yaw=0.9,
            speed=self.default_speed, wait=False)
        # Place position dependent of the current number of cubes
        self.arm.set_position(
            x=286.7, y=24.4, z=(-67.1 + self.iteration*self.cube_height), roll=179.8, pitch=-0.1, yaw=2.9,
            speed=self.default_speed, wait=True)
        print("Placing cube...")
        self.arm.set_cgpio_digital(5, 0)
        self.arm.set_position(
            x=259.4, y=12.4, z=115.9, roll=179.6, pitch=-2.3, yaw=0.9,
            speed=self.default_speed, wait=False)
        self.arm.set_position(
            x=300, y=0, z=180, roll=-180, pitch=0, yaw=0,
            speed=self.default_speed, wait=True)

    def run(self):
        """Main state execution"""
        while True:
            try:
                if self.current_state == STATES["IDLE"]:
                    # Home position
                    self.arm.set_position(x=300, y=0, z=180, roll=-180, pitch=0, yaw=0, speed=self.default_speed, wait=True)
                    self.arm.set_cgpio_digital(5, 0)
                    self.current_state = STATES["WAIT_SENSOR"]

                elif self.current_state == STATES["WAIT_SENSOR"]:
                    self.arm.set_position(x=-69.6, y=243.5, z=96.8, roll=179.8, pitch=0.8, yaw=92, speed=self.pick_speed, wait=True)
                    print("Inspection position")

                    # Speech processing
                    response = self.speech_client.audio.speech.create(
                        model="tts-1",
                        voice="onyx",
                        input="Press Enter when the cube is in position"
                    )

                    # Audio file
                    tmp_path = f"output-{id}.opus"
                    response.stream_to_file(tmp_path)

                    # Load and play the audio file
                    pygame.mixer.music.load(tmp_path)
                    pygame.mixer.music.play()

                    # Loop to keep the script running during playback
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                    input("Press Enter when the cube is in position...")
                    self.current_state = STATES["PICK_AND_PLACE"]

                elif self.current_state == STATES["PICK_AND_PLACE"]:
                    print("Pick and place routine...")
                    self.pick_and_place_routine()
                    self.iteration += 1 # Register a cube as placed
                    print(f"Cubes placed: {self.iteration}")
                    time.sleep(2)
                    self.current_state = STATES["IDLE"]

                elif self.current_state == STATES["SHUTDOWN"]:
                    break
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.arm.disconnect()
                break

if __name__ == "__main__":
    try:
        SnapArm()
    except Exception as e:
        print(e)
        sys.exit(1)