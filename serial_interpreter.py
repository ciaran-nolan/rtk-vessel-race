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


def shortest_distance_to_finish_line(base, boat):
    num_u = (boat[0] * base[0]) + (boat[1] * base[1])
    den_u = boat[0] ** 2 + boat[1] ** 2

    u = num_u / den_u

    print(u)
    if 0 <= u <= 1:
        dist_num = abs((base[0] * -boat[1]) - (base[1] * -boat[0]))
        dist_den = math.sqrt(base[0] ** 2 + base[1] ** 2)
        dist = dist_num / dist_den
        print("Perpendicular: ", dist)
        return dist
    else:
        dist_to_committee = math.sqrt(boat[0] ** 2 + boat[1] ** 2)
        dist_to_pin = math.sqrt((base[0] - boat[0]) ** 2 + (base[1] - boat[1]) ** 2)
        if dist_to_committee < dist_to_pin:
            print("Committee Boat: ", dist_to_committee)
            return dist_to_committee
        else:
            print("Pin End: ", dist_to_pin)
            return dist_to_pin


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
    base_ned = [100, 100]
    boat_ned = [101, 101]
    boat_ned_crossed = [55, -0.05]
    # s = createserialcommunication()

    # sample_data = read_sample_relposned(s)
    # print(sample_data)

    boat_ned_1 = [5, 10]
    boat_ned_2 = [30, 5]
    boat_ned_3 = [55, -0.05]
    boat_ned_4 = [50, -10]

    shortest_distance_to_finish_line(base_ned, boat_ned)
    perpendicular_distance(base_ned, boat_ned)

    # interpolation.intersect_test()
    # finish_detection.has_crossed_slope(base_ned, boat_ned)
    # interpolation.linear_interpolation_positional(base_ned, boat_ned_1, boat_ned_2, np.nan, np.nan)
    # interpolation.linear_interpolation(base_ned, boat_ned, boat_ned_crossed)
    # interpolation.nonlinear_interpolation_univariate_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    # interpolation.nonlinear_interpolation_b_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    # interpolation.nonlinear_interpolation(base_ned, sample_data[0], sample_data[1], sample_data[2], sample_data[3])

    # angle_between(base_ned, boat_ned)
    # perpendicular_distance(base_ned, boat_ned)
    # equation_calculation(base_ned, boat_ned)
    # has_crossed_line_equation(boat_ned,ser)


# dist_line_segment(base_ned, boat_ned)

if __name__ == "__main__":
    simulation()
