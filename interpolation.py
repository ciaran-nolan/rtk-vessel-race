from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev, interp1d, UnivariateSpline
import tools
import distance
from intersection import intersection
import finish_detection


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


    return


def linear_interpolation_shortest_distance(base, boat_history):
    distances = []
    timestamp = []
    line_status = []
    for i in range(len(boat_history)):
        if i == 0:
            distances.append(distance.pnt2line(boat_history[i])[0])

            line_status.append(finish_detection.has_crossed_slope(base, boat_history[i]))
            timestamp.append(boat_history[i][2])
        else:

            timestamp.append(boat_history[i][2])
            boat_distance = distance.pnt2line(boat_history[i])[0]
            above_below = finish_detection.has_crossed_slope(base, boat_history[i])
            if above_below != line_status[i - 1]:
                boat_distance = -1 * boat_distance
            elif distances[i - 1] < 0:
                boat_distance = -1 * boat_distance
            distances.append(boat_distance)
            line_status.append(above_below)


    intercept_x = np.linspace(timestamp[0],timestamp[len(timestamp)-1], len(timestamp))
    intercept_y = np.zeros(len(timestamp))

    x_intersect, y_intersect = intersection(np.array(timestamp), np.array(distances), intercept_x, intercept_y)

    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])

    fig, ax = plt.subplots()
    ax.plot(timestamp, distances, 'ro')
    ax.plot(intercept_x, intercept_y)
    ax.plot(x_intersect, y_intersect, '*k')
    ax.title.set_text('Non-linear, Shortest')

    plt.plot(timestamp, distances, '-ro')


##Non Linear Interpolation of Data Set Points Using Shortest Distance To Finish Line
def nonlinear_interpolation_shortest_distance(base, boat_history):

    distances = []
    timestamp = []
    line_status = []

    for i in range(len(boat_history)):
        if i == 0:
            distances.append(distance.pnt2line(boat_history[i])[0])

            line_status.append(finish_detection.has_crossed_slope(base, boat_history[i]))
            timestamp.append(boat_history[i][2])
        else:

            timestamp.append(boat_history[i][2])
            boat_distance = distance.pnt2line(boat_history[i])[0]
            above_below = finish_detection.has_crossed_slope(base, boat_history[i])
            if above_below != line_status[i-1]:
                boat_distance = -1*boat_distance
            elif distances[i-1] < 0:
                boat_distance = -1*boat_distance
            distances.append(boat_distance)
            line_status.append(above_below)


    tck, u = splprep([timestamp, distances], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    time_new, short_new = splev(u_new, tck, der=0)

    intercept_x = np.linspace(timestamp[0],timestamp[len(timestamp)-1], len(timestamp))
    intercept_y = np.zeros(len(timestamp))

    x_intersect, y_intersect = intersection(time_new, short_new, intercept_x, intercept_y)

    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])

    fig, ax = plt.subplots()
    ax.plot(timestamp, distances, 'ro')
    ax.plot(time_new, short_new, 'r-')
    ax.plot(intercept_x, intercept_y)
    ax.plot(x_intersect, y_intersect, '*k')
    ax.title.set_text('Non-linear, Shortest')


    return x_intersect[0], y_intersect[0]
