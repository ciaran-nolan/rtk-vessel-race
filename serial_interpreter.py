import serial
import numpy as np
import numpy.linalg as la
import struct
import time
import math
from decimal import Decimal

def createserialcommunication():
    ser = serial.Serial() #open serial port
    ser.port ="COM9"
    ser.baudrate = 19200
    ser.open()
   # print(ser.name)
    return ser


def ubxnavposllh(ser):
    time.sleep(.1)
    bytes2 = b'\xb5b\x01\x02\x1c\x00\x88l\xcf\x1d0\x16K\xfcL\xf6\xc5\x1fNY\x01\x00\xe3\x8a\x00\x00\xd0\x08\x00\x00\x1c' \
            b'\x13\x00\x00 '
    bytes = ser.read(34)
    print(bytes)
    headerbyte1 = bytes[0]
    headerbyte2 = bytes[1]
    overhead = bytes[2]
    overhead2 = bytes[3]
    message_size = int.from_bytes(bytes[4:6],"little")
    timeweek = int.from_bytes(bytes[6:10],"little")
    longitude = struct.unpack("<i",bytes[10:14])
    revisedlongitude = longitude[0] * 1e-7
    latitude = struct.unpack("<I",bytes[14:18])
    #latitude = int.from_bytes(bytes[14:18],"little")
    revisedlatitude = latitude[0]*1e-7
    heightellipsoid = int.from_bytes(bytes[18:22],"little")
    heightmsl = int.from_bytes(bytes[22:26],"little")
    horiaccuracy = int.from_bytes(bytes[26:30],"little")
    vertaccuracy = int.from_bytes(bytes[30:34],"little")
    print(revisedlongitude)

def ubxnavrelposned(ser):
    bytes = ser.read(46)
    #bytes2=b'\xb5b\x01<(\x00\x00\x00\x00\x00\x88r3"*\x01\x00\x00\xe5\x01\x00\x00B\xff\xff\xff68\xde\x00\xee\x0e\x00\x00'
    #headerbyte1 = bytes[0]
    #headerbyte2 = bytes[1]
    #class_byte = bytes[0]
    #id = bytes[1]
    #message_size = int.from_bytes(bytes[2:4], "little")
    #message_version = bytes[4]
    #reserved = bytes[5]
    #ref_station_id = bytes[6:8]
    #timeweek = int.from_bytes(bytes[8:12], "little")
    relposn = struct.unpack("<l",bytes[12:16])
    relpose = struct.unpack("<l", bytes[16:20])
    relposd = struct.unpack("<l", bytes[20:24])
    relposhpn = np.uintc(bytes[24]) * 1e-2
    relposhpe = np.uintc(bytes[25]) * 1e-2
    relposhpd = np.uintc(bytes[26]) * 1e-2
    #reserved2 = bytes[27]
    #accn =int.from_bytes(bytes[28:32], "little")
    #acce = int.from_bytes(bytes[32:36], "little")
    #accd = int.from_bytes(bytes[36:40], "little")
    #flags = bytes[40:44]
    #check1 = bytes[44];
    #check2 = bytes[45];

    resolvedn = relposn[0] + relposhpn
    resolvede = relpose[0] + relposhpe
    resolvedd = relposd[0] + relposhpd


    #lineardistance = math.sqrt(resolvedn**2+resolvede**2)/100
    #print(lineardistance)
    return [resolvedn, resolvede, resolvedd]


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """

    dot = v1[0] * v2[0] + v1[1] * v2[1]  # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0]  # determinant
    angle = -math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    print(angle*(180/math.pi))
    return angle

def has_crossed_line(base_vector, ser):
    crossedline = False

    while not(crossedline):

        checknum = check_bytes(ser)
        while checknum != 1:
            checknum = check_bytes(ser)
        rover_vector = ubxnavrelposned(ser)
        angle = angle_between((base_vector[0],base_vector[1]), (rover_vector[0], rover_vector[1]))
        #print(angle*(180/math.pi))
        if angle < 0:
            crossedline = True;

    return


def check_bytes(ser):
    ser.flush()
    bytes = []
    bytes.append(ser.read(1))

    if int.from_bytes(bytes[0], "little") == 36:
        nmea_end = False
        i = 1
        while not(nmea_end):
            bytes.append(ser.read(1))
            print( int.from_bytes(bytes[i],"little"))
            if  int.from_bytes(bytes[i],"little") == 10:
                nmea_end = True
            else:
                i+=1
        check_bytes(ser)
    else:
        bytes.append(ser.read(1))
        if int.from_bytes(bytes[0],"little") == 181:
            #vector = ubxnavrelposned(ser)
            #print(vector)
            return 1


def perpenddicular_distance(base_vector,vecrover):
    lineardistance = math.sqrt(vecrover[0]**2+vecrover[1]**2)
    perpdist = math.sqrt(lineardistance**2+math.sqrt(base_vector[0]**2+base_vector[1]**2))
    print(perpdist)
    print(lineardistance)
    print(math.sqrt(30**2))

def main():
    s = createserialcommunication()
    checkreturn = check_bytes(s)
    while checkreturn != 1:
        checkreturn = check_bytes(s)

    base_vector = ubxnavrelposned(s)
    #base_vector = [-1684.44, -2476.23, 37.8]
    print(base_vector)
    input("Press any key to begin")
   #base_vector = ubxnavrelposned(s)
    has_crossed_line(base_vector,s)
    print("Receiver has crossed line at ",)

    return 0


if __name__ == "__main__":
    main()