import numpy as np


def separate_x_y_coords(coordinate_list):
    x = [i[0] for i in coordinate_list]
    y = [i[1] for i in coordinate_list]
    return x, y

def shortest_distance(distance_data):
    distance = [i[0] for i in distance_data]
    timestamp = [i[1] for i in distance_data]
    return distance, timestamp

