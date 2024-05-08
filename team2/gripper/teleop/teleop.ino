#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

Servo wire_gripper; // create servo object to control a servo
Servo board_gripper;

int wire_pos = 0; // variable to store the servo position
int board_pos = 0;

const int WIRE_PWM = 13;
const int BOARD_PWM = 12;


const char *ssid = "afr2903";
const char *password = "12345678"; // Set password
const int udpPort = 1234;

WiFiUDP udp;

IPAddress staticIP(192, 168, 18, 23); // Set the desired static IP address
IPAddress gateway(192, 168, 18, 1);   // Set the gateway of your network
IPAddress subnet(255, 255, 255, 0);   // Set the subnet mask of your network

void setup(){
    Serial.begin(115200);
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

    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    ESP32PWM::allocateTimer(3);
    wire_gripper.setPeriodHertz(330);         // standard 50 hz servo
    wire_gripper.attach(WIRE_PWM, 500, 2500); // attaches the servo on pin 18 to the servo object
    board_gripper.setPeriodHertz(330);           // standard 50 hz servo
    board_gripper.attach(BOARD_PWM, 500, 2500);     // attaches the servo on pin 18 to the servo object
}

void loop(){
    int packetSize = udp.parsePacket();
    if (packetSize){
        Serial.printf("Received %d bytes from %s, port %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
        char incomingPacket[255];
        int len = udp.read(incomingPacket, 255);
        bool board_requested = false;
        if (len > 0){
            if(incomingPacket[0] == 'b')
                board_requested = true;

            incomingPacket[len] = 0;
            // Trim leading and trailing whitespaces
            String message_completed;
            for (int i = 1; i < len; i++){
                char letter = incomingPacket[i];
                if (letter != ' '){
                    message_completed += letter;
                    Serial.println(letter);
                    Serial.println(message_completed);
                }
            }
            int target_pos = message_completed.toInt();
            Serial.printf("UDP packet contents: %i\n", target_pos);

            if (board_requested){
                board_gripper.write(target_pos);
            } else {
                wire_gripper.write(target_pos);
            }
        }
    }
    delay(10);
}