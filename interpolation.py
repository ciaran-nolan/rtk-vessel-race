from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev, interp1d, UnivariateSpline

##linear interpolation
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
        u = numerator/denominator
        print(u)
        print("Linear intercept", u*s[0]+boat1[0], u*s[0]+boat1[1])

    return u

##nonlinear interpolation
def nonlinear_interpolation_b_spline(base, boat1, boat2, boat3, boat4):

    x_pts = [boat1[0], boat2[0], boat3[0], boat4[0]]
    y_pts = [boat1[1], boat2[1], boat3[1], boat4[1]]

    tck, u = splprep([x_pts, y_pts], u=None, s=0.0, per=0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)

    N=1000
    x = np.linspace(0, base[0], N)
    y = np.linspace(0, base[1], N)

    x_intersect,y_intersect = intersection(x_new, y_new, x, y)
    print("Non-linear Intercept: ", x_intersect[0], y_intersect[0])


    fig, ax = plt.subplots()
    ax.plot(x_pts, y_pts, 'ro')
    ax.plot(x_new, y_new, 'r-')
    ax.plot([0,base[0]], [0,base[1]], marker='o')
    ax.plot(x_intersect, y_intersect, "*k")
    plt.show()

    return
def nonlinear_interpolation_univariate_spline(base, boat1, boat2, boat3, boat4):
    x_pts = [boat1[0], boat2[0], boat3[0], boat4[0]]
    y_pts = [boat1[1], boat2[1], boat3[1], boat4[1]]



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