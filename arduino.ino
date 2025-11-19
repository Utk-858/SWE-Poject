#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// ----------------------------------------------------------------
// 1. CONFIGURATION
// ----------------------------------------------------------------

// WIFI
const char* ssid = "iPhone";
const char* password = "Utkarsh001";

// THINGSPEAK MQTT
const char* mqtt_server = "mqtt3.thingspeak.com";
const char* mqtt_client_id = "CiQfIhA9GSQpFDcyDAEdNyA"; 
const char* mqtt_user = "CiQfIhA9GSQpFDcyDAEdNyA";
const char* mqtt_password = "41LbJsUOg0spmSuSJwU5Z2NP";
const char* publish_topic = "channels/3170362/publish"; 

// DHT SENSOR
#define DHTPIN 15     // Pin connected to the DHT Data pin
#define DHTTYPE DHT11 // Change to DHT22 if you are using that one
DHT dht(DHTPIN, DHTTYPE);

// ----------------------------------------------------------------

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_INTERVAL 1500 // 20 seconds (Safe for ThingSpeak free tier)

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(mqtt_client_id, mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin(); // Start the sensor
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > MSG_INTERVAL) {
    lastMsg = now;

    // --- READ DATA FROM SENSOR ---
    float t = dht.readTemperature(); // Read Temperature (Celsius)
    float h = dht.readHumidity();    // Read Humidity
    
    // Check if any reads failed
    if (isnan(t) || isnan(h)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // --- CREATE PAYLOAD ---
    // Field 1 = Temp, Field 2 = Humidity
    String payload = "field1=" + String(t) + "&field2=" + String(h);
    
    Serial.print("Publishing: ");
    Serial.println(payload);
    
    client.publish(publish_topic, payload.c_str());
  }
}