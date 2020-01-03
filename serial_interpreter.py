import serial
import numpy as np
import ubx_messages
import struct
import time
import math
from decimal import Decimal
from timeit import default_timer as timer

def createserialcommunication():
    ser = serial.Serial()  # open serial port
    ser.port = "COM9"
    ser.baudrate = 19200
    ser.open()
    # print(ser.name)
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

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = (dx * dx + dy * dy) ** .5
    print(dist)
    return dist


"""
def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)
"""


def angle_between(v1,v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    dot = v1[0] * v2[0] + v1[1] * v2[1]  # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0]  # determinant
    angle = -math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    #print("Angle is", angle * (180 / math.pi))
    return angle


def has_crossed_line_angle(base_ned, ser):
    crossed_line = False

    while not crossed_line:

        check_num = check_bytes(ser)
        while check_num != 1:
            check_num = check_bytes(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        angle = angle_between((base_ned[0], base_ned[1]), (boat_ned[0], boat_ned[1]))
        if angle < 0:
            crossed_line = True
    return


def has_crossed_line_dist(base_ned, ser):
    crossed_line = False

    while not (crossed_line):

        check_num = check_bytes(ser)
        while check_num != 1:
            check_num = check_bytes(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        dist = perpendicular_distance(base_ned, boat_ned)
        if dist < 0:
            crossed_line = True
    return


def has_crossed_line_equation(base_ned, ser):
    crossed_line = False
    m = base_ned[1] / base_ned[0]

    while not (crossed_line):

        checknum = check_bytes(ser)
        while checknum != 1:
            checknum = check_bytes(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        print("boat_y = ", boat_ned[1])
        print("boat_x = ", boat_ned[0] * m)
        if (boat_ned[1] < boat_ned[0] * m):
            crossed_line = True;

    return


def check_bytes(ser):
    ser.flush()
    bytes = []
    bytes.append(ser.read(1))

    if int.from_bytes(bytes[0], "little") == 36:
        nmea_end = False
        i = 1
        while not (nmea_end):
            bytes.append(ser.read(1))
            print(int.from_bytes(bytes[i], "little"))
            if int.from_bytes(bytes[i], "little") == 10:
                nmea_end = True
            else:
                i += 1
        check_bytes(ser)
    else:
        bytes.append(ser.read(1))
        if int.from_bytes(bytes[0], "little") == 181:
            # vector = ubxnavrelposned(ser)
            # print(vector)
            return 1


def perpendicular_distance(base_ned, boat_ned):
    perpdist = abs((base_ned[1] * boat_ned[0] - base_ned[0] * boat_ned[1])) / (
        math.sqrt(base_ned[0] ** 2 + base_ned[1] ** 2))
    print("Perpendicular distance is: ", perpdist)
    return perpdist


def equation_calculation(base_ned, boat_ned):
    m = base_ned[1] / base_ned[0]
   # print("y_component = ", boat_ned[1], "\nx_component*slope = ", boat_ned[0]*m)
    if boat_ned[1] > boat_ned[0]*m:
        return False
    return True


def main():
    s = createserialcommunication()
    checkreturn = check_bytes(s)
    while checkreturn != 1:
        checkreturn = check_bytes(s)

    base_vector = ubx_messages.ubxnavrelposned(s)
    # base_vector = [-1684.44, -2476.23, 37.8]
    print(base_vector)
    input("Press any key to begin")
    # base_vector = ubxnavrelposned(s)
    has_crossed_line_angle(base_vector, s)
    print("Receiver has crossed line")

    return 0


def simulation():
    base_ned = [100, -100, 0]
    boat_ned = [50, -50 ,0]

    angle_between(base_ned, boat_ned)
    perpendicular_distance(base_ned, boat_ned)

    equation_calculation(base_ned, boat_ned)

    #start = timer()
    #end = timer()
    #print(end-start)
    #has_crossed_line_equation(boat_ned,ser)

# dist_line_segment(base_ned, boat_ned)

if __name__ == "__main__":
    simulation()
