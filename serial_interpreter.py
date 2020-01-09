import numpy as np
import serial
import ubx_messages
import math
import finish_detection
import interpolation
import distance


def createserialcommunication():
    ser = serial.Serial()  # open serial port
    ser.port = "COM10"
    ser.baudrate = 19200
    ser.open()
    return ser


def perpendicular_distance(base_ned, boat_ned):
    perpdist = abs((base_ned[1] * boat_ned[0] - base_ned[0] * boat_ned[1])) / (
        math.sqrt(base_ned[0] ** 2 + base_ned[1] ** 2))
    print("Perpendicular distance is: ", perpdist)
    return perpdist


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


def main():
    s = createserialcommunication()
    checknum = ubx_messages.check_bytes(s)
    while checknum != 1:
        checknum = ubx_messages.check_bytes(s)

    base_vector = ubx_messages.ubxnavrelposned(s)
    # base_vector = [-1684.44, -2476.23, 37.8]
    print(base_vector)
    input("Press any key to begin")
    # base_vector = ubx_messages.ubxnavrelposned(s)
    finish_detection.has_crossed_line_angle(base_vector, s)
    print("Receiver has crossed line")

    return 0



if __name__ == "__main__":
    main()
