'''
Description: 
Author: notplus
Date: 2021-03-19 21:35:25
LastEditors: notplus
LastEditTime: 2021-03-22 09:26:00
'''

import utils.constant as constant
from utils.utils import parseDouble
import math


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
        self._prn = prn
        self._oc = oc
        self._clock_bias = clock_bias
        self._clock_drift = clock_drift
        self._clock_drift_rate = clock_drift_rate

    def setOrbit1(self, iode, c_rs, delta_n, m_0):
        self._iode = iode
        self._c_rs = c_rs
        self._delta_n = delta_n
        self._m_0 = m_0

    def setOrbit2(self, c_uc, e, c_us, sqrt_a):
        self._c_uc = c_uc
        self._e = e
        self._c_us = c_us
        self._sqrt_a = sqrt_a

    def setOrbit3(self, toe, c_ic, omega_0, c_is):
        self._toe = toe
        self._c_ic = c_ic
        self._omega_0 = omega_0
        self._c_is = c_is

    def setOrbit4(self, i_0, c_rc, omega, oemga_dot):
        self._i_0 = i_0
        self._c_rc = c_rc
        self._omega = omega
        self._omega_dot = oemga_dot

    def setOrbit5(self, i, code_l2, gps_week, l2_flag):
        self._i = i
        self._code_l2 = code_l2
        self._gps_week = gps_week
        self._l2_flag = l2_flag

    def setOrbit6(self, precision, status, tgd, iodc):
        self._precision = precision
        self._status = status
        self._tgd = tgd
        self._iodc = iodc

    def setOrbit7(self, send_time, h, backup_1, backup_2):
        self._send_time = send_time
        self._h = h
        self._backup_1 = backup_1
        self._backup_2 = backup_2


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

            self.__records = []
            for i in range(8, len(lines), 8):
                # line 1
                prn = int(lines[i][0:2])
                year = int(lines[i][3:5])
                month = int(lines[i][6:8])
                day = int(lines[i][9:11])
                hour = int(lines[i][12:14])
                minute = int(lines[i][15:17])
                second = float(lines[i][17:22])

                clock_bias = parseDouble(lines[i][22:41])
                clock_drift = parseDouble(lines[i][41:60])
                clock_drift_rate = parseDouble(lines[i][60:79])

                oc = OC(year, month, day, hour, minute, second)

                record = SatelliteRecord(
                    prn, oc, clock_bias, clock_drift, clock_drift_rate)

                # Orbit 1
                record.setOrbit1(parseDouble(lines[i+1][3:22]), parseDouble(lines[i+1][22:41]),
                                 parseDouble(lines[i+1][41:60]), parseDouble(lines[i+1][60:79]))

                # Orbit 2
                record.setOrbit2(parseDouble(lines[i+2][3:22]), parseDouble(lines[i+2][22:41]),
                                 parseDouble(lines[i+2][41:60]), parseDouble(lines[i+2][60:79]))

                # Orbit 3
                record.setOrbit3(parseDouble(lines[i+3][3:22]), parseDouble(lines[i+3][22:41]),
                                 parseDouble(lines[i+3][41:60]), parseDouble(lines[i+3][60:79]))

                # Orbit 4
                record.setOrbit4(parseDouble(lines[i+4][3:22]), parseDouble(lines[i+4][22:41]),
                                 parseDouble(lines[i+4][41:60]), parseDouble(lines[i+4][60:79]))

                # Orbit 5
                record.setOrbit5(parseDouble(lines[i+5][3:22]), parseDouble(lines[i+5][22:41]),
                                 parseDouble(lines[i+5][41:60]), parseDouble(lines[i+6][60:79]))

                # Orbit 6
                record.setOrbit6(parseDouble(lines[i+6][3:22]), parseDouble(lines[i+6][22:41]),
                                 parseDouble(lines[i+6][41:60]), parseDouble(lines[i+6][60:79]))

                # Orbit 7
                record.setOrbit7(parseDouble(lines[i+7][3:22]), parseDouble(lines[i+7][22:41]),
                                 parseDouble(lines[i+7][41:60]), parseDouble(lines[i+7][60:79]))

                self.__records += [record]

    def computeSatelliteCoordinates(self, prn, t):
        t_k = t
        index = 0
        for i in range(len(self.__records)):
            if prn == self.__records[i]._prn:
                tmp_t_k = t-self.__records[i]._toe
                if abs(tmp_t_k) < abs(t_k):
                    index = i
                    t_k = abs(tmp_t_k)

        if abs(t_k) > 7200:
            print("Warning: the time difference is too large")
        record = self.__records[index]
        
        a = record._sqrt_a*record._sqrt_a
        n_0 = math.sqrt(constant.mu/a/a/a)
        n = n_0+record._delta_n
        m_k = record._m_0+n*t_k

        e_k1 = m_k
        e_k0 = 0.0
        while abs(e_k1-e_k0) > 1e-12:
            e_k0 = e_k1
            e_k1 = m_k+record._e*math.sin(e_k0)
        e_k = e_k1
        v_k = math.atan(math.sqrt(1-record._e*record._e) /
                        (1-record._e)*math.tan(e_k/2))*2

        u_k = v_k+record._omega

        delta_u_k = record._c_uc * \
            math.cos(2*u_k)+record._c_us*math.sin(2*u_k)
        delta_r_k = record._c_rc * \
            math.cos(2*u_k)+record._c_rs*math.sin(2*u_k)
        delta_i_k = record._c_ic * \
            math.cos(2*u_k)+record._c_is*math.sin(2*u_k)

        u = u_k+delta_u_k
        r = a*(1-record._e*math.cos(e_k))+delta_r_k
        i = record._i_0+delta_i_k

        x = r*math.cos(u)
        y = r*math.sin(u)

        lambda_ = record._omega_0 + \
            (record._omega_dot-constant.omega_e) * \
            t_k-constant.omega_e*record._toe

        X = r*(math.cos(u)*math.cos(lambda_)-math.sin(u)
               * math.cos(i)*math.sin(lambda_))
        Y = r*(math.cos(u)*math.sin(lambda_)+math.sin(u)
               * math.cos(i)*math.cos(lambda_))
        Z = r*math.sin(u)*math.sin(i)

        return X, Y, Z
