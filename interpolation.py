import numpy as np
import matplotlib.pyplot as plt

##linear interpolation
x_pts = np.linspace(0, 2*np.pi, 10)
# 10 equidistant x coords from 0 to 10
y_pts = np.sin(x_pts)
x_vals = np.linspace(0, 2*np.pi, 50)
# 50 desired points
y_vals = np.interp(x_vals, x_pts, y_pts)
plt.plot(x_pts, y_pts, 'o') # plot known data points
plt.plot(x_vals, y_vals, '-x') # plot interpolated points
plt.show()





##nonlinear interpolation