'''
Description: 
Author: notplus
Date: 2021-03-19 21:35:25
LastEditors: notplus
LastEditTime: 2021-03-21 22:07:30
'''

from utils.constant import *
from utils.utils import parseDouble


class OC:
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second


class SatelliteRecord:
    def __init__(self, prn, oc, clock_bias, clock_drift, clock_drift_rate):
        self.prn = prn
        self.oc = oc
        self.clock_bias = clock_bias
        self.clock_drift = clock_drift
        self.clock_drift_rate = clock_drift_rate

    def setOrbit1(self, iode, c_rs, delta_n, m_0):
        self.iode = iode
        self.c_rs = c_rs
        self.delta_n = delta_n
        self.m_0 = m_0

    def setOrbit2(self, c_uc, e, c_us, sqrt_a):
        self.c_uc = c_uc
        self.e = e
        self.c_us = c_us
        self.sqrt_a = sqrt_a

    def setOrbit3(self, toe, c_ic, omega_0, c_is):
        self.toe = toe
        self.c_ic = c_ic
        self.omega_0 = omega_0
        self.c_is = c_is

    def setOrbit4(self, i_0, c_rc, omega, oemga_dot):
        self.i_0 = i_0
        self.c_rc = c_rc
        self.omega = omega
        self.oemga_dot = oemga_dot

    def setOrbit5(self, i, code_l2, gps_week, l2_flag):
        self.i = i
        self.code_l2 = code_l2
        self.gps_week = gps_week
        self.l2_flag = l2_flag

    def setOrbit6(self, precision, status, tgd, iodc):
        self.precision = precision
        self.status = status
        self.tgd = tgd
        self.iodc = iodc

    def setOrbit7(self, send_time, h, backup_1, backup_2):
        self.send_time = send_time
        self.h = h
        self.backup_1 = backup_1
        self.backup_2 = backup_2


class Ephemeris:
    def __init__(self, path):
        self.__parseFile(path)

    def __parseFile(self, path):
        print("parse file %s" % path)
        with open(path, 'r') as f:
            # RINEX 2 GPS Navigation
            # parse header
            # line 1 RINEX VERSION / TYPE
            self.__rinex_version = f.read(9)
            f.read(11)
            self.__type = f.read(1)
            f.read(19)
            f.read(40)
            f.read(1)

            # line 2 PGM / RUN BY / DATE
            self.__pgm = f.read(20)
            self.__run_by = f.read(20)
            self.__data = f.read(20)
            f.read(20)
            f.read(1)

            # line 3 COMMENT
            self.__comment = f.read(60)
            f.read(20)
            f.read(1)

            # line 4 ION ALPHA
            f.read(2)
            self.__ion_alpha_a0 = parseDouble(f.read(12))
            self.__ion_alpha_a1 = parseDouble(f.read(12))
            self.__ion_alpha_a2 = parseDouble(f.read(12))
            self.__ion_alpha_a3 = parseDouble(f.read(12))
            f.read(30)
            f.read(1)

            # line 5 ION BETA
            f.read(2)
            self.__ion_beta_b0 = parseDouble(f.read(12))
            self.__ion_beta_b1 = parseDouble(f.read(12))
            self.__ion_beta_b2 = parseDouble(f.read(12))
            self.__ion_beta_b3 = parseDouble(f.read(12))
            f.read(30)
            f.read(1)

            # line 6 DELTA-UTC: A0,A1,T,W
            f.read(3)
            self.__a0 = parseDouble(f.read(19))
            self.__a1 = parseDouble(f.read(19))
            self.__t = int(f.read(9))
            self.__w = int(f.read(9))
            f.read(21)
            f.read(1)

            # line 7 LEAP SECONDS
            self.__delta_t = int(f.read(6))
            f.read(74)
            f.read(1)

            # line 8 END OF HEADER
            f.read(60)
            f.read(20)
            f.read(1)

            # satellite records
            self.__records=[]
            while f:
                # line 1
                prn = int(f.read(2))
                f.read(1)
                year = int(f.read(2))

                f.read(1)
                month = int(f.read(2))
                f.read(1)
                day = int(f.read(2))
                f.read(1)
                hour = int(f.read(2))
                f.read(1)
                minute = int(f.read(2))

                second = float(f.read(5))

                clock_bias = parseDouble(f.read(19))
                clock_drift = parseDouble(f.read(19))
                clock_drift_rate = parseDouble(f.read(19))
                f.read(1)

                oc = OC(year, month, day, hour, minute, second)

                record = SatelliteRecord(
                    prn, oc, clock_bias, clock_drift, clock_drift_rate)

                # Orbit 1
                f.read(3)
                record.setOrbit1(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)
                
                # Orbit 2
                f.read(3)
                record.setOrbit2(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)

                # Orbit 3
                f.read(3)
                record.setOrbit3(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)

                # Orbit 4
                f.read(3)
                record.setOrbit4(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)

                # Orbit 5
                f.read(3)
                record.setOrbit5(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)

                # Orbit 6
                f.read(3)
                record.setOrbit6(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)

                # Orbit 7
                f.read(3)
                record.setOrbit7(parseDouble(f.read(19)), parseDouble(f.read(19)),
                                 parseDouble(f.read(19)), parseDouble(f.read(19)))
                f.read(1)
                
                self.__records += [record]

    def test(self):
        print(self.__rinex_version)
        