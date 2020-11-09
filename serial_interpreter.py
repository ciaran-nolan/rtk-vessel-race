import serial
import ubx_messages
import finish_detection
import classes
import interpolation
import matplotlib.pyplot as plt
from bitstring import BitArray


# open serial communication
def createserialcommunication():
    ser = serial.Serial()  # open serial port
    ser.port = "COM19"
    ser.baudrate = 19200
    ser.open()
    return ser

# read a set of 4 sample relative position messages for observation
def read_sample_relposned(ser):
    ubx_messages.isrelposned(ser)
    a = ubx_messages.ubxnavrelposned(ser)

    ubx_messages.isrelposned(ser)
    b = ubx_messages.ubxnavrelposned(ser)

    ubx_messages.isrelposned(ser)
    c = ubx_messages.ubxnavrelposned(ser)

    ubx_messages.isrelposned(ser)
    d = ubx_messages.ubxnavrelposned(ser)

    return [a, b, c, d]

# function to maintain a log of a given boat
# tracks a boat across a line and informs Python terminal of:
# Finish, and Interpolated Finish Time
def boat_tracker(base, boat, s):

    crossed_line = False
    above_below_previous = None

    s.flush()

    while not crossed_line:
        # ensure incoming data is UBX
        checknum = ubx_messages.check_bytes(s)
        while checknum != 1:
            checknum = ubx_messages.check_bytes(s)
        # extract the boat's relative position message
        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        print(current_boat_ned)
        # check if the boat is above or below the finish line
        current_above_below = finish_detection.has_crossed_slope(base, current_boat_ned)

        if above_below_previous is None:
            above_below_previous = current_above_below
        # check if the previous above below line detection is different to current
        # this covers both finish line orientations
        elif above_below_previous != current_above_below:
            print("Boat has crossed the line")
            crossed_line = True
        current_boat_ned.append(current_above_below)
        boat.update_position_history(current_boat_ned)

    # range 9 a further 10 data points collected after line crossing
    for position in range(9):
        checknum = ubx_messages.check_bytes(s)
        while checknum != 1:
            checknum = ubx_messages.check_bytes(s)
        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        print(current_boat_ned)
        current_above_below = finish_detection.has_crossed_slope(base, current_boat_ned)
        current_boat_ned.append(current_above_below)
        boat.update_position_history(current_boat_ned)

    print(boat.boat_history)
    # calculate linear and non-linear interpolation
    interpolation.nonlinear_interpolation_shortest_distance(base, boat.boat_history)
    interpolation.linear_interpolation_shortest_distance(base, boat.boat_history, False)
    plt.show()

    return

#function for simply streaming RTCM over serial port for observation
def stream_serial():

    s = createserialcommunication()
    preamble = BitArray(s.read(1))
    bytes = BitArray(s.read(2))
    data_size = int(bytes.bin[6:], 2)
    data_crc = BitArray(s.read(data_size + 3))

    string = str(preamble + bytes + data_crc)
    # write to file for observation
    with open('1087.txt', 'w') as f:
        f.write(string)

    print(data_size)



def main():
    s = createserialcommunication()
    checknum = ubx_messages.check_bytes(s)
    while checknum != 1:
        checknum = ubx_messages.check_bytes(s)

    base_vector = ubx_messages.ubxnavrelposned(s)
    print(base_vector)
    base = classes.base([-325, -300, 32, 207922000])
    print(base.position)

    input("Press any key to begin")
    boat = classes.boat(20, 1, None)
    boat_tracker(base, boat, s)
    # base_vector = ubx_messages.ubxnavrelposned(s)
    #finish_detection.has_crossed_line_angle(base_vector, s)
    boat_tracker(base, boat, s)
    #finish_detection.has_crossed_slope(base, s)
    print("Receiver has crossed line")

    return 0

def check_time():
    while True:
        s = createserialcommunication()
        checknum = ubx_messages.check_bytes(s)
        while checknum != 1:
            checknum = ubx_messages.check_bytes(s)

        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        print(current_boat_ned[3])

if __name__ == "__main__":
    stream_serial()
