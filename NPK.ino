#include <SoftwareSerial.h>
#include <Wire.h>
//#include <Adafruit_GFX.h>
//#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT
#define OLED_RESET -1
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define RE 8
#define DE 7

//const byte nitro[] = {xxxx, xxxx, xxxx, xxxx, xxxx, xxxx, xxxx, xxxx};
  const byte nitro[] = {};
  const byte phos[] = {};
  const byte pota[] = {};
  byte values[11];
  SoftwareSerial mod(2,3);
  

void setup() {
  // put your setup code here, to run once:

 Serial.begin(9600);
 mod.begin(9600);
 pinMode(RE, OUTPUT);
 pinMode(DE, OUTPUT);

 display.begin(SSD1306_SWITCHCAPVCC, 0x3C); //initialize with the 12C addr 0x3C
 delay(500);
 display.clearDisplay();
 display.setCursor(25, 15);
 display.setTextSize(1);
 display.setTextColor(WHITE);
 display.println("NPK Sensor");
 display.setCursor(25, 35);
 display.setTextSize(1);
 display.print("Initializing");
 display.display();
 delay(3000);
}

void loop() {
  // put your main code here, to run repeatedly:
byte va11,val2,val3;
val1 = nitrogen();
delay(250);
val2 = phosphorus();
delay(250);}

Serial.print("Nitrogen: ");
Serial.print(val1);
Serial.println(" mg/kg ");

Serial.print("Phosphorous: ");
Serial.print(val2);
Serial.println(" mg/kg ");

Serial.print("Potassium: ");
Serial.print(val3);
Serial.println(" mg/kg ");
delay(2000);

display.clearDisplay();

display.setTextSize(2);
display.setCursor(0, 5);
display.print("N: ");
display.print(val1);
display.setTextSize(1);
display.print(" mg/kg");

display.setTextSize(2);
display.setCursor(0, 25);
display.print("P: ");
display.print(val2);
display.setTextSize(1);
display.print(" mg/kg");

display.setTextSize(2);
display.setCursor(0, 45);
display.print("K: ");
display.print(val3);
display.setTextSize(1);
display.print(" mg/kg");

display.display();
}

byte nitrogen() {
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);
  if(mod.write(nitro,sizeof(nitro))==8){
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  for(byte i=0;i<7;i++){
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();
}
return values[4];
}

byte phosphorus(){
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);
  if(mod.write(phos,sizeof(pota))==8){
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  for(byte i=0;i<7;i++){
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();
}
return values[4];
}

byte potassium(){
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);

if(mod.write(pota,sizeof(pota))==8){
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  for(byte i=0;i<7;i++){
    values[i] = mod.read();
    Serial.print(values[i], HEX);
  }
  Serial.println();
}
return values[4];
}
}
