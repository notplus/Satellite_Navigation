'''
Description: 
Author: notplus
Date: 2021-03-28 20:19:07
LastEditors: notplus
LastEditTime: 2021-03-28 20:19:09
FilePath: /satellite_coordinate/ephemeris_module/ephemeris.py
'''

import utils.constant as constant
from utils.utils import parseDouble
import math
from utils.time_convert import Time
from ephemeris_module.satellite_type.gps import GPS
from ephemeris_module.satellite_type.bds import BDS

class Ephemeris:
    def __init__(self, path):
        self.__parseFile(path)

    def __parseFile(self, path):
        print("parse file %s" % path)
        with open(path, 'r') as f:
            lines = f.readlines()

            # RINEX 2 GPS Navigation
            # parse header
            # line 1 RINEX VERSION / TYPE
            self.__rinex_version = lines[0][0:9]
            self.__type = lines[0][20:21]

            # line 2 PGM / RUN BY / DATE
            self.__pgm = lines[1][0:20]
            self.__run_by = lines[1][20:40]
            self.__data = lines[1][40:60]

            # line 3 COMMENT
            self.__comment = lines[2][0:60]

            # line 4 ION ALPHA
            self.__ion_alpha_a0 = parseDouble(lines[3][2:14])
            self.__ion_alpha_a1 = parseDouble(lines[3][14:26])
            self.__ion_alpha_a2 = parseDouble(lines[3][26:40])
            self.__ion_alpha_a3 = parseDouble(lines[3][40:52])

            # line 5 ION BETA
            self.__ion_beta_b0 = parseDouble(lines[4][2:14])
            self.__ion_beta_b1 = parseDouble(lines[4][14:26])
            self.__ion_beta_b2 = parseDouble(lines[4][26:40])
            self.__ion_beta_b3 = parseDouble(lines[4][40:52])

            # line 6 DELTA-UTC: A0,A1,T,W
            self.__a0 = parseDouble(lines[5][3:22])
            self.__a1 = parseDouble(lines[5][22:41])
            self.__t = int(lines[5][41:50])
            self.__w = int(lines[5][50:59])

            # line 7 LEAP SECONDS
            self.__delta_t = int(lines[6][0:6])

            # line 8 END OF HEADER

            # satellite records
            self.__satellites = []
            i = 8
            while i < len(lines):
                satellite = None
                if lines[0][0] == 'G':
                    satellite = GPS(lines[i:i+8])
                    i += 8
                elif lines[0][0] == 'C':
                    satellite = BDS(lines[i:i+8])
                    i += 8
                elif lines[0][0] == 'R':
                    satellite = None
                    i += 4
                elif lines[0][0] == 'S':
                    satellite = None
                    i += 4
                elif lines[0][0] == 'E':
                    satellite = None
                    i += 8
                elif lines[0][0] == 'J':
                    satellite = None
                    i += 8
                elif lines[0][0] == 'I':
                    satellite = None
                    i += 8
                else:
                    satellite = GPS(lines[i:i+8])
                    i += 8

                if satellite:
                    self.__satellites += [satellite]

    '''
    description: 
    param {*} self
    param {*} prn
    param {*} t
    return {*}
    '''

    def computeSatelliteCoordinates(self, prn, t):
        t = t.GPST()
        t_k = t
        index = 0
        for i in range(len(self.__satellites)):
            if prn == self.__satellites[i].record.prn:
                tmp_t_k = t-self.__satellites[i].record.toe
                if abs(tmp_t_k) < abs(t_k):
                    index = i
                    t_k = abs(tmp_t_k)

        if abs(t_k) > 7200:
            print("Warning: the time difference is too large")
        
        return self.__satellites[index].ComputeCoord(t)
