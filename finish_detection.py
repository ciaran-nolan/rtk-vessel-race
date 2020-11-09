import math
import ubx_messages
import distance


## A variety of finish detection methods evaluated during system develpment

# used for the angle between two vectors
def angle_between(vector1, vector2):
    dot_prod = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    determinant = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    # use atan2 to compute angle
    angle = -math.atan2(determinant, dot_prod)
    return angle


# Real-time processing of base/rover angles to detect a line crossing
def has_crossed_line_angle(base_ned, ser):
    # using boolean variable for better visualisation purposes
    crossed_line = False

    while not crossed_line:
        # check for relative position message
        ubx_messages.isrelposned(ser)
        # poll a relative position message
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        # calculate angle
        angle = angle_between((base_ned[0], base_ned[1]), (boat_ned[0], boat_ned[1]))
        if angle < 0:
            # line crossing has occurred, exit.
            crossed_line = True
    return


## Line crossing based on shortst distance
def has_crossed_line_dist(base_ned, ser):
    crossed_line = False

    while not crossed_line:
        # check for relative position message
        ubx_messages.isrelposned(ser)
        #extract relative position message
        boat_ned = ubx_messages.ubxnavrelposned(ser)
        # calculate perpendicular distance
        dist = distance.pnt2line(boat_ned, base_ned)
        if dist < 0:
            crossed_line = True
    return

## Line crossing using point above or below to slope of the finish line
def has_crossed_slope(base, boat_ned):
    # detect whether the boat is above or below the finish_line
    if boat_ned[1] * base.position[0] > base.position[1] * boat_ned[0]:
        return 0
    else:
        return 1
