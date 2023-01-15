#define redAnalog 11 // NOTE: analog is btwn 0 and 255!
#define greenAnalog 10
#define blueAnalog 9
#define buttonPin 2

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(redAnalog, OUTPUT);
  pinMode(greenAnalog, OUTPUT);
  pinMode(blueAnalog, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
}
// EACH ASCII CHAR IS 1 BYTE 8 BITS
const char sendingChar = 'B'; // const since the only code being sent from arduino is B
char receivingChar;

int prevButtonState = 1;
int currentButtonState;

// list of potetially useful serial commands
// Serial.find()

// function prototyping
void recChar(void);
void sendChar(void);

void loop()
{
  currentButtonState = digitalRead(buttonPin);
  if (currentButtonState == 0 & prevButtonState == 1){ // all code within if statement will only run ONCE on the down stroke of button
    sendChar(); // function sends const char B indicating to python that it should begin
    recChar(); //update receivingChar variable to "hopefully" what the status of spotify is
    switch (receivingChar) //always checking the receivingChar variable to see if python returned info
  {
  case 'N': // there is either no current song or it is paused
    analogWrite(redAnalog, 50);
    receivingChar = ' ';
    break;
  case 'A': // song is Already liked
    analogWrite(greenAnalog, 50);
    analogWrite(blueAnalog, 50);
    receivingChar = ' ';
    break;
  case 'W': // song Will be liked
    analogWrite(greenAnalog, 50);
    receivingChar = ' ';
    break;
  default:
    break;
  }
  delay(500);
  analogWrite(redAnalog, 0);
  analogWrite(greenAnalog, 0);
  analogWrite(blueAnalog, 0);
  }

  prevButtonState = currentButtonState;//update previous button state var
}

void recChar()
{
  while(Serial.available() == 0){ //check if the serial buffer is empty
  }
  receivingChar = Serial.read(); // if there is a byte in buffer, update receivingChar
  Serial.read(); //clear the buffer
}

void sendChar()
{ // sending char is being updated simply for debugging purposes to make sure the correct data is sent
  Serial.write(sendingChar);
}
