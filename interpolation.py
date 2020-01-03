from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as spicy

##linear interpolation
def linear_interpolation(base, boat1, boat2):
    q = boat1

    s = np.subtract(boat2, boat1)
    print(s)

    r = base
    numerator = np.cross(q, r)
    denominator = np.cross(r, s)

    print numerator
    print denominator
    print("Divide!: ", numerator/denominator)

    if denominator != 0:
        u = numerator/denominator
        print u


    return u

##nonlinear interpolation
def nonlinear_interpolation(base, boat1, boat2,boat3,boat4):

    x_pts = [boat1[0], boat2[0], boat3[0], boat4[0]]
    # 10 equidistant x coords from 0 to 10
    y_pts = [boat1[1], boat2[1], boat3[1], boat4[1]]

    print x_pts, y_pts
    #f = spicy.interp1d(x_pts,y_pts, kind='cubic')
    tck, f = spicy.splprep([x_pts, y_pts], s=0)
    new_points = spicy.splev(f, tck)

    #x_vals = np.linspace(0, 2 * np.pi, 50)
    # 50 desired points
    #y_vals = np.interp(x_vals, x_pts, y_pts)

    fig, ax = plt.subplots()
    ax.plot(x_pts, y_pts, 'ro')
    ax.plot(new_points[0], new_points[1], 'r-')
    plt.show()

    #plt.plot(x_pts, y_pts, 'o')  # plot known data points
    #plt.plot(f)  # plot interpolated points
    #plt.show()
    return