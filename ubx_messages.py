# Python script to extract and examine certain UBX messages

import numpy as np
import struct
import time


class FinishPin:
    def __init__(self, north, east):
        self.relpos = [north, east]

# is nmea is enabled along side ubx - need to ignore it
# can ignore this if nmea is disabled at the receiver
def check_bytes(ser):
    ser.flush()
    bytes = []
    bytes.append(ser.read(1))

    if int.from_bytes(bytes[0], "little") == 36:
        nmea_end = False
        i = 1
        while not (nmea_end):
            bytes.append(ser.read(1))
            print(int.from_bytes(bytes[i], "little"))
            if int.from_bytes(bytes[i], "little") == 10:
                nmea_end = True
            else:
                i += 1
        check_bytes(ser)
    else:
        bytes.append(ser.read(1))
        if int.from_bytes(bytes[0], "little") == 181:
            return 1

# top level function to check for a UBX-NAV-RELPOSNED message
def isrelposned(ser):
    checknum = check_bytes(ser)
    while checknum != 1:
        checknum = check_bytes(ser)

# Byte by Byte breakdown of UBX-NAV-POSLLH
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
    message_size = int.from_bytes(bytes[4:6], "little")
    timeweek = struct.unpack("<I", bytes[10:14])
    longitude = struct.unpack("<i", bytes[10:14])
    revisedlongitude = longitude[0] * 1e-7
    latitude = struct.unpack("<I", bytes[14:18])
    # latitude = int.from_bytes(bytes[14:18],"little")
    revisedlatitude = latitude[0] * 1e-7
    heightellipsoid = int.from_bytes(bytes[18:22], "little")
    heightmsl = int.from_bytes(bytes[22:26], "little")
    horiaccuracy = int.from_bytes(bytes[26:30], "little")
    vertaccuracy = int.from_bytes(bytes[30:34], "little")
    print(revisedlongitude)

# Byte by byte breakdown of UBX-NAV_RELPOSNED, not only timeweek,relposn, relpose are used in this project.
def ubxnavrelposned(ser):
    bytes = ser.read(46)

    # headerbyte1 = bytes[0]
    # headerbyte2 = bytes[1]
    # class_byte = bytes[0]
    # id = bytes[1]
    # message_size = int.from_bytes(bytes[2:4], "little")
    # message_version = bytes[4]
    # reserved = bytes[5]
    # ref_station_id = bytes[6:8]
    timeweek = struct.unpack("<L", bytes[8:12])[0]
    relposn = struct.unpack("<l", bytes[12:16])
    relpose = struct.unpack("<l", bytes[16:20])
    relposd = struct.unpack("<l", bytes[20:24])
    relposhpn = np.uintc(bytes[24]) * 1e-2
    relposhpe = np.uintc(bytes[25]) * 1e-2
    relposhpd = np.uintc(bytes[26]) * 1e-2
    # reserved2 = bytes[27]
    # accn =int.from_bytes(bytes[28:32], "little")
    # acce = int.from_bytes(bytes[32:36], "little")
    # accd = int.from_bytes(bytes[36:40], "little")
    # flags = bytes[40:44]
    # check1 = bytes[44];
    # check2 = bytes[45];

    return [relposn[0], relpose[0], relposd[0], timeweek]
