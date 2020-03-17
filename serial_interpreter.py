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
    ser.port = "COM12"
    ser.baudrate = 19200
    ser.open()
    return ser


def equation_calculation(base_ned, boat_ned):
    m = base_ned[1] / base_ned[0]

    if boat_ned[1] > boat_ned[0] * m:
        return False
    return True


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
def boat_tracker(base, boat, s):

    crossed_line = False
    above_below_previous = None

    s.flush()

    while not crossed_line:
        checknum = ubx_messages.check_bytes(s)
        while checknum != 1:
            checknum = ubx_messages.check_bytes(s)
        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        print(current_boat_ned)
        current_above_below = finish_detection.has_crossed_slope(base, current_boat_ned)
        if above_below_previous is None:
            above_below_previous = current_above_below
        elif above_below_previous != current_above_below:
            print("Boat has crossed the line")
            crossed_line = True
        current_boat_ned.append(current_above_below)
        boat.update_position_history(current_boat_ned)

    #
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
    interpolation.nonlinear_interpolation_shortest_distance(base, boat.boat_history)
    interpolation.linear_interpolation_shortest_distance(base, boat.boat_history, False)
    plt.show()

    return

def stream_serial():

    s = createserialcommunication()
    data_sizes = []
    temp = 0
    for x in range(100):

        line1 = BitArray(s.read(1))
        print(line1, temp)
        line2 = BitArray(s.read(2))
        data_size = int(line2.bin[6:], 2)
        data_sizes.append(data_size)
        print(data_size)
        s.read(data_size+3)
        temp = line1


    print(data_sizes)

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
