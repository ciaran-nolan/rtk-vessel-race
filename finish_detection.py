import math
import ubx_messages
import serial_interpreter
import simulation 

class Counter:
    def __init__(self, boat_history_limit):
        self.counter = 0
        self.boat_history_limit = boat_history_limit

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    dot = v1[0] * v2[0] + v1[1] * v2[1]  # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0]  # determinant
    angle = -math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    # print("Angle is", angle * (180 / math.pi))
    return angle


def has_crossed_line_angle(base_ned, ser):
    crossed_line = False

    while not crossed_line:
        ubx_messages.isrelposned(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        angle = angle_between((base_ned[0], base_ned[1]), (boat_ned[0], boat_ned[1]))
        if angle < 0:
            crossed_line = True
    return


def has_crossed_line_dist(base_ned, ser):
    crossed_line = False

    while not crossed_line:
        ubx_messages.isrelposned(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        dist = serial_interpreter.perpendicular_distance(base_ned, boat_ned)
        if dist < 0:
            crossed_line = True
    return


def has_crossed_line_equation(base_ned, ser):
    crossed_line = False
    m = base_ned[1] / base_ned[0]

    while not crossed_line:
        ubx_messages.isrelposned(ser)
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        if boat_ned[1] < boat_ned[0] * m:
            crossed_line = True
    return

def has_crossed_slope(base_ned, boat_ned):
    if boat_ned[1]*base_ned[0] > base_ned[1]*boat_ned[0]:
        return 0
    else:
        return 1
