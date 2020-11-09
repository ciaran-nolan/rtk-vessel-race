# Python Script for accepting bulk RTCM and creating an organized message for
# Adafruit Feather M0 to handle all messages at once
# Process:
# 1: Accept RTCM Messages at the beginning of each one second transmission cycle
# 2: Extract the payload size of each message
# 3: Add an array of markers at the beginning of the full RTCM message,
# to indicate where each RTCM message starts and ends, reducing the
# necessity for bitwise operation at the MCU
# 4: Include 2 bytes representing the total size of the message to allow
# all data to be read into memory without risk of overwrites
# 5: Transmit organized packet over Feather M0 USB virtual COM port

import serial
from bitstring import BitArray

# function to open a com port.
# NOTE: Ensure COM Port number is correct before running (Varies from computer)
def createserialcommunication(com_port, baud):
    ser = serial.Serial()  # open serial port
    ser.port = com_port
    ser.baudrate = baud
    ser.open()
    ser.inter_byte_timeout = 0.1
    return ser


# Function to extract the index where each message starts and ends
def extract_indexes(data_string):

    # count the number of messages
    marker_count = 0
    # placeholder to hold the current marker position. Starts at first message (0)
    marker = 0
    # byte array to hold hex value representing marker position
    marker_bytes = b''
    # extract the data size of the first message using bitwise operation
    data_size = int(BitArray(data_string[marker+1:marker+3]).bin[6:], 2)

    # increment the new marker position. Note the increment of 4 is to account for
    # 3 bytes of CRC and to move the marker to the next preamble (if it exists):
    # the increment of two is to account for the reserved and data size bits
    marker = marker + 2 + data_size + 4
    # If only one message arrives, exit
    if marker >= len(data_string):
        return marker_bytes, 0

    else:
        # 211 represents 0xD3 in binary, the preamble for each RTCM message
        while data_string[marker] == 211:
            # a preamble has been found.

            # convert the position of the marker into a hex value
            marker_bytes += marker.to_bytes(1, 'big')
            # increment the byte counter
            marker_count += 1
            # extract the data size of the proceeding message
            data_size = int(BitArray(data_string[marker + 1:marker + 3]).bin[6:], 2)
            # increment the marker position to the start of the new message (if exists)
            marker = marker + 2 + data_size + 4
            # marker now exceeds the size of the string, no more messages, break from the loop
            if marker >= len(data_string):
                break
        # return the byte array representing each of the markers, as well as the number of marker
        return marker_bytes, marker_count


def stream_rtcm():
    # open serial ports for GNSS receivers and Feather M0
    s_in = createserialcommunication("COM24", 115200)
    s_out = createserialcommunication("COM21", 115200)

    while True:
        # read in the max amount of RTCM data possible, timeout after 1ms if no further bytes appear
        data_buffer = s_in.read(4120)

        # find the length of the entire message
        payload_length_int = len(data_buffer)

        # if no data read, wait until available data
        while len(data_buffer) == 0:
            data_buffer = s_in.read(4120)

        # use the extract function to generate markers
        markers, markers_int = extract_indexes(data_buffer)

        # increase the payload length by the number of markers to be added, so Feather M0
        # is aware of the amount of data to read
        payload_length_int += len(markers)
        # convert payload length to two hex bytes
        payload_length = payload_length_int.to_bytes(2, 'big')

        # generate byte array for overhead (payload length and markers)
        overhead = payload_length + markers

        # add overhead to data buffer
        payload = overhead + data_buffer
        # Write organized message to Feather via USB
        s_out.write(payload)

if __name__ == "__main__":
    stream_rtcm()
