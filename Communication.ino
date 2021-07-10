#define quantity_of_graphs 3

String graphs[quantity_of_graphs]; //names
float steps[quantity_of_graphs]; //in seconds
unsigned long last_times[quantity_of_graphs];

int pot = A0;
int reading;
String received_string;

void setup() {

  graphs[0] = "Velocity";
  steps[0] = 1;

  graphs[1] = "Current";
  steps[1] = 0.5;
  
  graphs[2] = "RPM";
  steps[2] = 0.3;

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
        Serial.println(graphs[i] + ";" + steps[i]);
      }
      Serial.println("end");
    }
  }
  
  reading = analogRead(pot);
  for(int i = 0; i < quantity_of_graphs; i++){
    if(millis() - last_times[i] >= steps[i]*1000){

      //trade for CAN entries
      if(i == 0){
        reading = reading;
      }
      else if(i == 1){
        reading = (int)reading/2 + 50;
      }
      else if(i == 2){
        reading = (int)(reading*1.5);
      }
      ///////////////////////////

      Serial.println(graphs[i] + ";" + (String)reading);
      last_times[i] = millis();
    }
  }
}
