#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "CAPITALIST";
const char* password = "123456789";

// Server settings
const char* serverIP = "192.168.101.164";
const int serverPort = 5000;
String serverBaseURL = "http://" + String(serverIP) + ":" + String(serverPort);

// Pin configuration
#define LDR_PIN 34              // Analog input from LDR (ADC1)
#define PIR_PIN 35              // Digital input from PIR motion senso
#define LED_PIN 2               // Simulate LED strip
#define FAN_PWM_PIN 25          // Analog output for fan speed (DAC/PWM capable)

unsigned long previousMillis = 0;
const long interval = 500;

void setup() {
  Serial.begin(9600);

  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(FAN_PWM_PIN, OUTPUT); // will use ledcAttach for PWM

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  // Setup PWM on FAN pin (PWM channel 0)
  ledcSetup(0, 5000, 8);           // Channel 0, 5kHz, 8-bit resolution
  ledcAttachPin(FAN_PWM_PIN, 0);  // Attach FAN_PWM_PIN to PWM channel 0
}

// ... (previous setup code unchanged)

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    
    int lightLevel = analogRead(LDR_PIN);
    int scaledLight = map(lightLevel, 0, 4095, 0, 100);
    int motionRaw = digitalRead(PIR_PIN); 

    Serial.print("Light Intensity: ");
    Serial.println(scaledLight);
    Serial.print("Motion Detected: ");
    Serial.println(motionRaw == 1 ? "Yes" : "No");

    if (WiFi.status() == WL_CONNECTED) {
      
      HTTPClient http;
      String postURL = serverBaseURL + "/esp/update";
      http.begin(postURL);
      http.addHeader("Content-Type", "application/json");

      StaticJsonDocument<200> postDoc;
      postDoc["light"] = scaledLight;
      postDoc["motion"] = motionRaw;

      String payload;
      serializeJson(postDoc, payload);
      int postCode = http.POST(payload);

      if (postCode > 0) {
        Serial.println("Sensor data POSTed");
      } else {
        Serial.print("POST failed: ");
        Serial.println(http.errorToString(postCode));
      }
      http.end();

      // === GET control settings from server ===
      HTTPClient http2;
      String getURL = serverBaseURL + "/esp/control";
      http2.begin(getURL);
      int getCode = http2.GET();

      if (getCode > 0) {
        String response = http2.getString();
        Serial.println("GET response: " + response);

        StaticJsonDocument<200> getDoc;
        DeserializationError error = deserializeJson(getDoc, response);

        if (!error) {
          int led = getDoc["led"];                      
          int fanSpeed = getDoc["fan_speed"];           
          int ledOverride = getDoc["led_override"];     

          
          ledcWrite(0, fanSpeed);

          // ----- LED CONTROL -----
          if (ledOverride == 1) {
            digitalWrite(LED_PIN, led == 1 ? HIGH : LOW);
            Serial.println("LED Override: Manual from app");
          } else {
            if (motionRaw == 1 ) {
              if (scaledLight < 30) {
                digitalWrite(LED_PIN, HIGH);
                Serial.println("LED Auto ON: Dark & Motion");
              } else {
                digitalWrite(LED_PIN, LOW);
                Serial.println("LED Auto OFF: Bright despite Motion");
              }
            } else {
              digitalWrite(LED_PIN, LOW);
              Serial.println("LED Auto OFF: No Motion");
            }
          }
        } else {
          Serial.print("JSON Error: ");
          Serial.println(error.c_str());
        }
      } else {
        Serial.print("GET error: ");
        Serial.println(http2.errorToString(getCode));
      }
      http2.end();

    } else {
      Serial.println("WiFi not connected");
    }
  }
}
