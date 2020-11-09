from math import radians, cos, sin, asin, sqrt

# separate x, y coords from relative position vectors
def separate_x_y_coords(coordinate_list):
    x = [i[0] for i in coordinate_list]
    y = [i[1] for i in coordinate_list]
    return x, y

# separate timestamp and shortest distances
def shortest_distance(distance_data):
    distance = [i[0] for i in distance_data]
    timestamp = [i[1] for i in distance_data]
    return distance, timestamp

# calculate perpendicular distance between finish line and boat
def perpendicular_distance(base_ned, boat_ned):
    perpdist = abs((base_ned[1] * boat_ned[0] - base_ned[0] * boat_ned[1])) / (
        sqrt(base_ned[0] ** 2 + base_ned[1] ** 2))
    print("Perpendicular distance is: ", perpdist)
    return perpdist


# Function to calculate the distance between two points on Earth
def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radius of earth in km
    r = 6371

    # calculate the result
    return (c * r)


def tools_main():

    lat1 = 52.79271561
    lat2 = 52.792725724
    lon1 = -6.139479904
    lon2 = -6.139467550

    print(distance(lat1, lat2, lon1, lon2), "K.M")

if __name__ == "__main__":
    tools_main()
