#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "afr2903";
const char* password = "12345678"; // Set password
const int udpPort = 1234;

WiFiUDP udp;

IPAddress staticIP(192, 168, 18, 23); // Set the desired static IP address
IPAddress gateway(192, 168, 18, 1);    // Set the gateway of your network
IPAddress subnet(255, 255, 255, 0);    // Set the subnet mask of your network

String instructions[] = {
  "HOME",
  "PICK_ARDUINO",
  "PLACE_ARDUINO",
  "PICK_RAMPS",
  "PLACE_RAMPS",
  "PICK_DRIVER",
  "PLACE_DRIVER",
  "PICK_WIRE",
  "PLACE_WIRE",
  "PICK_ASSEMBLY",
  "PLACE_ASSEMBLY"
};

void setup() {
  Serial.begin(115200);
  Serial.println();
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  
//  Serial.print("Default Gateway: ");
//  Serial.println(WiFi.gatewayIP());
//  Serial.print("Subnet Mask: ");
//  Serial.println(WiFi.subnetMask());
//  Serial.print("IP Address: ");
//  Serial.println(WiFi.localIP());

  WiFi.config(staticIP, gateway, subnet);

  Serial.print("Current ip: ");
  Serial.println(WiFi.localIP());
  

  udp.begin(udpPort);
  Serial.println("UDP server started");
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
    char incomingPacket[255];
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
      Serial.print("Entering first if");
      // Trim leading and trailing whitespaces
      String message_completed;
      for (int i = 0; i < len; i++) {
        char letter = incomingPacket[i];
        if (letter != ' ') {
          message_completed += letter;
        Serial.println(letter);
        Serial.println(message_completed);
        }
      }
      String target_instruction = instructions[message_completed.toInt()];
      Serial.printf("UDP packet contents: %s\n", target_instruction.c_str());
      // Send confirmation message
    }
  }
  delay(10);
}