'''
Description: 
Author: notplus
Date: 2021-03-28 17:03:06
LastEditors: notplus
LastEditTime: 2021-04-07 14:13:51
FilePath: /satellite_coordinate/ephemeris_module/satellite_type/gps.py
'''

from ephemeris_module.satellite import Satellite
from utils.utils import parseDouble
from utils.time_convert import Time
import math
import utils.constant as constant

class _GPSRecord(object):
    def __init__(self, system, prn, year, month, day, hour, minute, second, clock_bias, clock_drift, clock_drift_rate):
        self.system = system
        self.prn = prn
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
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
        self.omega_dot = oemga_dot

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


class GPS(Satellite):
    def __init__(self, lines):
        i = 0
        if lines[0][0] == 'G':
            i += 1
            prn = int(lines[0][1:3])
            year = int(lines[0][4:8])
            month = int(lines[0][9:11])
            day = int(lines[0][12:14])
            hour = int(lines[0][15:17])
            minute = int(lines[0][18:20])
            second = float(lines[0][21:23])
            clock_bias = parseDouble(lines[0][23:42])
            clock_drift = parseDouble(lines[0][42:61])
            clock_drift_rate = parseDouble(lines[0][61:80])

            self.record = _GPSRecord('G', prn, year, month, day, hour,
                                     minute, second, clock_bias, clock_drift, clock_drift_rate)
        else:
            prn = int(lines[0][0:2])
            year = int(lines[0][3:5])
            month = int(lines[0][6:8])
            day = int(lines[0][9:11])
            hour = int(lines[0][12:14])
            minute = int(lines[0][15:17])
            second = float(lines[0][17:22])
            clock_bias = parseDouble(lines[0][22:41])
            clock_drift = parseDouble(lines[0][41:60])
            clock_drift_rate = parseDouble(lines[0][60:79])

            self.record = _GPSRecord('G', prn, year, month, day, hour,
                                     minute, second, clock_bias, clock_drift, clock_drift_rate)

        # Orbit 1
        self.record.setOrbit1(parseDouble(lines[1][3+i:22+i]), parseDouble(lines[1][22+i:41+i]),
                              parseDouble(lines[1][41+i:60+i]), parseDouble(lines[1][60+i:79+i]))

        # Orbit 2
        self.record.setOrbit2(parseDouble(lines[2][3+i:22+i]), parseDouble(lines[2][22+i:41+i]),
                              parseDouble(lines[2][41+i:60+i]), parseDouble(lines[2][60+i:79+i]))

        # Orbit 3
        self.record.setOrbit3(parseDouble(lines[3][3+i:22+i]), parseDouble(lines[3][22+i:41+i]),
                              parseDouble(lines[3][41+i:60+i]), parseDouble(lines[3][60+i:79+i]))

        # Orbit 4
        self.record.setOrbit4(parseDouble(lines[4][3+i:22+i]), parseDouble(lines[4][22+i:41+i]),
                              parseDouble(lines[4][41+i:60+i]), parseDouble(lines[4][60+i:79+i]))

        # Orbit 5
        self.record.setOrbit5(parseDouble(lines[5][3+i:22+i]), parseDouble(lines[5][22+i:41+i]),
                              parseDouble(lines[5][41+i:60+i]), parseDouble(lines[6][60+i:79+i]))

        # Orbit 6
        self.record.setOrbit6(parseDouble(lines[6][3+i:22+i]), parseDouble(lines[6][22+i:41+i]),
                              parseDouble(lines[6][41+i:60+i]), parseDouble(lines[6][60+i:79+i]))

        # Orbit 7
        if i == 0:
            self.record.setOrbit7(parseDouble(lines[7][3+i:22+i]), parseDouble(lines[7][22+i:41+i]),
                                  parseDouble(lines[7][41+i:60+i]), parseDouble(lines[7][60+i:79+i]))
        else:
            self.record.setOrbit7(parseDouble(lines[7][3+i:22+i]), parseDouble(lines[7][22+i:41+i]),
                                  0, 0)

    def ComputeCoord(self, t):
        t_k = t-self.record.toe
        a = self.record.sqrt_a*self.record.sqrt_a
        n_0 = math.sqrt(constant.mu/a/a/a)
        n = n_0+self.record.delta_n
        m_k = self.record.m_0+n*t_k

        e_k1 = m_k
        e_k0 = 0.0
        while abs(e_k1-e_k0) > 1e-12:
            e_k0 = e_k1
            e_k1 = m_k+self.record.e*math.sin(e_k0)
        e_k = e_k1
        v_k = math.atan(math.sqrt(1-self.record.e*self.record.e) /
                        (1-self.record.e)*math.tan(e_k/2))*2

        u_k = v_k+self.record.omega

        delta_u_k = self.record.c_uc * \
            math.cos(2*u_k)+self.record.c_us*math.sin(2*u_k)
        delta_r_k = self.record.c_rc * \
            math.cos(2*u_k)+self.record.c_rs*math.sin(2*u_k)
        delta_i_k = self.record.c_ic * \
            math.cos(2*u_k)+self.record.c_is*math.sin(2*u_k)

        u = u_k+delta_u_k
        r = a*(1-self.record.e*math.cos(e_k))+delta_r_k
        i = self.record.i_0+delta_i_k

        x = r*math.cos(u)
        y = r*math.sin(u)

        lambda_ = self.record.omega_0 + \
            (self.record.omega_dot-constant.omega_e) * \
            t_k-constant.omega_e*self.record.toe

        X = r*(math.cos(u)*math.cos(lambda_)-math.sin(u)
               * math.cos(i)*math.sin(lambda_))
        Y = r*(math.cos(u)*math.sin(lambda_)+math.sin(u)
               * math.cos(i)*math.cos(lambda_))
        Z = r*math.sin(u)*math.sin(i)

        t_c = t - Time(2000+self.record.year,self.record.month,self.record.day,self.record.hour,self.record.minute,int(self.record.second)).GPST()
        ct = self.record.clock_bias+self.record.clock_drift*t_c+self.record.clock_drift_rate*t_c*t_c

        return X, Y, Z, ct
