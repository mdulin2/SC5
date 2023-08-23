#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2,3); // RX, TX

/* Uncomment the initialize the I2C address , uncomment only one, If you get a totally blank screen try the other*/
#define i2c_Address 0x3c //initialize with the I2C addr 0x3C Typically eBay OLED's
//#define i2c_Address 0x3d //initialize with the I2C addr 0x3D Typically Adafruit OLED's

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1   //   QT-PY / XIAO
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


struct ticket {
  //char no[0x10];  // 0
  char firstName[0x10];  // 1
  char lastName[0x10];  // 2
  char flightNo[0x10]; // 3
  char classData[0x4]; // 4
  //char arrivalLoc[0x20]; // 5
  //char destLoc[0x20]; // 6
  //char airline[0x20]; // 7
  char seatNo[0x10]; // 8
  char secret[0x2]; // 9
};

unsigned char checksum;

struct ticket my_ticket; 

void setup()   {

  Serial.begin(9600);
  mySerial.begin(9600); // set the data rate for the SoftwareSerial port

  // Show image buffer on the display hardware.
  // Since the buffer is intialized with an Adafruit splashscreen
  // internally, this will display the splashscreen.

  delay(250); // wait for the OLED to power up
  display.begin(i2c_Address, true); // Address 0x3C default
 //display.setContrast (0); // dim display
 
  display.display();
  delay(2000);

  // Clear the buffer.
  display.clearDisplay();

  // draw a single pixel
  display.drawPixel(10, 10, SH110X_WHITE);
  // Show the display buffer on the hardware.
  // NOTE: You _must_ call display after making any drawing commands
  // to make them visible on the display hardware!
  display.display();
  delay(2000);
  display.clearDisplay();

}

// Add the data to the string
void addData(int spot, int index, char d){

  if(index >= 0x20){ // Bounds check
    return;
  }

  // if(spot == 0){
  //   my_ticket.no[index] = d; 
  // }
  if(spot == 1){
    my_ticket.firstName[index] = d; 
  }
  else if(spot == 2){
    my_ticket.lastName[index] = d; 
  }
  else if(spot == 3){
    my_ticket.flightNo[index] = d; 
  }

  else if(spot == 4){
    my_ticket.classData[index] = d; 
  }

  // else if(spot == 5){
  //   my_ticket.arrivalLoc[index] = d; 
  // }
  
  // else if(spot == 6){
  //   my_ticket.destLoc[index] = d; 
  // }
  // else if(spot == 7){
  //   my_ticket.airline[index] = d; 
  // }
  else if(spot == 8){
    my_ticket.seatNo[index] = d;
  }

  // else if(spot == 9){
  //   my_ticket.secret[index] = d;
  // }
  // Secret - don't write to here for 9

  else if(spot == 10 && checksum == 0){ // Field 10!
    checksum = (unsigned char) d;
  }
}

bool try_print_flag(){
  if(strcasecmp(my_ticket.firstName, "elon") == 0 && strcasecmp(my_ticket.lastName, "musk") == 0){
    display.setTextSize(2);
    display.setTextColor(SH110X_WHITE);
    char flag[13] = {'S', 'C', '5', '{', 'B', '@', 'd','N', '8', 'M', 'e', '}', '\0'};
    display.print(flag);
    display.display();
    return true;
  }

  if(strcasecmp(my_ticket.classData, "F") == 0){
    display.setTextSize(2);
    display.setTextColor(SH110X_WHITE);
    char flag[15] = {'S', 'C', '5', '{', 'B', '&', 'd','C', 'l', 'a', 'S', 'S', '!', '}', '\0'};
    display.print(flag);
    display.display();
    return true;
  }

  // Secret has a value. Shouldn't be able to set this.
  if(strcasecmp(my_ticket.secret, "") != 0){
    display.setTextSize(2);
    display.setTextColor(SH110X_WHITE);
    char flag[15] = {'S', 'C', '5', '{', 'A', 'V', 'R','B', '0', 'F', '&', '}', '\0'};
    display.print(flag);
    display.display();
    return true;
  }
  return false;
}


void loop()
{
  if (mySerial.available()) // Check if there is Incoming Data in the Serial Buffer.
  {
    display.setCursor(0, 0); //oled display
 
    memset(&my_ticket, 0, sizeof(struct ticket));  // Clear ticket from previous round
    int field = 0;
    int index = 0;
    bool valid = false;
    unsigned char checksum_new = 0; // Make into 'long long' then mod by 256 myself?
    checksum = 0;

    while (mySerial.available()) // Keep reading Byte by Byte from the Buffer till the Buffer is empty
    {
      char input = mySerial.read(); // Read 1 Byte of data and store it in a character variable

      // Don't want to checksum the checksum field!
      if(field <= 9){
        checksum_new += (unsigned char) input; 
      }

      Serial.print(input); // Print the Byte

      // Parse the incoming data
      if(input == '|'){
        addData(field, index, '\x00'); // Add in a nullbyte to the end of the string
        index = 0;
        field += 1;
        continue; 
      }
      addData(field, index, input);
      delay(5);

      index += 1;
    }
    
    // If we have a complete ticket
    if(field >= 9){ // Change to 9
      valid = true;
    }

    // Must be a valid ticket in order to TRY to print the flag.
    if(valid == false){
      display.setTextSize(2);
      display.setTextColor(SH110X_WHITE);
      char str[20] = {'B','A','D',' ', 'T','I','C','K','E','T'};
      display.print(str);
      display.display();
    }
    else {
      if(try_print_flag() == false){
        display.setTextSize(2);
        display.setTextColor(SH110X_WHITE);
        char str[20] = {'H','E','L','L', 'O',' ', '\0'};
        display.print(str);
        display.print(my_ticket.firstName);
        display.display();
      }

      // Proper checksum
      if(checksum == checksum_new && strcasecmp(my_ticket.flightNo, "9675309") == 0){
        display.setCursor(0, 0); //oled display
        display.clearDisplay();
        display.setTextSize(2);
        display.setTextColor(SH110X_WHITE);
        char flag[20] = {'S', 'C', '5', '{', 'C', 'h', '3','e', '7', 'Y', 'o', 's', '3', '1', 'f', '}', '\0'};
        display.print(flag);
        display.display();
      }
    }

    // Sleep for 7 seconds then clear screen
    delay(7000);
    Serial.println();
    display.clearDisplay();
    display.setCursor(0, 0); //oled display

    //char str[12] = {'S','C','A','N', ' ','T', 'I','C','K','E','T', '\0'};
    display.print("");
    display.display();
    display.clearDisplay();
  }
}

/*
Use https://qrcode.tec-it.com/en to generate QR Codes.
Flags: 

Challenge 2:
- Set first and last name of ticket to elon musk 
- '1111|elon|musk|22222|E|Austin|Spokane|Alaska|22C|Secret|1|' 


Challenge 3: 
- Set ticket to be first class 
- '1111|Bill|Gates|22222|F|Austin|Spokane|Alaska|22C|Secret|1|'

Challenge 4:
- Find a way to set the 'secret' value.
- '1111|Bill|Gates|22222|E|Austin|Spokane|Alaska|AAAAAAAAAAAAAAAAAAAAAAAAAAA|Secret|1|'

Challenge 5: 
- Create a checksum in the final slot with the final number '9675309'.
- '111111|Maxwell|Dulin|9675309|E|Austin|Spokane|Alaska|22C|Secret|/|'

Code for checksum: 
string="XX"
for char in string:
  d = d + ord(char)
print(d % 256) 
*/
