'''
Description: 
Author: notplus
Date: 2021-03-28 16:59:12
LastEditors: notplus
LastEditTime: 2021-03-29 10:34:15
FilePath: /satellite_coordinate/media/notplus/DATA1/course/satellite/satellite_coordinate/ephemeris_module/satellite_type/bds.py
'''

from ephemeris_module.satellite import Satellite
from utils.utils import parseDouble
from utils.utils import is_bds_geo
from utils.utils import rotation_matrix
from utils.utils import rotation_matrix_z
from utils.utils import rotation_matrix_x
import math
import utils.constant as constant
import numpy as np


class _BDSRecord(object):
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

    def setOrbit1(self, aode, c_rs, delta_n, m_0):
        self.aode = aode
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

    def setOrbit5(self, idot, bds_week):
        self.idot = idot
        # self.spare = spare
        self.bds_week = bds_week
        # self.l2_flag = l2_flag

    def setOrbit6(self, sv_accuacy, sat_h1, tgd1, tgd2):
        self.sv_accuacy = sv_accuacy
        self.sat_h1 = sat_h1
        self.tgd1 = tgd1
        self.tgd2 = tgd2

    def setOrbit7(self, trans_time, aodc):
        self.trans_time = trans_time
        self.aodc = aodc
        # self.backup_1 = backup_1
        # self.backup_2 = backup_2


class BDS(Satellite):
    def __init__(self, lines):
        # line 1
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

        self.record = _BDSRecord('C', prn, year, month, day, hour,
                                 minute, second, clock_bias, clock_drift, clock_drift_rate)

        # Orbit 1
        self.record.setOrbit1(parseDouble(lines[1][4:23]), parseDouble(lines[1][23:42]),
                              parseDouble(lines[1][42:61]), parseDouble(lines[1][61:80]))

        # Orbit 2
        self.record.setOrbit2(parseDouble(lines[2][4:23]), parseDouble(lines[2][23:42]),
                              parseDouble(lines[2][42:61]), parseDouble(lines[2][61:80]))

        # Orbit 3
        self.record.setOrbit3(parseDouble(lines[3][4:23]), parseDouble(lines[3][23:42]),
                              parseDouble(lines[3][42:61]), parseDouble(lines[3][61:80]))

        # Orbit 4
        self.record.setOrbit4(parseDouble(lines[4][4:23]), parseDouble(lines[4][23:42]),
                              parseDouble(lines[4][42:61]), parseDouble(lines[4][61:80]))

        # Orbit 5
        self.record.setOrbit5(parseDouble(lines[5][4:23]),
                              parseDouble(lines[5][42:61]))

        # Orbit 6
        self.record.setOrbit6(parseDouble(lines[6][4:23]), parseDouble(lines[6][23:42]),
                              parseDouble(lines[6][42:61]), parseDouble(lines[6][61:80]))

        # Orbit 7
        self.record.setOrbit7(parseDouble(
            lines[7][4:23]), parseDouble(lines[7][23:42]))

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

        if is_bds_geo(self.record.prn):
            lambda_ = self.record.omega_0+self.record.omega_dot - \
                5/180*math.pi-constant.omega_e*self.record.toe
            xyzl = np.array([[math.cos(u)*math.cos(lambda_)-math.sin(u)* math.cos(i)*math.sin(lambda_)], 
                             [math.cos(u)*math.sin(lambda_)+math.sin(u)* math.cos(i)*math.cos(lambda_)], 
                             [math.sin(u)*math.sin(i)]])
            print(rotation_matrix(0,0,constant.omega_e*t_k))
            # return r*np.dot(np.dot(rotation_matrix(0,0,constant.omega_e*t_k),rotation_matrix(-5/180*math.pi,0,0)),xyzl)
            return r*np.dot(np.dot(rotation_matrix_z(constant.omega_e*t_k),rotation_matrix_x(-5/180*math.pi)),xyzl)

        else:
            lambda_ = self.record.omega_0 + \
                (self.record.omega_dot-constant.omega_e) * \
                t_k-constant.omega_e*self.record.toe
            X = r*(math.cos(u)*math.cos(lambda_)-math.sin(u)
                   * math.cos(i)*math.sin(lambda_))
            Y = r*(math.cos(u)*math.sin(lambda_)+math.sin(u)
                   * math.cos(i)*math.cos(lambda_))
            Z = r*math.sin(u)*math.sin(i)

            return X, Y, Z
