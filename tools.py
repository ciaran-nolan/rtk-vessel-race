import numpy as np


def separate_x_y_coords(coordinate_list):
    x = [int(i[0]) for i in coordinate_list]
    y = [int(i[1]) for i in coordinate_list]
    print(x, y)
