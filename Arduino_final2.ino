
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd1(0x3E,16,2);

String inString ="";

const int M1 = 9;
const int M2 = 8;
const int N1 = 7;
const int N2 = 6;
const int EnA = 10;
const int EnB = 5;

int intData = 0;
int Lspeed = 80;
int Rspeed = 80;

void setup() {

  lcd1.begin();
  lcd1.backlight();
  
  // This baud rate must match the one set up for Pi
  Serial.begin(9600);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(N1, OUTPUT);
  pinMode(N1, OUTPUT);
  pinMode(EnA, OUTPUT);
  pinMode(EnB, OUTPUT);

}

void loop() {
  // If there is a serial message available
    
  if (Serial.available() > 0) {
    
    
    
    // Read it into our string
    String data = Serial.readStringUntil('\n');
    lcd1.setCursor(0,0);
    lcd1.print(data);

   
//    data.toInt();
    intData= data.toInt();
    
    if (intData > 320){

      Rspeed = Rspeed + 10;
      Lspeed = 100;
      
      analogWrite(EnA, Lspeed);
      analogWrite(EnB, Rspeed);

      digitalWrite(M1, HIGH);
      digitalWrite(M2, LOW);
      digitalWrite(N1, LOW);
      digitalWrite(N2, HIGH);
      }
      else if (intData < 320){
        
        Lspeed = Lspeed + 20;
        Rspeed = 100;
        
        analogWrite(EnA, Lspeed);
        analogWrite(EnB, Rspeed);
  
        digitalWrite(M1, HIGH);
        digitalWrite(M2, LOW);
        digitalWrite(N1, LOW);
        digitalWrite(N2, HIGH);
        
      
      }
      else {
        Lspeed = 100;
        Rspeed = 100;
        
        analogWrite(EnA, Lspeed);
        analogWrite(EnB, Rspeed);
  
        digitalWrite(M1, HIGH);
        digitalWrite(M2, LOW);
        digitalWrite(N1, HIGH);
        digitalWrite(N2, LOW);
        }

    String strdata = String(intData);
    Serial.print("You sent me: ");
    Serial.println(strdata);
      }
    
    


  }

    
    
