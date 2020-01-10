import serial_interpreter
import distance
import finish_detection
import interpolation
import tools
import numpy as np
import ubx_messages
import relpos_sim_data

base_ned = ubx_messages.FinishPin(8000, 6000)


def simulation():
    #base_ned = ubx_messages.FinishPin(100, 100)
    boat_ned = [104, 106, 110483600]
    boat_ned_crossed = [55, -0.05]
    # s = createserialcommunication()

    counter = finish_detection.Counter(4)

    # sample_data = read_sample_relposned(s)
    # print(sample_data)

    boat_ned_1 = [6000, 0, 110483600]
    boat_ned_2 = [6000, 2000, 110484600]
    boat_ned_3 = [6000, 4000, 110485600]
    boat_ned_4 = [6000, 6000, 110486600]
    boat_ned_5 = []
    base, boat_history = relpos_sim_data.test45_approach()

    #boat_history = [boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4]
    # tools.separate_x_y_coords(boat_history)
    # serial_interpreter.perpendicular_distance(base_ned.relpos, boat_ned)
    # distance.pnt2line(boat_ned)
    interpolation.linear_interpolation_shortest_distance(base_ned.relpos, boat_history)
    # interpolation.intersect_test()
    # finish_detection.has_crossed_slope(base_ned, boat_ned)
    #interpolation.linear_interpolation_positional(base_ned.relpos, boat_history)
    # interpolation.linear_interpolation(base_ned, boat_ned, boat_ned_crossed)
    # interpolation.nonlinear_interpolation_univariate_spline(base_ned, boat_ned_1, boat_ned_2, boat_ned_3, boat_ned_4)
    interpolation.nonlinear_interpolation_b_spline(base_ned.relpos, boat_history)
    #interpolation.nonlinear_interpolation_shortest_distance(base_ned.relpos, boat_history)

    # angle_between(base_ned, boat_ned)
    # perpendicular_distance(base_ned, boat_ned)
    # equation_calculation(base_ned, boat_ned)
    # has_crossed_line_equation(boat_ned,ser)


# dist_line_segment(base_ned, boat_ned)

if __name__ == "__main__":
    simulation()
