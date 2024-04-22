#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>

#define ONE_WIRE_BUS 2 // Data pin for DS18B20

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Initialize the LCD library with the numbers of the interface pins
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 6, d7 = 3;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

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

  // If the temperature is valid
  if (temperatureC != DEVICE_DISCONNECTED_C) {
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

  // Wait for a moment before taking the next reading
  delay(1000);
}

