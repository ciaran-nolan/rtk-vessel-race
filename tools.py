import numpy as np
import math


def separate_x_y_coords(coordinate_list):
    x = [i[0] for i in coordinate_list]
    y = [i[1] for i in coordinate_list]
    return x, y


def shortest_distance(distance_data):
    distance = [i[0] for i in distance_data]
    timestamp = [i[1] for i in distance_data]
    return distance, timestamp


def perpendicular_distance(base_ned, boat_ned):
    perpdist = abs((base_ned[1] * boat_ned[0] - base_ned[0] * boat_ned[1])) / (
        math.sqrt(base_ned[0] ** 2 + base_ned[1] ** 2))
    print("Perpendicular distance is: ", perpdist)
    return perpdist
