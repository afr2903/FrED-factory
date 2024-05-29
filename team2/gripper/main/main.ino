/*
  Script to control the gripper of the robot receiving positions from Python script
  to the servo motors.
  ESP32Servo library is used to control the servo motors.
  WiFi library is used to connect to the network.
  Author: afr2903
*/

#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

// Servo objects to control the grippers
Servo wire_gripper; 
Servo board_gripper;

const int WIRE_PWM_PIN = 13;
const int BOARD_PWM_PIN = 12;

// Servo values
int wire_current_pos = -1;
int board_current_pos = -1;
int wire_target_pos = -1;
int board_target_pos = -1;

// Network setup & credentials
const char *ssid = "ESP32_AP";
const char *password = "mit"; // Set password
const int udpPort = 1234;

WiFiUDP udp;

IPAddress staticIP(192, 168, 2, 23); // Set the desired static IP address
IPAddress gateway(192, 168, 2, 1);   // Set the gateway of your network
IPAddress subnet(255, 255, 255, 0);   // Set the subnet mask of your network

void setup(){
    Serial.begin(115200);

    // WiFi connection
    Serial.println();
    //WiFi.begin(ssid, password);
    WiFi.softAPConfig(staticIP, gateway, subnet);
    WiFi.softAP(ssid, password);

    Serial.print("Current IP: ");
    Serial.println(WiFi.softAPIP());

    udp.begin(udpPort);
    Serial.println("UDP server started");

    // Servo setup
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    ESP32PWM::allocateTimer(3);
    wire_gripper.setPeriodHertz(330);         // standard 50 hz servo
    wire_gripper.attach(WIRE_PWM_PIN, 500, 2500); // attaches the servo on pin 18 to the servo object
    board_gripper.setPeriodHertz(330);           // standard 50 hz servo
    board_gripper.attach(BOARD_PWM_PIN, 500, 2500);     // attaches the servo on pin 18 to the servo object
}

void loop(){
    int packetSize = udp.parsePacket(); // Receive UDP packet
    if (packetSize){
        char incoming_packet[255];
        int len = udp.read(incoming_packet, 255);
        bool board_requested = false;
        if (len > 0){
            // Check gripper requested
            if(incoming_packet[0] == 'b')
                board_requested = true;

            incoming_packet[len] = 0;
            String message;
            // Trim leading and trailing whitespaces
            for (int i = 1; i < len; i++){
                char letter = incoming_packet[i];
                if (letter != ' ')
                    message += letter;
            }
            // Convert the target position to integer
            int target_pos = message.toInt();
            Serial.printf("Target: %c%i\n", incoming_packet[0], target_pos);
            Serial.println();

            // Set the target position
            if (board_requested){
                board_target_pos = target_pos;
            } else {
                wire_target_pos = target_pos;
            }
        }
    }

    // Set the current position to the target position with steps
    if (wire_current_pos != wire_target_pos){
        if (wire_current_pos == -1)
            wire_current_pos = wire_target_pos - 1;
        wire_current_pos += wire_current_pos < wire_target_pos ? 1 : -1;
        wire_gripper.write(wire_current_pos);
        Serial.printf("Wire: %i\n", wire_current_pos);
    }
    if (board_current_pos != board_target_pos){
        if (board_current_pos == -1)
            board_current_pos = board_target_pos - 1;
        board_current_pos += board_current_pos < board_target_pos ? 1 : -1;
        board_gripper.write(board_current_pos);
        Serial.printf("Board: %i\n", board_current_pos);
    }

    delay(20);
}