//#include <WiFi.h>
#include <FirebaseESP32.h>

#define WIFI_SSID "iPhone"
#define WIFI_PASSWORD "Rexa12340"
#define FIREBASE_HOST "https://soil-anly-crop-recommendation-default-rtdb.europe-west1.firebasedatabase.app"
#define FIREBASE_AUTH "AIzaSyCXVEA5wcTVFIJi3WvCr1_-lVWshqZce7c"

// Define the Firebase database path
#define DATABASE_PATH "/sensors"

FirebaseData firebaseData;

void setup() {
  Serial.begin(9600);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi!");

  // Initialize Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
  // Check if WiFi is still connected
  if (WiFi.status() == WL_CONNECTED) {
    // Wait for data from Arduino Uno
    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      
      // Split data into sensor readings
      int separator_index = data.indexOf(',');
      if (separator_index != -1) {
        String moisture = data.substring(3, separator_index);
        int separator_index2 = data.indexOf(',', separator_index + 1);
        String ph = data.substring(separator_index + 4, separator_index2);
        String npk = data.substring(separator_index2 + 5);

        // Send sensor data to Firebase
        Firebase.setString(firebaseData, DATABASE_PATH "/moisture", moisture);
        Firebase.setString(firebaseData, DATABASE_PATH "/ph", ph);
        Firebase.setString(firebaseData, DATABASE_PATH "/npk", npk);
        
        if (firebaseData.httpCode() == HTTP_CODE_OK) {
          Serial.println("Data sent to Firebase!");
        } else {
          Serial.println("Failed to send data to Firebase");
          Serial.println(firebaseData.errorReason());
        }
      }
    }
  } else {
    Serial.println("WiFi disconnected. Reconnecting...");
    WiFi.reconnect();
  }

  delay(5000); // Update every 5 seconds
}
