#include <IRremote.h>

/*
*  Default is Arduino pin D11.
*  You can change this to another available Arduino Pin.
*  Your IR receiver should be connected to the pin defined here
*/
#define RECV_PIN A2
#define LEDpin 15
#define Max_IR 4

IRrecv irrecv(RECV_PIN);
IRsend irsend;


decode_results results;
uint16_t last_value =0;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
  digitalWrite(LEDpin, LOW);
  pinMode(LEDpin, OUTPUT);
}


void dump(decode_results *results) {
  // Dumps out the decode_results structure.
  // Call this after IRrecv::decode()
  int count = results->rawlen;
  if (results->decode_type == UNKNOWN) {
    Serial.print("Unknown encoding: ");
  }
  else if (results->decode_type == NEC) {
    Serial.print("Decoded NEC: ");

  }
  else if (results->decode_type == SONY) {
    Serial.print("Decoded SONY: ");
  }
  else if (results->decode_type == RC5) {
    Serial.print("Decoded RC5: ");
  }
  else if (results->decode_type == RC6) {
    Serial.print("Decoded RC6: ");
  }
  else if (results->decode_type == PANASONIC) {
    Serial.print("Decoded PANASONIC - Address: ");
    Serial.print(results->address, HEX);
    Serial.print(" Value: ");
  }
  else if (results->decode_type == LG) {
    Serial.print("Decoded LG: ");
  }
  else if (results->decode_type == JVC) {
    Serial.print("Decoded JVC: ");
  }
  else if (results->decode_type == AIWA_RC_T501) {
    Serial.print("Decoded AIWA RC T501: ");
  }
  else if (results->decode_type == WHYNTER) {
    Serial.print("Decoded Whynter: ");
  }
  Serial.print(results->value, HEX);
  Serial.print(" (");
  Serial.print(results->bits, DEC);
  Serial.println(" bits)");
  Serial.print("Raw (");
  Serial.print(count, DEC);
  Serial.print("): ");

  for (int i = 1; i < count; i++) {
    if (i & 1) {
      Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
    }
    else {
      Serial.write('-');
      Serial.print((unsigned long) results->rawbuf[i]*USECPERTICK, DEC);
    }
    Serial.print(" ");
  }
  Serial.println();
}

void TV_on()
{
  int i = 0;
  while (i<Max_IR)
   {
     irsend.sendNEC(0x20DF10EF,32);  // Power on LG TV
     delay(40);
     i++;
   }
}

void LED_on()
{
  int i = 0;
  while (i<Max_IR)
   {
     irsend.sendNEC(0xFFB04F,32);  // Power on LED strip
     delay(40);
     i++;
   }
}

void loop() {
  if (irrecv.decode(&results)) {
    if (results.decode_type== RC5)
    {
      if (((results.value & 0x5ff)==0x541)&(!Serial)&(last_value!=results.value))
      {
        TV_on();
        LED_on();
        irrecv.enableIRIn();
        digitalWrite(LEDpin, HIGH);
        delay(100);
      }
      else
      {    Serial.println(results.value, HEX);
          // dump(&results);
      }
      last_value=results.value;
    }

        // Serial.println(results.decode_type);
    irrecv.resume(); // Receive the next value
  }
  digitalWrite(LEDpin, LOW);

}
