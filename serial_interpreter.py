import serial
import ubx_messages
import finish_detection
import classes
import interpolation

# open serial communication
def createserialcommunication():
    ser = serial.Serial()  # open serial port
    ser.port = "COM10"
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
    checknum = ubx_messages.check_bytes(s)
    while checknum != 1:
        checknum = ubx_messages.check_bytes(s)

    while not crossed_line:
        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        current_above_below = finish_detection.has_crossed_slope(base.position, current_boat_ned)
        if above_below_previous is None:
            above_below_previous = current_above_below
        elif above_below_previous != current_above_below:
            crossed_line = True
        current_boat_ned.append(current_above_below)
        boat.update_position_history(current_boat_ned)

    #
    for position in range(len(boat.boat_history_limit-2)):
        current_boat_ned = ubx_messages.ubxnavrelposned(s)
        current_above_below = finish_detection.has_crossed_slope(base.position, current_boat_ned)
        current_boat_ned.append(current_above_below)
        boat.update_position_history(current_boat_ned)

    interpolation.nonlinear_interpolation_shortest_distance(base.position, boat.boat_history)

   

def main():
    s = createserialcommunication()
    checknum = ubx_messages.check_bytes(s)
    while checknum != 1:
        checknum = ubx_messages.check_bytes(s)

    base_vector = ubx_messages.ubxnavrelposned(s)
    base = classes.base(base_vector)

    input("Press any key to begin")

    boat = classes.boat(20, 1, None)
    boat_tracker(base, boat, s)
    # base_vector = ubx_messages.ubxnavrelposned(s)
    #finish_detection.has_crossed_line_angle(base_vector, s)
    finish_detection.has_crossed_slope(base, s)
    print("Receiver has crossed line")

    return 0



if __name__ == "__main__":
    main()
