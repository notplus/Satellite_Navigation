'''
Description: 
Author: notplus
Date: 2021-03-28 20:19:07
LastEditors: notplus
LastEditTime: 2021-03-28 22:02:21
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

            # RINEX 2/3 GPS Navigation
            # parse header

            i = 0

            # line 1 RINEX VERSION / TYPE
            self.__rinex_version = float(lines[i][0:9])
            self.__type = lines[i][20:21]
            i += 1

            # line 2 PGM / RUN BY / DATE
            self.__pgm = lines[i][0:20]
            self.__run_by = lines[i][20:40]
            self.__data = lines[i][40:60]
            i += 1

            # COMMENT (optional)
            self.__comments = []
            while lines[i][60:80].strip() == "COMMENT":
                self.__comments += [lines[i][0:60]]
                i += 1

            if self.__rinex_version < 3:  # Version 2
                # ION ALPHA (optional)
                self.__ion_alpha_a0 = parseDouble(lines[i][2:14])
                self.__ion_alpha_a1 = parseDouble(lines[i][14:26])
                self.__ion_alpha_a2 = parseDouble(lines[i][26:40])
                self.__ion_alpha_a3 = parseDouble(lines[i][40:52])
                i += 1

                # ION BETA (optional)
                self.__ion_beta_b0 = parseDouble(lines[i][2:14])
                self.__ion_beta_b1 = parseDouble(lines[i][14:26])
                self.__ion_beta_b2 = parseDouble(lines[i][26:40])
                self.__ion_beta_b3 = parseDouble(lines[i][40:52])
                i += 1

                # DELTA-UTC: A0,A1,T,W (optional)
                self.__a0 = parseDouble(lines[i][3:22])
                self.__a1 = parseDouble(lines[i][22:41])
                self.__t = int(lines[i][41:50])
                self.__w = int(lines[i][50:59])
                i += 1

                # LEAP SECONDS (optional)
                self.__delta_t = int(lines[6][0:6])
                i += 1

            else:  # Version 3
                # IONOSPHERIC CORR (optional)
                self.__ionospheric_corr = dict()

                while lines[i][60:80].strip() == "IONOSPHERIC CORR":
                    iono = []
                    if lines[i][0:4].strip() == "GAL":
                        iono = [float(lines[i][5:17]), float(
                            lines[i][17:29]), float(lines[i][29:41])]
                    else:
                        iono = [float(lines[i][5:17]), float(lines[i][17:29]), float(
                            lines[i][29:41]), float(lines[i][41:53])]

                    if not lines[i][54:55].isspace():  # Time mark
                        iono += [lines[i][54:55]]

                    if not lines[i][56:57].isspace():  # SV ID
                        iono += [lines[i][56:57]]

                    self.__ionospheric_corr[lines[i][0:4].strip()] = iono
                    i += 1

                # TIME SYSTEM CORR (optional)
                self.__time_system_corr = dict()

                while lines[i][60:80].strip() == "TIME SYSTEM CORR":
                    time_sys = dict()
                    time_sys["a0"] = float(lines[i][5:22])
                    time_sys["a1"] = float(lines[i][22:38])
                    time_sys["T"] = int(lines[i][39:45])
                    time_sys["W"] = int(lines[i][46:50])
                    if not lines[i][51:56].isspace():
                        time_sys["S"] = lines[51:56]

                    if not lines[i][57:59].isspace():
                        time_sys["U"] = int(lines[i][57:59])

                    self.__time_system_corr[lines[i][0:4].strip()] = time_sys
                    i += 1

                # LEAP SECONDS (optional)
                self.__leap_seconds = dict()
                if lines[i][60:80].strip() == "LEAP SECONDS":
                    if not lines[i][0:6].isspace():
                        self.__leap_seconds["currentNum"] = int(lines[i][0:6])
                    if not lines[i][6:12].isspace():
                        self.__leap_seconds["dtLSF"] = int(lines[i][6:12])
                    if not lines[i][12:18].isspace():
                        self.__leap_seconds["WN_LSF"] = int(lines[i][12:18])
                    if not lines[i][18:24].isspace():
                        self.__leap_seconds["DN"] = int(lines[i][18:24])
                    if not lines[i][24:27].isspace():
                        self.__leap_seconds["TimeSysId"] = lines[i][24:27]
                    i += 1

            # END OF HEADER
            if lines[i][60:80].strip() == "END OF HEADER":
                i += 1

            # satellite records
            self.__satellites = []

            while i < len(lines):
                satellite = None
                if self.__rinex_version < 3:
                    satellite = GPS(lines[i:i+8])
                    i += 8
                elif lines[i][0] == 'G':
                    satellite = GPS(lines[i:i+8])
                    i += 8
                elif lines[i][0] == 'C':
                    satellite = BDS(lines[i:i+8])
                    i += 8
                elif lines[i][0] == 'R':
                    satellite = None
                    i += 4
                elif lines[i][0] == 'S':
                    satellite = None
                    i += 4
                elif lines[i][0] == 'E':
                    satellite = None
                    i += 8
                elif lines[i][0] == 'J':
                    satellite = None
                    i += 8
                elif lines[i][0] == 'I':
                    satellite = None
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
