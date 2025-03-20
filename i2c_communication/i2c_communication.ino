#include <Wire.h>

byte buffer[64];  // Array per memorizzare i byte ricevuti
int byteIndex = 0;

void setup() {
  // Inizializzazione della comunicazione seriale e I2C
  Serial.begin(9600);
  Wire.begin();
  delay(100);
}

void loop() {
   // Attende finché non sono stati ricevuti tutti i 64 byte
  while (byteIndex < 64){
    if (Serial.available() > 0){
      buffer[byteIndex] = Serial.read();  // Memorizza il byte ricevuto
      byteIndex++;  // Incrementa l'indice per il prossimo byte
    }
  }

    // inviamo i dati
    for (int i = 0; i < 64; i += 4){   
      byte address = buffer[i];        // Primo byte = Indirizzo I2C
      byte data1 = buffer[i+1];        // Secondo byte = Command
      byte data2 = buffer[i+2];        // Terzo byte = MSB dei dati
      byte data3 = buffer[i+3];        // Quarto byte = LSB dei dati

      // Invia i dati al dispositivo I2C
      sendToI2C(address, data1, data2, data3);
     }
     
     byteIndex = 0;
  }

// Funzione per inviare i dati tramite I2C
void sendToI2C(byte address, byte data1, byte data2, byte data3) {
  // Inizia la trasmissione I2C
  Wire.beginTransmission(address); 
  
  // Invia i 3 byte di dati
  Wire.write(data1);
  Wire.write(data2);
  Wire.write(data3);
  
  Wire.endTransmission();
  
  //Serial.print(address, HEX);
  //Serial.print("Inviato a I2C address 0x");
  //Serial.print(": ");
  //Serial.print(data1, HEX);
  //Serial.print(" ");
  //Serial.print(data2, HEX);
  //Serial.print(" ");
  //Serial.println(data3, HEX);
}
