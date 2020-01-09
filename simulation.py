import serial_interpreter
import distance
import finish_detection
import interpolation
import tools
import numpy as np
import ubx_messages
def simulation():
    base_ned = [100, 100]
    boat_ned = [104, 106]
    boat_ned_crossed = [55, -0.05]
    # s = createserialcommunication()

    counter = finish_detection.Counter(4)

    # sample_data = read_sample_relposned(s)
    # print(sample_data)

    boat_ned_1 = [79, 80]
    boat_ned_2 = [79, 79]
    boat_ned_3 = [79, 79]
    boat_ned_4 = [81, 78]
    boat_ned_5 = []

    boat_history = np.array([boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4])
    tools.separate_x_y_coords(boat_history)
    serial_interpreter.perpendicular_distance(base_ned, boat_ned)
    distance.pnt2line(boat_ned, [0, 0], base_ned)
    # interpolation.intersect_test()
    # finish_detection.has_crossed_slope(base_ned, boat_ned)
    # interpolation.linear_interpolation_positional(base_ned, boat_ned_1, boat_ned_2, np.nan, np.nan)
    # interpolation.linear_interpolation(base_ned, boat_ned, boat_ned_crossed)
    # interpolation.nonlinear_interpolation_univariate_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    # interpolation.nonlinear_interpolation_b_spline(base_ned, boat_history, counter.boat_history_limit)
    # interpolation.nonlinear_interpolation(base_ned, sample_data[0], sample_data[1], sample_data[2], sample_data[3])

    # angle_between(base_ned, boat_ned)
    # perpendicular_distance(base_ned, boat_ned)
    # equation_calculation(base_ned, boat_ned)
    # has_crossed_line_equation(boat_ned,ser)


# dist_line_segment(base_ned, boat_ned)

if __name__ == "__main__":
    simulation()
