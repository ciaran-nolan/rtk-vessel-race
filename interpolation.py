from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev, interp1d, UnivariateSpline
import tools
##linear interpolation
import distance
from intersection import intersection


def linear_interpolation_positional(base, boat1, boat2, boat3, boat4):
    if np.isnan(boat3) or np.isnan(boat4):
        fig, ax = plt.subplots()
        ax.plot([boat1[0], boat2[0]], [boat1[1], boat2[1]], marker='o')
        ax.plot([0, base[0]], [0, base[1]])

    else:
        fig, ax = plt.subplots()
        ax.plot([boat1[0], boat2[0], boat3[0], boat4[0]], [boat1[1], boat2[1], boat3[1], boat4[1]], marker='o')
        ax.plot([0, base[0]], [0, base[1]])

    q = boat1
    s = np.subtract(boat2, boat1)
    print(s)

    r = base
    numerator = np.cross(q, r)
    denominator = np.cross(r, s)

    if denominator != 0:
        u = numerator / denominator
        print(u)
        print("Linear intercept", u * s[0] + boat1[0], u * s[0] + boat1[1])

    return u


##nonlinear interpolation
## Note: Two Identical points will return an error from splprep
##TODO funciton to remove duplicate points

def nonlinear_interpolation_b_spline(base, boat_history):

    x_pts, y_pts = tools.separate_x_y_coords(boat_history)
    tck, u = splprep([x_pts, y_pts], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)

    N = 1000
    x = np.linspace(0, base[0], N)
    y = np.linspace(0, base[1], N)

    x_intersect, y_intersect = intersection(x_new, y_new, x, y)
    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])

    fig, ax = plt.subplots()
    ax.plot(x_pts, y_pts, 'ro')
    ax.plot(x_new, y_new, 'r-')
    ax.plot([0, base[0]], [0, base[1]], marker='o')
    ax.plot(x_intersect, y_intersect, "*k")
    plt.show()

    return


def linear_interpolation_shortest_distance(base, boat_data):



    dis = list(map(distance.pnt2line, boat_data))
    shortest_distance_data, timestamp = tools.shortest_distance(dis)
    plt.plot(timestamp, shortest_distance_data)
    plt.show()


    print(shortest_distance_data)


def nonlinear_interpolation_shortest_distance(base, boat_history):
    dis = list(map(distance.pnt2line, boat_history))
    shortest_distance_data, timestamp = tools.shortest_distance(dis)
    tck, u = splprep([timestamp, shortest_distance_data], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    time_new, short_new = splev(u_new, tck, der=0)

    fig, ax = plt.subplots()
    ax.plot(timestamp, shortest_distance_data, 'ro')
    ax.plot(time_new, short_new, 'r-')


    plt.show()

    return

def intersect_test():
    a, b = 1, 2
    phi = np.linspace(3, 10, 100)
    x1 = a * phi - b * np.sin(phi)
    y1 = a - b * np.cos(phi)

    x2 = phi
    y2 = np.sin(phi) + 2
    x, y = intersection(x1, y1, x2, y2)

    plt.plot(x1, y1, c="r")
    plt.plot(x2, y2, c="g")
    plt.plot(x, y, "*k")
    plt.show()
