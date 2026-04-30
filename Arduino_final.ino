const int led = 13;
String inString ="";

const int M1 = 7;
const int M2 = 6;
const int N1 = 5;
const int N2 = 4;
const int EnA = 9;
const int EnB = 3;

int intdata = 0;
int Lspeed = 100;
int Rspeed = 100;

void setup() {
  
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

   
    
    intdata= data.toInt();
    if (intdata > 320){

      Rspeed = Rspeed + 20;
      Lspeed = 100;
      
      analogWrite(EnA, Lspeed);
      analogWrite(EnB, Rspeed);

      digitalWrite(M1, HIGH);
      digitalWrite(M2, LOW);
      digitalWrite(N1, HIGH);
      digitalWrite(N2, LOW);
      }
      else if (intdata < 320){
        Lspeed = Lspeed + 20;
        Rspeed = 100;
        
        analogWrite(EnA, Lspeed);
        analogWrite(EnB, Rspeed);
  
        digitalWrite(M1, HIGH);
        digitalWrite(M2, LOW);
        digitalWrite(N1, HIGH);
        digitalWrite(N2, LOW);
        
      
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
      }
    
    String strdata = String(intdata);
    Serial.print("You sent me: ");
    Serial.println(strdata);


  }

    
    
