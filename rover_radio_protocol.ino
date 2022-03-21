// Header file for the manager
#include <RHReliableDatagram.h>
#include <RH_RF95.h>
#include <SPI.h>
#include <math.h>

// The rover must know its own address and the address of the base station
// The client address must ALWAYS be > 2 ( 1 - Base, 2 - Pin)
#define CLIENT_ADDRESS 3
#define BASE_ADDRESS 1

// Some global definitions for Base Address and Pin Mappings
#define RFM95_CS 5 // Chip Select /  Slave Select 
#define RFM95_RST 6 //  SPI Radio Reset
#define RFM95_INT 10 // SPI Radio Interrupt

// Frequency of SPI radio
#define RF95_FREQ 434.0

// External interrupt Pin
const uint8_t external_interrupt = 13;

// FLAGS //

///// RTCM ///////////////////////////////////////////////////////
// this flag signifies that the receiver must prepare to receive 
// RTCM correction data
int rtcm_flag = 0;
int rtcm_transmission_time = 500;
//////////////////////////////////////////////////////////////////


///// RELPOS / FINISH ////////////////////////////////////////////
bool check_for_finish = false;
int check_relpos = 0;
// this flag signifies that there are TWO valid positions stored
// if there is only one valid position, we cannot interpolate
int valid_positions = 0; 
// the boat finish in this period, this flag prepares for the result 
// to be sent in the next period
int boat_finished = 0;
// this flag permits the result to be sent in the CURRENT period
int can_send_finish = 0;
// the timeslot in which the boat can transmit its finish time
int timeslot_number = 0;
// time in milliseconds of the width of a finish time transmission slot
int finish_time_slot = 30; 
int guard_interval = 5;

// used for when finish time is ackowledged, so just wait for next race
int idle = 0;

int current_timestamp = 0;
int current_rover_north = 0;
int current_rover_east = 0;

int prev_timestamp = 0;
int prev_rover_north = 0;
int prev_rover_east = 0;
/////////////////////////////////////////////////////////////////

////// OTHER FLAGS //////////////////////////////////////////////

// this value signifies the time at which the timepulse arrived
// relative the the number of seconds since MCU program start
unsigned long flag_time;

////////////////////////////////////////////////////////////////


/// Relative Position & finish Time Buffers  /////////////////
// the previous relative positoin location
uint8_t previous_pos[12];
// the most recent relative position location
uint8_t current_pos[12];
// buffer to store full UBX-NAV-RELPOSNED Message
char current_relposned[48];
// integer to hold finish time 
int finish_time = 0;

//////////////////////////////////////////////////////////////

/// Status Message Buffer ///////////////////////////////////
// full message (2 byte Status, 8 byte Pin)
uint8_t size_of_status_message = 8;
uint8_t status_buffer[size_of_status_message];
uint8_t status_bytes[2];
uint8_t pin_location[8];
////////////////////////////////////////////////////////////

//Sample data
uint8_t data[] = "I have finished!";

//////// SPI Radio ////////////////////////////////////////////////// 
//SPI Radio Buffer - holds all incoming spi radio messages
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];

// Singleton instance of the radio driver
RH_RF95 driver(RFM95_CS, RFM95_INT);

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram rover(driver, CLIENT_ADDRESS);

//////////////////////////////////////////////////////////////////////

// ISR for external interrupt
void toggle(){
    // the boat has finished, no longer cares about RTCM
    if(boat_finished == 1){
       rtcm_flag = 0;
       can_send_finish = 1;
       boat_finished = 0;
     }
   
    // RTCM  flag is set, to preapre for reception over serial
    else{
      rtcm_flag = 1;  
      check_relpos = 1;
    }
    
    // Set time of flag using the millis() function
    flag_time = millis();
  }

void setup() 
{
  // set the mode of the external interrupt pin 
  pinMode(external_interrupt, INPUT);
  // Attach interrupt
  attachInterrupt(digitalPinToInterrupt(external_interrupt), toggle, RISING);
 
  //USB for debug
  Serial.begin(38400);
  //USART TX and RX pins for sending Received RTCM data to GPS
  Serial1.begin(115200);

  Serial1.setTimeout(1);
  while (!Serial) ; // Wait for serial port to be available

  //Initialise manager class and hence the radio with default settings
 
  ////////////////// Defaults //////////////////
  /// Frequency 434MHz                       ///
  /// Tx Power: 13dBm                        ///
  /// Bandwidth: 125KHz                      ///
  /// Coding Rate: 4/5    (1)                    ///
  /// Spreading Factor: 128 chips/ Symbol(7) ///
  /// CRC On                                 ///
  //////////////////////////////////////////////


  // Note HOPERF RFM96 module uses a PA_BOOST transmitter pin 
  // Power Range: 5 to 23 dBm:
  // Example rover.setTxPower(23, false);
  if (!rover.init())
    Serial.println("init failed");
  else
    Serial.println("init succesful");
}



// function to handle a message (either RTCM or Status)
void handle_message(uint8_t len){
  Serial.print("message");
  if(buf[0] == 0xD3){
    Serial1.write(buf, len);
  }
  else if(len == size_status_message){
      memcpy(pin_location, len);
      Serial.println("PIN");
    }
}

char preamble;

bool retrieve_relposned(){
    // following the UBX protocol
    // UBX-NAV_RELPOSNED is 46 Bytes long, the rover is concerned with three elements of this message only:
    // The Northern Offset of the pin from the committee boat
    // The Eastern Offseet of the pin from the committee boat
    // The timestamp in ms, generated by the GNSS unit
    
    if(Serial1.available() > 0){

      preamble = Serial1.read();
      while(preamble != 0xB5)
        preamble = Serial1.read(); 
      // this is to ensure that there are two valid positions before assigning previous_pos a value
      if(valid_positions == 1){
         prev_timestamp = current_timestamp;
         prev_rover_north = current_rover_north;
         prev_rover_east = current_rover_east;
      }
      
      // read the new relative position
      Serial1.readBytes(current_relposned, 47);
  
      // extract relevant info from RELPOSNED message
      int validity_check_north = current_relposned[13] | ( current_relposned[14] << 8 ) | ( current_relposned[15] << 16 ) | ( current_relposned[16] << 24 );
      int validity_check_east = current_relposned[17] | ( current_relposned[18] << 8 ) | ( current_relposned[19] << 16 ) | ( current_relposned[20] << 24 );
      //if North and East are both zero, the position is invalid
      if(validity_check_north != 0 && validity_check_east != 0){
       // only update if position is valid
        current_timestamp =  current_relposned[9] | ( current_relposned[10] << 8 ) | ( current_relposned[11] << 16 ) | ( current_relposned[12] << 24 );
        current_rover_north =  validity_check_north;
        current_rover_east =   validity_check_east;
      }

      //Debug Messages
      Serial.println(current_rover_north);
      Serial.println(current_rover_east);
      Serial.println(current_timestamp);
      //for(int i=0; i<48;i++) Serial.print(current_relposned[i], HEX);
      Serial.println();
      
      check_relpos = 0;
      return true;
    }
    else
      return false;
  }

bool check_if_finished(){
  
   int pin_north = pin_location[0] | ( pin_location[1] << 8 ) | ( pin_location[2] << 16 ) | ( pin_location[3] << 24 );
   int pin_east = pin_location[4] | ( pin_location[5] << 8 ) | ( pin_location[6] << 16 ) | ( pin_location[7] << 24 );
   

   // boat has crossed the line, time to get finish time 
   if(current_rover_east*pin_north > current_rover_north*pin_east){

      // Here, some calcualtions are required to interpolate for the finish time
      float finish_line_slope = pin_east/pin_north; 
      float rover_slope = (current_rover_east - prev_rover_east)/(current_rover_north - prev_rover_north);
    
      float point_of_intersection_north = (-rover_slope * prev_rover_north + prev_rover_east)/(finish_line_slope - rover_slope);
      float point_of_intersection_east = (rover_slope)*(point_of_intersection_north - prev_rover_north) + prev_rover_east;

      // to find finsh time, see how far alongthe line segment (Previous, Next) the point of intersection is. Since the time between both
      // RELPOSNED messages is exactly 1 second, a approximate finish time to the nearest millisecond can be calculated.
      float factor_previous = hypot((point_of_intersection_north - prev_rover_north), (point_of_intersection_east - prev_rover_east));
      // find the length between the two relative positions
      float factor_current = hypot((current_rover_north - prev_rover_north), (current_rover_east - prev_rover_east));

      // UBX reports time in milliseconds, so to find the factor between to 1 second reports, multiply by 1000 ms
      finish_time = prev_timestamp + (factor_previous/factor_current)*1000;
      Serial.println(prev_timestamp);
      return true;
    } 
  }


void self_assign_timeslot(){
  timeslot_number = random(20);
  boat_finished = 1;
}

void loop() {
    if(idle == 1){
       // wait until new race has started (How????)
      }
    // time allocated time slot for inbound RTCM is finished, set the flag to 0
    if(rtcm_flag == 1 && (millis() - flag_time > 500)){
      // Debug message
      Serial.println("End RTCM");
      rtcm_flag = 0;
    }
    // flag is 1, epect to receive corrections
    if(rtcm_flag == 1){
      // first check for RELPOSNED Message
        if(check_relpos == 1){
          if(retrieve_relposned()){
            if (valid_positions  == 0){
              valid_positions = 1;
            }
            else{
              check_for_finish = true;
              }
          }
        }
        // RTCM flag is one but timeslot has not expired
        uint8_t len = sizeof(buf);
        uint8_t from; 
        if(rover.recvfrom(buf, &len))
          handle_message(len);          
      }
      // Boat has crossed the line on the previous period, time
      // to inform the committee 
   /* else if(can_send_finish == 1){
        if(millis() - flag_time >= (flag_time + (timeslot_number*finish_time_slot) + guard_interval))
        // timeslot has expire, finish time has been determined
        // boat have crossed the line, needs to inform committee
        
        if(rover.sendtoWait(data, sizeof(data), BASE_ADDRESS)){
          Serial.println("Ack Received");
           idle = 1;
           can_send_finish = 0;
        }
        else{
            // set this to zero so the rover must wait unitl next time period
            can_send_finish = 0;
            // reassign a new timeslot
            self_assign_timeslot();
          }  
     }*/
      else if(check_if_finished()){
            self_assign_timeslot();
          }
 
}
