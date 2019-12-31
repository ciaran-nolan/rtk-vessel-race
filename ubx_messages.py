import numpy as np
import serial
import struct
import time

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
    #bytes = ser.read(46)
    bytes=b'\xb5b\x01<(\x00\x00\x00\x00\x00\x88r3"*\x01\x00\x00\xe5\x01\x00\x00B\xff\xff\xff68\xde\x00\xee\x0e\x00\x00'
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


