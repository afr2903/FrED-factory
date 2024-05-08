/*
  Script to control the gripper of the robot sending predefined positions
  to the servo motors.
  ESP32Servo library is used to control the servo motors.
  Author: afr2903
*/

#include <ESP32Servo.h>

Servo big_gripper; // Servo object to control the servo for the big gripper
Servo small_gripper; // Servo object to control the servo for the small gripper

const uint8_t FREQUENCY = 330; // 330 Hz
const uint8_t MIN_PWM = 500; // 500 us
const uint8_t MAX_PWM = 2500; // 2500 us

const uint8_t BIG_GRIPPER_PWM = 2;
const uint8_t SMALL_GRIPPER_PWM = 15;

// Gripper struct to store a configuration of the gripper
struct Gripper {
    uint8_t big_position;
    uint8_t small_position;
};

// Gripper predefined positions array
Gripper gripper_positions[] = {
    {120, 130},
    {100, 120},
    {150, 110},
    {110, 100},
    {150, 90},
    {90, 100},
    {100, 60},
    {110, 100},
    {120, 60},
    {110, 130},
    {150, 130}
};

// Enum to link Gripper states to a name
enum GripperState {
    HOME = 0,
    PICK_ARDUINO = 1,
    PLACE_ARDUINO = 2,
    PICK_RAMPS = 3,
    PLACE_RAMPS = 4,
    PICK_DRIVER = 5,
    PLACE_DRIVER = 6,
    PICK_WIRE = 7,
    PLACE_WIRE = 8,
    PICK_ASSEMBLY = 9,
    PLACE_ASSEMBLY = 10
} current_state = HOME;

GripperState target_state = HOME;

void setup() {
    Serial.begin(115200);
	
    // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);

    // Big gripper servo intialization
	big_gripper.setPeriodHertz(FREQUENCY);
	big_gripper.attach(BIG_GRIPPER_PWM, MIN_PWM, MAX_PWM);
    
    // Small gripper servo intialization
	small_gripper.setPeriodHertz(FREQUENCY);
	small_gripper.attach(SMALL_GRIPPER_PWM, MIN_PWM, MAX_PWM);
}

void loop() {
    if (current_state != target_state) {
        current_state = target_state;
        move_gripper();
    }
    target_state = (GripperState) ((current_state + 1) % 3);
    delay(5000);
}

void move_gripper(){
    uint8_t target_big_position = gripper_positions[current_state].big_position;
    uint8_t target_small_position = gripper_positions[current_state].small_position;
    Serial.print("Current state: ");
    Serial.print(current_state);
    Serial.print(" Big gripper position: ");
    Serial.print(target_big_position);
    Serial.print(" Small gripper position: ");
    Serial.println(target_small_position);

    big_gripper.write(target_big_position);
    small_gripper.write(target_small_position);
}