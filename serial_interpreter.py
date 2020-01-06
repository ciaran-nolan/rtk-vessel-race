import numpy as np
import serial
import ubx_messages
import math
import finish_detection
import interpolation

def createserialcommunication():
    ser = serial.Serial()  # open serial port
    ser.port = "COM10"
    ser.baudrate = 19200
    ser.open()
    return ser


# x1,y1,x2,y2 = end points of line segment
# x3,y3 = point to calculate distance to
def dist_line_segment(base_ned, boat_ned):  # x3,y3 is the point

    norm = base_ned[0] * base_ned[0] + base_ned[1] * base_ned[1]
    u = ((boat_ned[0]) * base_ned[0] + (boat_ned[1]) * base_ned[1]) / norm

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = u * base_ned[0]
    y = u * base_ned[1]

    dx = x - boat_ned[0]
    dy = y - boat_ned[1]

    dist = (dx * dx + dy * dy) ** .5
    print(dist)
    return dist


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


def simulation():
    base_ned = [80, 20]
    boat_ned = [999, 999]
    boat_ned_crossed = [55, -0.05]
    #s = createserialcommunication()

    #sample_data = read_sample_relposned(s)
    #print(sample_data)

    boat_ned_1 = [5, 10]
    boat_ned_2 = [30, 5]
    boat_ned_3 = [55, -0.05]
    boat_ned_4 = [50, -10]

    #interpolation.intersect_test()
    finish_detection.has_crossed_slope(base_ned, boat_ned)
    interpolation.linear_interpolation(base_ned, boat_ned_1, boat_ned_2, np.nan, np.nan)
    #interpolation.linear_interpolation(base_ned, boat_ned, boat_ned_crossed)
    #interpolation.nonlinear_interpolation_univariate_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    interpolation.nonlinear_interpolation_b_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    #interpolation.nonlinear_interpolation(base_ned, sample_data[0], sample_data[1], sample_data[2], sample_data[3])

    # angle_between(base_ned, boat_ned)
    # perpendicular_distance(base_ned, boat_ned)
    # equation_calculation(base_ned, boat_ned)
    # has_crossed_line_equation(boat_ned,ser)


# dist_line_segment(base_ned, boat_ned)

if __name__ == "__main__":
    simulation()
