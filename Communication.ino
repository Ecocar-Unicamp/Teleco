#define quantity_of_graphs 6

String graphs[quantity_of_graphs]; //names
float steps[quantity_of_graphs]; //in seconds
String uom[quantity_of_graphs]; //unit of measurement
unsigned long last_times[quantity_of_graphs];

int pot = A0;
float reading;
float treated_reading; //remove this
String received_string;

void setup() {

  graphs[0] = "Velocity";
  steps[0] = 2.3;
  uom[0] = "km/h";

  graphs[1] = "Current";
  steps[1] = 0.5;
  uom[1] = "mA";
  
  graphs[2] = "RPM";
  steps[2] = 1;
  uom[2] = "Hz";

  graphs[3] = "A";
  steps[3] = 0.7;
  uom[3] = "ua";

  graphs[4] = "B";
  steps[4] = 1.7;
  uom[4] = "ub";

  graphs[5] = "C";
  steps[5] = 0.3;
  uom[5] = "uc";

  for(int i = 0; i < quantity_of_graphs; i++){
    last_times[i] = 0;
  }

  
  Serial.begin(9600);
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}

void loop() {
  if (Serial.available() > 0) {
    received_string = Serial.readStringUntil('\n');
    if(received_string == "connect"){
      Serial.println("begin");
      for(int i = 0; i < quantity_of_graphs; i++){
        Serial.println(graphs[i] + ";" + steps[i] + ";" + uom[i]);
      }
      Serial.println("end");
    }
  }
  
  reading = analogRead(pot);
  for(int i = 0; i < quantity_of_graphs; i++){
    if(millis() - last_times[i] >= steps[i]*1000){

      //trade for CAN entries
      if(i == 0){
        treated_reading = reading;
      }
      else if(i == 1){
        treated_reading = 5 + sin(reading);
      }
      else if(i == 2){
        treated_reading = 5 + cos(reading);
      }
      else if(i == 3){
        treated_reading = pow(2,(-1)*reading/100);
      }
      else if(i == 4){
        treated_reading = pow(reading,2);
      }
      else if(i == 5){
        treated_reading = (-1)*reading;
      }
      ///////////////////////////

      Serial.println((String)i + ";" + (String)treated_reading);
      last_times[i] = millis();
    }
  }
}
