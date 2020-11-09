from random import randint
import numpy as np
import math

# this file combines functions, which when placed together represent a boats
# approach to a hypothetical finish line

# note the functions were derived visually, using geogebra, hence the use of
# floating points with several trailing decimals

# These functions simply create thousands of data points in a linear space,
# separated by an integer number of millisecond timestamps

def generate_45_degree_turn():
    #define base, history list and timestamps
    base = [8000, 6000]
    boat_history = []
    timestamp1 = randint(100000, 600000)

    # loop to generate 45 degree approach timestamps
    for i in range(3001):
        if i == 0:
            boat_history.append([2000, 0, 0])
            boat_history[0][2] = timestamp1
        else:
            boat_history.append([2000, i, (boat_history[i - 1][2] + 2)])

    # extract data at one second intervals for interpolation
    extracted_data = extract_test_data(timestamp1, boat_history)
    return base, boat_history, extracted_data


def generate_slow_turn():
    base = [8000, 6000]
    # range of x values to define function
    x = np.linspace(2000, 5000, 3000)
    # function to approximate a wide turn of a vessel
    y = 0.001 * x ** 2 - 10000
    # list to hold simulation data
    boat_history = []
    # initial timestamp
    timestamp1 = randint(100000, 600000)

    # loop to generate timestamps for data
    for i in range(len(x)):
        if i == 0:
            boat_history.append([x[i], y[i], timestamp1])
        else:
            boat_history.append([x[i], y[i], (boat_history[i - 1][2] + 2)])

    # extract data at one second intervals for interpolation
    extracted_data = extract_test_data(timestamp1, boat_history)

    return base, boat_history, extracted_data


def generate_tight_tack():
    base = [8000, 6000]
    x1 = np.linspace(2000, 3400, 1400)
    x2 = np.flip(np.linspace(3000, 3399, 399))

    x = np.concatenate((x1, x2), axis=0)

    y1 = 0.001 * x1 ** 2 - 10000
    y2 = (0.1 * x2 - 390.596412) ** 2 - 1000

    y = np.concatenate((y1, y2), axis=0)

    boat_history = []
    timestamp1 = randint(100000, 600000)

    for i in range(len(x)):
        if i == 0:
            boat_history.append([x[i], y[i], timestamp1])
        else:
            boat_history.append([x[i], y[i], (boat_history[i - 1][2] + 2)])

    extracted_data = extract_test_data(timestamp1, boat_history)

    return base, boat_history, extracted_data


def upwind_tacks():

    base = [8000, 6000]
    x1 = np.linspace(4000, 4500, 1000)
    x2 = np.linspace(4501, 5000, 998)
    x3 = np.flip(np.linspace(4500, 4999, 998))
    x4 = np.linspace(4501, 5000, 998)
    x5 = np.flip(np.linspace(4500, 4999, 998))

    x = np.concatenate((x1, x2, x3, x4, x5), axis=0)

    y1 = (0.1 * x1 - 400) ** 2
    y2 = x2 - 2000
    y3 = 3000 + 0 * x3
    y4 = x4 - 1500
    y5 = -1 * x5 + 8500

    y = np.concatenate((y1, y2, y3, y4, y5), axis=0)

    boat_history = []
    timestamp1 = randint(100000, 600000)

    for i in range(len(x)):
        if i == 0:
            boat_history.append([x[i], y[i], timestamp1])
        else:
            boat_history.append([x[i], y[i], (boat_history[i - 1][2] + 2)])

    extracted_data = extract_test_data(timestamp1, boat_history)

    return base, boat_history, extracted_data

#function to simulate a boat varying speeds across a finish line
def variable_speeds():
    base = [8000, 6000]
    distance_tolerance = 1e-9
    #declare functions and spaces

    x1 = np.linspace(2000, 10000, 50000)
    x1 = np.flip(x1)
    y1 = ((0.01 * x1 - 100) ** 2) - 10000

    initial_velocity1 = 0.1
    final_velocity = 6
    timestamp1 = 100000
    velocity_increment1 = (.1 / 1000)
    chosen1, chosen1_x, chosen1_y = variable_speed_selector(initial_velocity1, final_velocity, x1, y1, distance_tolerance, velocity_increment1, timestamp1)


    x2 = np.linspace(2000, 9000, 7000)
    y2 = ((0.01 * x2 - 8) ** 2) - 3744
    initial_velocity2 = 0.1
    final_velocity2 = 8
    velocity_increment2 = (4 / 7000)
    timestamp2 = chosen1[len(chosen1)-1][2] + 1
    chosen2, chosen2_x, chosen2_y = variable_speed_selector(initial_velocity2, final_velocity2, x2, y2,
                                                            distance_tolerance, velocity_increment2, timestamp2)


    x3 = np.linspace(5990, 9000, 12000)
    x3 = np.flip(x3)
    y3 = ((0.01 * x3 - 100) ** 2) + 2880
    initial_velocity3 = 0.1
    final_velocity3 = 10
    velocity_increment3 = (4 / 12000)
    timestamp3 = chosen2[len(chosen2)-1][2] + 1
    chosen3, chosen3_x, chosen3_y = variable_speed_selector(initial_velocity3, final_velocity3, x3, y3,
                                                            distance_tolerance, velocity_increment3, timestamp3)



    x4 = np.linspace(5990, 9000, 6000)
    y4 = ((0.02 * x4 - 63.75) ** 2) + 1346.5
    initial_velocity4 = 0.1
    final_velocity4 = 0.9
    velocity_increment4 = (0.4 / 6000)
    timestamp4 = chosen3[len(chosen3)-1][2] + 1
    chosen4, chosen4_x, chosen4_y = variable_speed_selector(initial_velocity4, final_velocity4, x4, y4,
                                                            distance_tolerance, velocity_increment4, timestamp4)

    chosen = chosen1 + chosen2 + chosen3 + chosen4
    extracted_data = extract_test_data(timestamp1, chosen)

    return base, chosen, extracted_data

def variable_speed_straight_line():
    base = [8000, 6000]
    distance_tolerance = 1e-9


    x1 = np.linspace(0, 3000, 50000)

    y1 = (6/8)*x1 - 100

    initial_velocity1 = 0.1
    final_velocity = 6
    timestamp1 = 100000
    velocity_increment1 = (1 / 2000)
    chosen1, chosen1_x, chosen1_y = variable_speed_selector(initial_velocity1, final_velocity, x1, y1,
                                                            distance_tolerance, velocity_increment1, timestamp1)

    x2 = np.linspace(-10000, 3000, 30000)
    x2 = np.flip(x2)
    y2 = -x2 + 5150
    initial_velocity2 = 0.1
    final_velocity2 = 5
    velocity_increment2 = (0.1 / 1000)
    timestamp2 = chosen1[len(chosen1) - 1][2] + 1
    chosen2, chosen2_x, chosen2_y = variable_speed_selector(initial_velocity2, final_velocity2, x2, y2,
                                                            distance_tolerance, velocity_increment2, timestamp2)

    chosen = chosen1 + chosen2
    extracted_data = extract_test_data(timestamp1, chosen)

    return base, chosen, extracted_data

def variable_speed_single_quadratic():
    base = [8000, 6000]
    distance_tolerance = 1e-9
    x1 = np.linspace(0, 3000, 50000)
    y1 = 0.001*x1**2 - 1000

    initial_velocity1 = 0.01
    final_velocity = 8
    timestamp1 = 100000
    velocity_increment1 = (0.4 / 2000)
    chosen1, chosen1_x, chosen1_y = variable_speed_selector(initial_velocity1, final_velocity, x1, y1,
                                                            distance_tolerance, velocity_increment1, timestamp1)
    chosen = chosen1
    extracted_data = extract_test_data(timestamp1, chosen)

    return base, chosen, extracted_data

# function to pick points that accurately represent an increase in velocity. The velocity calculations
# are based on the fact that all points are spaced evenly with respect to time. finding the distance and time
# between two points allows for a speed to be found. Point separation is then chosen such that that speed is
# matched
def variable_speed_selector(initial_velocity, maximum_velocity, x, y, tolerance, velocity_increment, timestamp):
    # set the desired initial velocity
    current_velocity = initial_velocity
    current_position = 0
    chosen_x = [x[0]]
    chosen_y = [y[0]]
    chosen = [[x[0], y[0], timestamp]]
    current_timestamp = timestamp + 1

    # loop until max velocity or end of boat data
    while current_velocity <= maximum_velocity and current_position != len(x) - 1:
        if current_velocity >= maximum_velocity:
            current_velocity = maximum_velocity

        if current_position == len(x) - 1:
            break
        for k in range((current_position + 1), len(y)):
            linear_dist = math.hypot(x[current_position] - x[k], y[current_position] - y[k])
            #distance between two selected points does not represent desured velocity, increment k
            if linear_dist <= current_velocity:
                # check if k has reached end of data
                if k == len(y) - 1:
                    current_position = len(x) - 1
                    break
                continue
            # linear distance sufficiently represents desired velocity
            elif linear_dist >= current_velocity:
                # check if velocity is within the specified tolerance (point could be too far)
                # giving a velocity that is considerably more than desied
                if linear_dist - current_velocity <= tolerance:
                    chosen_x.append(x[k])
                    chosen_y.append(y[k])
                    chosen.append([x[k], y[k], current_timestamp])
                # velocity is outside tolerance, get into tolerance by getting the midpoint between previously
                # selected point and current selected point
                else:
                    chosen_x.append(((x[k] - x[k - 1]) / 2) + x[k - 1])
                    chosen_y.append(((y[k] - y[k - 1]) / 2) + y[k - 1])
                    chosen.append([((x[k] - x[k - 1]) / 2) + x[k - 1], ((y[k] - y[k - 1]) / 2) + y[k - 1],
                                   current_timestamp])
                # increment the time stamp by 1, to represent velocity change over the desired period, rather
                # than the multiple data points
                current_timestamp = current_timestamp + 1
                current_position = k
                current_velocity = current_velocity + velocity_increment
                break
    return chosen, chosen_x, chosen_y

def extract_test_data(timestamp1, boat_data):
    extracted_data = [boat_data[0]]

    for i in range(len(boat_data)):
        if i == 0:
            continue
        # since full data set is in milliseconds, extract data at one second
        # intervals, for a realistic simulation subset
        if (boat_data[i][2] - timestamp1) % 1000 == 0:
            extracted_data.append(boat_data[i])

    return extracted_data

if __name__ == "__main__":
    variable_speeds()
