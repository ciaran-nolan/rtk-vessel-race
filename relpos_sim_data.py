## approach line from a 45 degree angle
from random import randint
import numpy as np
import math
import matplotlib.pyplot as plt

def test45_approach():
    base = [8000, 6000]

    boat_data = [[2000, 990, 110483600],  # second 1
                 [2000, 1000, 110483600],
                 [2000, 1010, 110483600],
                 [2000, 1020, 110483600],
                 [2000, 1030, 110483600],
                 [2000, 1040, 110483600],
                 [2000, 1050, 110483600],
                 [2000, 1060, 110483600],
                 [2000, 1070, 110483600],
                 [2000, 1080, 110483600],
                 [2000, 1090, 110483600],
                 [2000, 1100, 110483600],
                 [2000, 1110, 110483600],
                 [2000, 1120, 110483600],
                 [2000, 1140, 110483600],
                 [2000, 1150, 110483600],
                 [2000, 1160, 110483600],
                 [2000, 1170, 110483600],
                 [2000, 1180, 110483600],
                 [2000, 1190, 110483600],
                 [2000, 1200, 110483600],
                 [2000, 1210, 110483600],
                 [2000, 1220, 110483600],
                 [2000, 1230, 110483600],
                 [2000, 1240, 110483600],
                 [2000, 1250, 110483600],
                 [2000, 1260, 110483600],
                 [2000, 1270, 110483600],
                 [2000, 1280, 110483600],
                 [2000, 1290, 110483600],
                 [2000, 1300, 110483600],
                 [2000, 1310, 110483600],
                 [2000, 1320, 110483600],
                 [2000, 1330, 110483600],
                 [2000, 1340, 110483600],
                 [2000, 1350, 110483600],
                 [2000, 1360, 110483600],
                 [2000, 1370, 110483600],
                 [2000, 1380, 110483600],
                 [2000, 1390, 110483600],
                 [2000, 1410, 110483600],
                 [2000, 1420, 110483600],
                 [2000, 1430, 110483600],
                 [2000, 1440, 110483600],
                 [2000, 1450, 110483600],
                 [2000, 1451, 110483600],
                 [2000, 1452, 110483600],
                 [2000, 1453, 110483600],
                 [2000, 1454, 110483600],
                 [2000, 1455, 110483600],
                 [2000, 1456, 110483600],
                 [2000, 1457, 110483600],
                 [2000, 1458, 110483600],
                 [2000, 1459, 110483600],
                 [2000, 1460, 110483600],
                 [2000, 1461, 110483600],
                 [2000, 1462, 110483600],
                 [2000, 1463, 110483600],
                 [2000, 1464, 110483600],
                 [2000, 1465, 110483600],
                 [2000, 1466, 110483600],
                 [2000, 1467, 110483600],
                 [2000, 1468, 110483600],
                 [2000, 1469, 110483600],
                 [2000, 1470, 110483600],
                 [2000, 1471, 110483600],
                 [2000, 1472, 110483600],
                 [2000, 1473, 110483600],
                 [2000, 1474, 110483600],
                 [2000, 1475, 110483600],
                 [2000, 1476, 110483600],
                 [2000, 1477, 110483600],
                 [2000, 1478, 110483600],
                 [2000, 1479, 110483600],
                 [2000, 1480, 110483600],
                 [2000, 1481, 110483600],
                 [2000, 1482, 110483600],
                 [2000, 1483, 110483600],
                 [2000, 1484, 110483600],
                 [2000, 1485, 110483600],
                 [2000, 1486, 110483600],
                 [2000, 1487, 110483600],
                 [2000, 1488, 110483600],
                 [2000, 1489, 110483600],
                 [2000, 1490, 110483600],
                 [2000, 1491, 110483600],
                 [2000, 1492, 110483600],
                 [2000, 1493, 110483600],
                 [2000, 1494, 110483600],
                 [2000, 1495, 110483600],
                 [2000, 1496, 110483600],
                 [2000, 1497, 110483600],
                 [2000, 1498, 110483600],
                 [2000, 1499, 110483600],
                 [2000, 1500, 110483600],
                 [2000, 1501, 110483600],
                 [2000, 1502, 110483600],
                 [2000, 1503, 110483600],
                 [2000, 1504, 110483600],
                 [2000, 1505, 110483600],
                 [2000, 1506, 110483600],
                 [2000, 1507, 110483600],
                 [2000, 1508, 110483600],
                 [2000, 1509, 110483600],
                 [2000, 1510, 110483600],
                 [2000, 1511, 110483600],
                 [2000, 1512, 110483600],
                 [2000, 1513, 110483600],
                 [2000, 1514, 110483600],
                 [2000, 1515, 110483600],
                 [2000, 1516, 110483600],
                 [2000, 1517, 110483600],
                 [2000, 1518, 110483600],
                 [2000, 1519, 110483600],
                 [2000, 1520, 110483600],
                 [2000, 1521, 110483600],
                 [2000, 1522, 110483600],
                 [2000, 1523, 110483600],
                 [2000, 1524, 110483600],
                 [2000, 1525, 110483600],
                 [2000, 1526, 110483600],
                 [2000, 1527, 110483600],
                 [2000, 1528, 110483600],
                 [2000, 1529, 110483600],
                 [2000, 1521, 110483600],
                 [2000, 1522, 110483600],
                 [2000, 1523, 110483600],
                 [2000, 1524, 110483600],
                 [2000, 1525, 110483600],
                 [2000, 1526, 110483600],
                 [2000, 1527, 110483600],
                 [2000, 1528, 110483600],
                 [2000, 1529, 110483600],
                 [2000, 1530, 110483600],
                 [2000, 1531, 110483600],
                 [2000, 1532, 110483600],
                 [2000, 1533, 110483600],
                 [2000, 1534, 110483600],
                 [2000, 1535, 110483600],
                 [2000, 1536, 110483600],
                 [2000, 1537, 110483600],
                 [2000, 1538, 110483600],
                 [2000, 1539, 110483600],
                 [2000, 1540, 110483600],
                 [2000, 1541, 110483600],
                 [2000, 1542, 110483600],
                 [2000, 1543, 110483600],
                 [2000, 1544, 110483600],
                 [2000, 1545, 110483600],
                 [2000, 1546, 110483600],
                 [2000, 1547, 110483600],
                 [2000, 1548, 110483600],
                 [2000, 1549, 110483600],
                 [2000, 1550, 110483600],
                 [2000, 1560, 110483600],
                 [2000, 1570, 110483600],
                 [2000, 1580, 110483600],
                 [2000, 1590, 110483600],
                 [2000, 1600, 110483600],
                 [2000, 1610, 110483600],
                 [2000, 1620, 110483600],
                 [2000, 1630, 110483600],
                 [2000, 1640, 110483600],
                 [2000, 1650, 110483600],
                 [2000, 1660, 110483600],
                 [2000, 1670, 110483600],
                 [2000, 1680, 110483600],
                 [2000, 1690, 110483600],
                 [2000, 1700, 110483600],
                 [2000, 1710, 110483600],
                 [2000, 1720, 110483600],
                 [2000, 1730, 110483600],
                 [2000, 1740, 110483600],
                 [2000, 1750, 110483600],
                 [2000, 1760, 110483600],
                 [2000, 1770, 110483600],
                 [2000, 1780, 110483600],
                 [2000, 1790, 110483600],
                 [2000, 1800, 110483600],
                 [2000, 1810, 110483600],
                 [2000, 1820, 110483600],
                 [2000, 1830, 110483600],
                 [2000, 1840, 110483600],
                 [2000, 1850, 110483600],
                 [2000, 1860, 110483600],
                 [2000, 1870, 110483600],
                 [2000, 1880, 110483600],
                 [2000, 1890, 110483600]]

    timestamp1 = randint(100000, 600000)
    boat_data[0][2] = timestamp1

    for i in range(len(boat_data)):
        if i == 0:
            continue
        elif (boat_data[i][1] - boat_data[i - 1][1]) == 10:
            boat_data[i][2] = boat_data[i - 1][2] + 20
        else:
            boat_data[i][2] = boat_data[i - 1][2] + 2

    print(boat_data)

    return base, boat_data


def generate_data_45():
    base = [8000, 6000]
    boat_history = []
    timestamp1 = randint(100000, 600000)
    boat_history.append([2000, 0, 0])
    boat_history[0][2] = timestamp1
    for i in range(3001):
        if i == 0:
            continue
        boat_history.append([2000, i, (boat_history[i - 1][2] + 2)])

    print(boat_history)
    extracted_data = extract_test_data(timestamp1, boat_history)
    return base, boat_history, extracted_data


def generate_slow_turn():
    base = [8000, 6000]
    x = np.linspace(2000, 5000, 3000)
    y = 0.001 * x ** 2 - 10000
    boat_history = []
    timestamp1 = randint(100000, 600000)

    for i in range(len(x)):
        if i == 0:
            boat_history.append([x[i], y[i], timestamp1])
        else:
            boat_history.append([x[i], y[i], (boat_history[i - 1][2] + 2)])

    print(boat_history)
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


def variable_speeds():
    base = [8000, 6000]
    distance_tolerance = 1e-9
    #declare functions and spaces
    # x0 = np.linspace(7000, 10000, 20000)
    # x0 = np.flip(x0)
    # y0 = ((0.01 * x0 - 100) ** 2) - 10000


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


def variable_speed_selector(initial_velocity, maximum_velocity, x, y, tolerance, velocity_increment, timestamp):
    current_velocity = initial_velocity
    current_position = 0
    chosen_x = [x[0]]
    chosen_y = [y[0]]
    chosen = [[x[0], y[0], timestamp]]
    current_timestamp = timestamp + 1

    while current_velocity <= maximum_velocity and current_position != len(x) - 1:
        if current_velocity >= maximum_velocity:
            current_velocity = maximum_velocity

        if current_position == len(x) - 1:
            break
        for k in range((current_position + 1), len(y)):
            linear_dist = math.hypot(x[current_position] - x[k], y[current_position] - y[k])
            if linear_dist <= current_velocity:
                if k == len(y) - 1:
                    current_position = len(x) - 1
                    break
               # print("here: ", math.hypot(x[current_position] - x[k], y[current_position] - y[k]),  current_velocity, k)
                continue
            elif linear_dist >= current_velocity:
                if linear_dist - current_velocity <= tolerance:
                    chosen_x.append(x[k])
                    chosen_y.append(y[k])
                    chosen.append([x[k], y[k], current_timestamp])

                else:
                    chosen_x.append(((x[k] - x[k - 1]) / 2) + x[k - 1])
                    chosen_y.append(((y[k] - y[k - 1]) / 2) + y[k - 1])
                    chosen.append([((x[k] - x[k - 1]) / 2) + x[k - 1], ((y[k] - y[k - 1]) / 2) + y[k - 1],
                                   current_timestamp])
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
        if (boat_data[i][2] - timestamp1) % 1000 == 0:
            extracted_data.append(boat_data[i])

    return extracted_data

if __name__ == "__main__":
    variable_speeds()
