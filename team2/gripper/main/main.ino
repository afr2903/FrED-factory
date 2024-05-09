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

// Network setup & credentials
const char *ssid = "RoboMaze";
const char *password = "RoBorregos2024"; // Set password
const int udpPort = 1234;

WiFiUDP udp;

IPAddress staticIP(192, 168, 2, 23); // Set the desired static IP address
IPAddress gateway(192, 168, 2, 1);   // Set the gateway of your network
IPAddress subnet(255, 255, 255, 0);   // Set the subnet mask of your network

void setup(){
    Serial.begin(115200);

    // WiFi connection
    Serial.println();
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED){
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");
    WiFi.config(staticIP, gateway, subnet);

    Serial.print("Current ip: ");
    Serial.println(WiFi.localIP());

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
            int target_pos = message.toInt();
            Serial.printf("UDP packet contents: %c%i\n", incoming_packet[0], target_pos);
            Serial.println();

            if (board_requested){
                board_gripper.write(target_pos);
            } else {
                wire_gripper.write(target_pos);
            }
        }
    }
    delay(10);
}