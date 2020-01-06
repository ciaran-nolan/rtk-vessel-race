from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev, interp1d

##linear interpolation
def linear_interpolation(base, boat1, boat2):


    fig, ax = plt.subplots()
    ax.plot([boat1[0], boat2[0]], [boat1[1], boat2[1]], marker = 'o')
    ax.plot([0, base[0]], [0, base[1]])

    q = boat1
    s = np.subtract(boat2, boat1)
    print(s)

    r = base
    numerator = np.cross(q, r)
    denominator = np.cross(r, s)

    if denominator != 0:
        u = numerator/denominator
        print(u)

    return u

##nonlinear interpolation
def nonlinear_interpolation(base, boat1, boat2, boat3, boat4):

    x_pts = [boat1[0], boat2[0], boat3[0], boat4[0]]
    y_pts = [boat1[1], boat2[1], boat3[1], boat4[1]]

    print(x_pts, y_pts)
    tck, u = splprep([x_pts,y_pts], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)

    fig, ax = plt.subplots()
    ax.plot(x_pts, y_pts, 'ro')
    ax.plot(x_new,y_new, 'r-')
    ax.plot([0,base[0]],[0,base[1]])

    plt.show()

    return