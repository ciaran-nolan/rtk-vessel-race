// Radio Protocol using the Airspayce Packet Radio Library

// Include Headers: Note Reliable Datagram inherits most of regular datagram so this is 
// suitable for use
// Airspayce Packet Radio Library 
#include <RHReliableDatagram.h>
#include <RH_RF95.h>
///
#include <SPI.h>

// Some global definitions for Base Address and Pin Mappings
#define SERVER_ADDRESS 1
#define RFM95_CS 5 // SPI Chip/ Slave Select
#define RFM95_RST 6 // SPI Reset
#define RFM95_INT 10 // SPI Interrupt

// Some other flag vars for ISR etc.
//Define the max buffer size = 255 bytes
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
const uint8_t external_interrupt = 13;
int rtcm_flag = 0;
unsigned long flag_time;


/// PIN and Status ///
// array to  
uint8_t pin[8] = {0};
// array to hold 16 bits which make the two byte status
uint8_t status_bytes[16] = {0};

uint8_t status_message[10];
////////////////

///// RTCM Variables /////

int marker = 0;
int data_size = 0;
byte markers[3];
int num_messages = 0;
byte preamble = 0xD3;
// an array to hold the size of each message
uint8_t sent_sizes[4] = {0,0,0,0};
// a var to hold the size of the current message to be sent
uint8_t size_to_send = 0;
// 2 byte array to collect the first two received bytes, which tell the size of the payload
char payload_size[2];
// Since the RTCM protocol is not freely available to identify each message as they arrive
// They are simply held in "message" arrays"
// The max theoretical size of a message is: 
// 2^10 = 1024 byte payload 
// 3 bytes of header (8 bits Preamble, 6 Reserved bits, 10 bit Data Size)
// 24 bit CRC
// Each Message: Max 1030 bytes
// Maximum RTCM = 4*1030 = 4120 bytes
char rx_data[4120];
uint8_t message_1[1030];
uint8_t message_2[1030];
uint8_t message_3[1030];
uint8_t message_4[1030];

/////// END RTCM Variable //////////////////////////////////////////////

/// SPI Radio Driver and Manager Instances //////
// Singleton instance of the radio driver
RH_RF95 driver(RFM95_CS, RFM95_INT);
// Class to manage message delivery and receipt, using the RH_RF95 drive
RHReliableDatagram base(driver, SERVER_ADDRESS);


//// END SPI Instances ///////////////////////////////////////////////



// Interrupt Service Routine for GPS timepulse
void toggle(){
    // set the flag to one so the controller knows to read from usb serial
    rtcm_flag = 1;  
}

// send finish to laptop for processing  
void handle_competitor_finish(uint8_t len){
  Serial.write(buf, len);
  
  }

//funciton to stream serial form the 
void stream_and_send_rtcm(){
    // set the number of received messages to 0
    num_messages = 0;
    // reset the flag in preparation for the next time pulse
    rtcm_flag = 0;  

    // message have not yet arrived, usually due to latency from GPS -> Computer -> MCU via USB
    // Exit Function and try again
    if(!Serial.available()){
      return;
      }
  
    // There is data available
    // Read the first two bytes to get the data size
    Serial.readBytes(payload_size, 2);   
    //convert two byte uint8_t data to 32bit integer
    data_size = (int)payload_size[0]*256 + (int)payload_size[1];

    
    // some debgging messages which can be read from FTDI serial converter  
    Serial1.print("Data to Read: ");
    Serial1.println(data_size);

    // integer for debugging number of received bytes
    int count = 0;       
    count = Serial.readBytes(rx_data, data_size);

    //clear buffer in any noisy data has arrived
    while(Serial.available()){
      Serial.read();
      }
   
    // Need to find out how many messages exist in the payload.
    // The start of each message is marked by a marker byte, for easy collection
    // The markers appear at the front of the payload.
    // Search until the RTCM preamble (0xD3) is found, all bytes before the preamble will be a marker
    // Number of messages is the number of markers + 1, since the start of the first message starts at
    // 0 and does not need to be tracked.
    while(rx_data[num_messages] != 0xD3){
      // add the marker to a dedicated array for handling the individual messages
      markers[num_messages] = rx_data[num_messages];
      // increase the number of messages
      num_messages++;
    }
    
    // Iterate for the nuber of available messages
    // In theory, the SPI radio should receive at minimum, 3 messages per one second cycle
    // The conditionals below handle all cases from 1 message to 4
    // <= rather than < allows for the first message which does not have a marker to be accounted
    // for.
    for(int i = 0; i <= num_messages; i++){
      // If the current message is the finsl message in the stream then the end marker is simply the 
      // size of the data
      if(i == num_messages){
          if(i==0){
            for(int j = 0; j<data_size;j++){
              // pull message from full rxbuffer and place in relevant message array
              message_1[j] = rx_data[j+num_messages];
            }
            // Find the size to be sent
            size_to_send = data_size + 1;
            // Send over SPI
            base.sendto((message_1), size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            break;
          }
          else if(i==1){
            for(int j = markers[0]; j<data_size; j++){
              message_2[j-markers[0]] = rx_data[j+num_messages];
          }
            size_to_send = (data_size + 1) - markers[0];
            base.sendto(message_2, size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            break;
          }
          else if(i==2){
            for(int j = markers[1]; j<data_size;j++){
              message_3[j-markers[1]] = rx_data[j+num_messages];
          }
           
            size_to_send = (data_size + 1) - markers[1];
            base.sendto(message_3,(data_size+1)-markers[1], RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            break;
          }
          else if(i==3){
            for(int j = markers[2]; j<data_size;j++){
              message_4[j-markers[2]] = rx_data[j+num_messages];
          }
         
            size_to_send = (data_size + 1) - markers[2];
            base.sendto(message_4,size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            break;
          }
        }
      // the current message is not the final message, need to use the markers to collect the 
      // correct amount of data  
      else{
        if(i==0){
            for(int j = 0; j<markers[0];j++){
              message_1[j] = rx_data[j+num_messages];
            }
            size_to_send = markers[0];
            base.sendto(message_1, size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            continue;
          }
          else if(i==1){
            for(int k = markers[0]; k<markers[1];k++){
              message_2[k-markers[0]] = rx_data[k+num_messages];
          }
            size_to_send =  markers[1]-markers[0];
            base.sendto(message_2, size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            continue;
          }
          else if(i==2){
            for(int j = markers[1]; j<markers[2];j++){
              message_3[j-markers[1]] = rx_data[j+num_messages];
          }
            sent_sizes[i] = data_size-markers[1];
            base.sendto(message_3, markers[2]-markers[1], RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            continue;
          }
          else if(i==3){
            for(int j = markers[2]; j<data_size;j++){
              message_4[j-markers[2]] = rx_data[j+num_messages];
          }
            size_to_send = (data_size+1)-markers[2];           
            base.sendto(message_4, size_to_send, RH_BROADCAST_ADDRESS);
            Serial1.println("Sent");
            continue;
          }
      }
    }

    Serial1.println("RTCM Collection Complete: ");
    Serial1.println(num_messages); 
    markers[0] = 0;
    markers[1] = 0;
    markers[2] = 0;
    marker = 0;
    num_messages = 0;
  }

void setup() 
{
  // Define timemode pin as an input
  pinMode(external_interrupt, INPUT);
  //initiate ISR on rising edge of pin
  attachInterrupt(digitalPinToInterrupt(external_interrupt), toggle, RISING);
 
  // Open USB Serial Port (Only need USB on Base)
  Serial.begin(115200);
  // FTDI Debugging only
  Serial1.begin(19200);
  // Wait for serial port to be available
  while (!Serial) ; 

  //Initialise manager class and hence the radio with default settings
 
  ////////////////// Defaults //////////////////
  /// Frequency 434MHz                       ///
  /// Tx Power: 13dBm                        ///
  /// Bandwidth: 125KHz                      ///
  /// Coding Rate: 4/5                       ///
  /// Spreading Factor: 128 chips/ Symbol    ///
  /// CRC On                                 ///
  //////////////////////////////////////////////


  // Note HOPERF RFM96 module uses a PA_BOOST transmitter pin 
  // Power Range: 5 to 23 dBm:
  // Example base.setTxPower(23, false);
  if (!base.init())
    Serial1.println("init failed");
  else
    Serial1.println("init succesful");

}


void send_status_byte(){
   // bitwise operations here (Future Work)
   //memcpy(status_message, status_byte)
   memcpy(status_message+2, pin, 8*sizeof(uint8_t));
   
   base.sendto(pin, 8, RH_BROADCAST_ADDRESS);
   
}

void loop() {
   //timepulse has cause ISR, need to send RTCM corrections    
   if(rtcm_flag == 1){
        // debugging to UART
        Serial1.println("RTCM Interrupt");
        stream_and_send_rtcm();
        send_status_byte();
        //send_status_packet();
        rtcm_flag = 0;
      }
    else{
        uint8_t len = sizeof(buf);
        // Address from which the message originated
        uint8_t from; 
        if(base.recvfromAck(buf, &len, &from)){
            // recieved a finish time, need to handle it
            // Acknowledge who its from, hold results
            if(from == 2){
                Serial1.write("Pin Updated");
                memcpy(pin, buf, 8*sizeof(uint8_t));
              }
            else{
                handle_competitor_finish(len);
              }
            // debug message 
            Serial1.write(buf, len);
          }
      
      }
}
