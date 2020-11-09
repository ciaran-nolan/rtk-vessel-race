from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev, interp1d, UnivariateSpline
import tools
import distance
from intersection import intersection
import finish_detection
# note this script employs external libraries such as:
# scipy, matplotlib and numpy. These must be installed via pip or IDE
# for proper usage


def linear_interpolation_relposned(base, boat_history):
    np.unique(boat_history, axis=0)
    x_pts, y_pts = tools.separate_x_y_coords(boat_history)
    N = 1000
    x = np.linspace(0, base[0], N)
    y = np.linspace(0, base[1], N)
    x_intersect, y_intersect = intersection(x_pts, y_pts, x, y)


# nonlinear interpolation of relative positions
# Only for visualization purposes.
def nonlinear_interpolation_b_spline(base, boat_history):
    # ensure no duplicate points
    np.unique(boat_history, axis=0)

    # separate x and y points for non linear interpolation
    x_pts, y_pts = tools.separate_x_y_coords(boat_history)

    # conduct spline interpolation using scipy package
    tck, u = splprep([x_pts, y_pts], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 10000)
    x_new, y_new = splev(u_new, tck, der=0)

    # points describing finish line for graphical representation
    x = np.linspace(0, base.position[0], 1000)
    y = np.linspace(0, base.position[1], 1000)

    # Find intersection
    x_intersect, y_intersect = intersection(x_new, y_new, x, y)

    # plotting
    fig, ax = plt.subplots()
    ax.plot(x_pts, y_pts, 'ro')
    ax.plot(x_new, y_new, 'r-')
    ax.plot([0, base.position[0]], [0, base.position[1]], marker='o')
    ax.plot(x_intersect, y_intersect, "*k")
    ax.title.set_text('Non-Linear Interpolation of Boat Relative Position')
    ax.set_xlabel('Northern Relative Offset (cm)')
    ax.set_ylabel('Eastern Relative Offset (cm)')

    return


def linear_interpolation_shortest_distance(base, boat_history, full_set):
    np.unique(boat_history, axis=0)
    # lists to hold interpolation requirements
    # distances to line
    distances = []
    # time stamp of generated relative positions
    timestamp = []
    # status of each point (above/below line)
    line_status = []

    crossed_time = []
    crossed_dist = []

    for i in range(len(boat_history)):
        if i == 0:
            distances.append(distance.pnt2line(boat_history[i], base.position)[0])
            line_status.append(finish_detection.has_crossed_slope(base, boat_history[i]))
            timestamp.append(boat_history[i][2])

        else:
            timestamp.append(boat_history[i][2])
            boat_distance = distance.pnt2line(boat_history[i], base.position)[0]
            above_below = finish_detection.has_crossed_slope(base, boat_history[i])

            # line crossing detected
            if above_below != line_status[i - 1]:
                # full set contains thousands of points, and has runtime issues with interpolation plotting
                # as a result, this only plots the one point either side of the finish line
                if full_set:
                    # negate the distance to show a line crossing
                    boat_distance = -1 * boat_distance
                    # add the distance of the point to line after BEFORE crossing
                    crossed_dist.append(distances[i - 1])
                    # add the newly calcated point
                    crossed_dist.append(boat_distance)
                    # add the two relevant timestamps
                    crossed_time.append(timestamp[i - 1])
                    crossed_time.append(boat_history[i][2])
                    break

                # smaller subset of points extracted from full set
                boat_distance = -1 * boat_distance
            # if boat has already crossed the line, check the value of the shortest distance
            # if its < 0 maintain this until a new line crossing is detected
            elif distances[i - 1] < 0:
                boat_distance = -1 * boat_distance

            distances.append(boat_distance)
            line_status.append(above_below)

    #find intercept of interpolated data
    intercept_x = np.linspace(timestamp[0], timestamp[len(timestamp) - 1], len(timestamp))
    intercept_y = [0] * (len(timestamp))

    # plot results depending on whther or not a full set or subset of data is used.
    # Note this was to prevent run time issues
    if (full_set):
        x_intersect, y_intersect = intersection(np.array(crossed_time), np.array(crossed_dist), np.array(intercept_x),
                                                np.array(intercept_y))
        print("Linear Intercept: ", x_intersect[0], y_intersect[0])
        fig, ax = plt.subplots()
        ax.plot(x_intersect, y_intersect, '*k')
        ax.plot(crossed_time, crossed_dist, '-ro')
        ax.plot(intercept_x, intercept_y)
        ax.title.set_text('Linear Interpolation of Shortest Distance to Finish Line')
        ax.set_xlabel('Time of Week (Milliseconds)')
        ax.set_ylabel('Shortest Distance (cm)')

    else:
        x_intersect, y_intersect = intersection(np.array(timestamp), np.array(distances), np.array(intercept_x),
                                                np.array(intercept_y))

        print("Linear Intercept: ", x_intersect[0], y_intersect[0])
        fig, ax = plt.subplots()
        ax.plot(x_intersect, y_intersect, '*k')
        ax.plot(timestamp, distances, '-ro')
        ax.plot(intercept_x, intercept_y)
        ax.title.set_text('Linear Interpolation of Shortest Distance to Finish Line')
        ax.set_xlabel('Time of Week (Milliseconds)')
        ax.set_ylabel('Shortest Distance (cm)')


## Non Linear Interpolation of Data Set Points Using Shortest Distance To Finish Line
def nonlinear_interpolation_shortest_distance(base, boat_history):
    # remove duplicate rows
    np.unique(boat_history, axis=0)
    # unique distance to line
    distances = []
    # time stamp of each relative position message
    timestamp = []
    # shows if each point is above or below the finish line
    line_status = []

    # process the relative position messages into shortest distance for illustration
    for i in range(len(boat_history)):
        if i == 0:
            distances.append(distance.pnt2line(boat_history[i], base.position)[0])
            line_status.append(finish_detection.has_crossed_slope(base, boat_history[i]))
            timestamp.append(boat_history[i][2])
        else:
            timestamp.append(boat_history[i][2])
            boat_distance = distance.pnt2line(boat_history[i], base.position)[0]
            above_below = finish_detection.has_crossed_slope(base, boat_history[i])
            # if line crossing has been detected, negate the distance
            if above_below != line_status[i - 1]:
                boat_distance = -1 * boat_distance
            # if previous value is negative line crossing has already been detected, negate distance
            elif distances[i - 1] < 0:
                boat_distance = -1 * boat_distance

            distances.append(boat_distance)
            line_status.append(above_below)

    # compute interpolation
    tck, u = splprep([timestamp, distances], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    time_new, short_new = splev(u_new, tck, der=0)

    # find intercepts and point of intersection
    intercept_x = np.linspace(timestamp[0], timestamp[len(timestamp) - 1], len(timestamp))
    intercept_y = np.zeros(len(timestamp))
    x_intersect, y_intersect = intersection(time_new, short_new, intercept_x, intercept_y)

    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])
    # plot results
    fig, ax = plt.subplots()
    ax.plot(timestamp, distances, 'ro')
    ax.plot(time_new, short_new, 'r-')
    ax.plot(intercept_x, intercept_y)
    ax.plot(x_intersect, y_intersect, '*k')
    ax.title.set_text('Non-Linear Interpolation of Shortest Distance to Finish Line')
    ax.set_xlabel('Time of Week (Milliseconds)')
    ax.set_ylabel('Shortest Distance (cm)')

    return x_intersect[0], y_intersect[0]


# Non Linear Interpolation of Data Set Points Using Shortest Distance To Finish Line
def nonlinear_interpolation_shortest_distance_real_time(base, boat_history):
    np.unique(boat_history, axis=0)
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
            # boat crossing detected, negate distance
            if boat_history[i][3] != boat_history[i - 1][3]:
                boat_distance = -1 * boat_distance
            # boat crossing previously dete
            elif  boat_history[i - 1][3] < 0:
                boat_distance = -1 * boat_distance

            distances.append(boat_distance)
    # interpolate
    tck, u = splprep([timestamp, distances], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    time_new, short_new = splev(u_new, tck, der=0)

    # find intercept and point of intersection of interpolated values with zero crossing
    intercept_x = np.linspace(timestamp[0], timestamp[len(timestamp) - 1], len(timestamp))
    intercept_y = np.zeros(len(timestamp))
    x_intersect, y_intersect = intersection(time_new, short_new, intercept_x, intercept_y)

    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])
    # plot
    fig, ax = plt.subplots()
    ax.plot(timestamp, distances, 'ro')
    ax.plot(time_new, short_new, 'r-')
    ax.plot(intercept_x, intercept_y)
    ax.plot(x_intersect, y_intersect, '*k')
    ax.title.set_text('Non-Linear Interpolation of Shortest Distance to Finish Line')
    ax.set_xlabel('Time of Week (Milliseconds)')
    ax.set_ylabel('Shortest Distance (cm)')

    return x_intersect[0], y_intersect[0]
