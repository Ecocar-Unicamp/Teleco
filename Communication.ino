int capacity = 20;

struct infograph{
  String nameOfGraph;
  String unityOfMeasurement;
  double stepOfGraph;
  String maximumValueAlert; // may be null
  String minimumValueAlert;
  unsigned long lastCollectingTime;
};

typedef struct infograph infograph;

infograph** listOfInfographs = (infograph**) calloc(capacity, sizeof(infograph*));

void addInfograph(String nameOfGraph, String unityOfMeasurement, double stepOfGraph, String maximumValueAlert = "", String minimumValueAlert = ""){
  int i = 0;
  while(listOfInfographs[i] != NULL){
    i++;
    if(i >= capacity){
      return;
    }
  }
  infograph* added = calloc(1, sizeof(infograph));
  added->nameOfGraph = nameOfGraph;
  added->unityOfMeasurement = unityOfMeasurement;
  added->stepOfGraph = stepOfGraph;
  added->maximumValueAlert = maximumValueAlert;
  added->minimumValueAlert = minimumValueAlert;
  listOfInfographs[i] = added;
}

String infographsInfo(int i){
  return listOfInfographs[i]->nameOfGraph + ";" + listOfInfographs[i]->stepOfGraph + ";" + 
  listOfInfographs[i]->unityOfMeasurement + ";" + listOfInfographs[i]->maximumValueAlert + ";" + listOfInfographs[i]->minimumValueAlert;
}

int pot = A0;
double reading;
double treated_reading; ///////////////////////////////////////////////////////remove this
String received_string;

void setup() { 
  //addInfograph(String nameOfGraph, String unityOfMeasurement, double stepOfGraph, String maximumValueAlert = "", String minimumValueAlert = "")
  addInfograph("Velocity", "km/h", 2.3, "900", "0");
  addInfograph("Current", "mA", 0.5, "6", "4");
  addInfograph("RPM", "Hz", 1, "6", "4.5");
  addInfograph("Temperature", "ºC", 0.7, "0.7", "0.5");
  addInfograph("Inclinação", "°", 1.7, "5000");
  addInfograph("NomeGrandeComoReferencia", "PassoGrandeComoReferencia", 0.3, "25");

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
      for(int i = 0; i < capacity && listOfInfographs[i] != NULL; i++){
        Serial.println(infographsInfo(i));
      }
      Serial.println("end");
    }
  }
  
  reading = analogRead(pot);
  unsigned long currentTime = millis();
  for(int i = 0; i < capacity && listOfInfographs[i] != NULL; i++){
    if(currentTime - listOfInfographs[i]->lastCollectingTime >= 1000 * listOfInfographs[i]->stepOfGraph){
      listOfInfographs[i]->lastCollectingTime = currentTime;

      //trade for CAN entries
      if(i == 0){
        treated_reading = 1000 - 3*reading;
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

      Serial.println((String)i + ";" + treated_reading + ";");
    }
  }
}
