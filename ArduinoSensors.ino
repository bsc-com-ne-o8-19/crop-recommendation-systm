#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>

#define ONE_WIRE_BUS 2 // Data pin for DS18B20
#define MOISTURE_PIN A0 // Analog pin for soil moisture sensor
//#define PH_PIN A1 // Analog pin for soil pH sensor
//#define NPK_PIN A2 // Analog pin for NPK sensor

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Initialize the LCD library with the numbers of the interface pins
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 6,rw = 7, d7 = 3;
LiquidCrystal lcd(rs, rw, en, d4, d5, d6, d7);

void setup() {
  // Start serial communication
  Serial.begin(9600);

  // Start DS18B20 temperature sensor
  sensors.begin();

  // Set up the LCD's number of columns and rows:
  lcd.begin(16, 2);

  // Print a message to the LCD.
  lcd.print("Soil Temp:");
}

void loop() {
  // Request temperature readings from DS18B20
  sensors.requestTemperatures();

  // Read temperature from DS18B20 in Celsius
  float temperatureC = sensors.getTempCByIndex(0);

  // Read soil moisture
  int soil_moisture = analogRead(MOISTURE_PIN);

  // Read soil pH
  //int soil_ph = analogRead(PH_PIN);

  // Read NPK sensor
  //int npk_value = analogRead(NPK_PIN);

  // If the temperature is valid
  if (temperatureC != 0) {
    // Print temperature to serial monitor
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.println(" °C");

    // Print temperature to LCD
    lcd.setCursor(0, 1);
    lcd.print("Temp: ");
    lcd.print(temperatureC);
    lcd.print("C      ");
  } else {
    // Print error message if temperature reading failed
    Serial.println("Error: Could not read temperature");
    lcd.clear();
    lcd.print("Error: Temp");
  }

  // Print soil moisture to serial monitor
  Serial.print("Soil Moisture: ");
  Serial.println(soil_moisture);

  // Print soil pH to serial monitor
  //Serial.print("Soil pH: ");
  //Serial.println(soil_ph);

  // Print NPK value to serial monitor
  //Serial.print("NPK: ");
  //Serial.println(npk_value);

  // Send sensor data to ESP32 module via serial communication
  Serial.print("SM:");
  Serial.print(soil_moisture);
  //Serial.print(",pH:");
  //Serial.print(soil_ph);
  //Serial.print(",NPK:");
 // Serial.println(npk_value);

  // Wait for a moment before taking the next reading
  delay(5000); // Update every 5 seconds
}

