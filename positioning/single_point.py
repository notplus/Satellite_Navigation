'''
Description: 
Author: notplus
Date: 2021-05-26 08:51:32
LastEditors: notplus
LastEditTime: 2021-05-28 17:45:09
FilePath: /positioning/single_point.py

Copyright (c) 2021 notplus
'''

from datetime import time, timedelta
from utils.utils import rotation_matrix_y, rotation_matrix_z
from ephemeris_module.ephemeris import Ephemeris
from observation.observation import Observation
import utils.constant as constant
from utils.coord_sys_trans import wgs84_to_ecef
import math
import numpy as np
from utils.coord_sys_trans import get_wgs84_elevation_azimuth
from positioning.correction import *
import matplotlib.pyplot as plt


class SinglePointPositioning(object):
    def __init__(self, ephemeris_path, observation_path):
        self.__ephemeris = Ephemeris(ephemeris_path)
        self.__observation = Observation(observation_path)

    '''
    @description: 
    @param {*} self
    @param {*} t
    @return {*}
    '''

    def positioning(self, t, evaluate_precision=False):
        X, Y, Z, dt_r = 1000, 1000, 1000, 0
        obs = self.__observation.find_last_observation(t)
        num_satellites = 0
        for k in obs.data.keys():
            if k[0] == 'G':
                num_satellites += 1

        while True:
            A = np.zeros([num_satellites, 4])
            l = np.zeros([num_satellites, 1])
            P = np.identity(num_satellites)
            i = 0
            for prn in obs.data:
                if prn[0] != 'G':
                    continue
                if 'Obs' not in obs.data[prn]['P1'] or 'Obs' not in obs.data[prn]['P2']:
                    continue
                rho = obs.data[prn]['P1']['Obs']
                _, _, _, dt_s = self.__ephemeris.compute_satellite_coordinates(
                    prn, t)

                ts_1 = obs.epoch.clone()
                ts_1.set_float_second(ts_1.get_float_second()-rho/constant.c)
                _, _, _, dt_s_1 = self.__ephemeris.compute_satellite_coordinates(
                    prn, ts_1)
                ts_2 = obs.epoch.clone()
                ts_2.set_float_second(
                    obs.epoch.get_float_second()-rho/constant.c-dt_s_1)

                while abs(ts_2.get_float_second()-ts_1.get_float_second()) >= 1e-8:
                    ts_1 = ts_2.clone()
                    ts_2 = obs.epoch.clone()
                    _, _, _, dt_s_1 = self.__ephemeris.compute_satellite_coordinates(
                        prn, ts_1)
                    ts_2.set_float_second(
                        ts_2.get_float_second()-rho/constant.c-dt_s_1)

                sx, sy, sz, dt_s = self.__ephemeris.compute_satellite_coordinates(
                    prn, ts_2)

                # 相对论效应改正
                dt_s += compute_relativistic_correction(
                    self.__ephemeris.find_last_satellite_ephemeris(prn, t.GPST()), ts_2.GPST())

                # 地球自转改正
                dt_earth = t.clone()
                dt_earth.set_float_second(
                    dt_earth.get_float_second()+dt_r/constant.c-ts_2.get_float_second())
                nx, ny, nz = wgs84_to_ecef(
                    sx, sy, sz, dt_earth.get_float_second()*constant.omega_e)

                # 权阵计算
                elevation, azimuth = get_wgs84_elevation_azimuth(
                    X, Y, Z, nx, ny, nz)
                P[i][i] = math.sin(elevation)*math.sin(elevation)

                # 电离层改正
                phi, lambda_, _ = wgs84_to_blh(nx, ny, nz)
                delta_ion = compute_ionosphere_correction_k8_model(
                    ts_2, self.__ephemeris, elevation, azimuth, phi, lambda_)

                # 对流层改正
                _, _, h_r = wgs84_to_blh(X, Y, Z)
                delta_tro = compute_troposphere_correction_hopfield(
                    h_r, elevation)

                R = math.sqrt((nx-X)*(nx-X)+(ny-Y)*(ny-Y)+(nz-Z)*(nz-Z))
                A[i][0] = (X-nx)/R
                A[i][1] = (Y-ny)/R
                A[i][2] = (Z-nz)/R
                A[i][3] = 1
                l[i][0] = rho - R + constant.c*dt_s + \
                    1.54573 * (rho - obs.data[prn]['P2']['Obs']) + delta_tro
                i += 1

            nxx = np.dot(np.dot(np.dot(np.linalg.inv(
                np.dot(np.dot(A.transpose(), P), A)), A.transpose()), P), l)

            X += nxx[0][0]
            Y += nxx[1][0]
            Z += nxx[2][0]
            dt_r = nxx[3][0]

            if np.linalg.norm(nxx[0:3]) < 0.01:
                if evaluate_precision:
                    Q_xx = np.linalg.inv(np.dot(A.transpose(), A))
                    GDOP = np.sqrt(np.trace(Q_xx))
                    PDOP = np.sqrt(np.trace(Q_xx)-Q_xx[3, 3])
                    TDOP = np.sqrt(Q_xx[3, 3])

                    B, L, _ = wgs84_to_blh(X, Y, Z)
                    R3 = rotation_matrix_z(math.pi-L)
                    R2 = rotation_matrix_y(math.pi/2-B)
                    PY = np.identity(3)
                    PY[1, 1] = -1

                    R_THS_TES = np.dot(np.dot(R3, R2), PY)
                    T = np.identity(4)
                    T[0:3, 0:3] = R_THS_TES
                    Q_y = np.linalg.inv(T.T.dot(A.T).dot(A).dot(T))
                    HDOP = np.sqrt(Q_y[0, 0]+Q_y[1, 1])
                    VDOP = np.sqrt(Q_y[2, 2])

                    return X, Y, Z, GDOP, PDOP, TDOP, HDOP, VDOP
                break

        return X, Y, Z

    '''
    @description: 
    @param {*} self
    @param {*} prn
    @param {*} t
    @return {*}
    '''

    def compute_satellite_coordinates(self, prn, t):
        return self.__ephemeris.compute_satellite_coordinates(prn, t)

    def single_point_positioning_demo(self):
        start_time = self.__observation.get_observation_start_time()
        end_time = self.__observation.get_observation_end_time()

        while start_time < end_time:
            x, y, z = self.positioning(start_time)
            print(f"%s X=%f,Y=%f,Z=%f" % (start_time.isoformat(), x, y, z))
            start_time += timedelta(hours=2)

        self.single_point_positioning_dop_figure(int(
            (end_time-self.__observation.get_observation_start_time()).total_seconds()/30+1))

    def single_point_positioning_dop_figure(self, epoch):
        start_time = self.__observation.get_observation_start_time()
        end_time = self.__observation.get_observation_end_time()
        if start_time+timedelta(seconds=30*epoch) > end_time+timedelta(seconds=30):
            return
        gdops, pdops, tdops, hdops, vdops = [], [], [], [], []

        for i in range(epoch):
            _, _, _, gdop, pdop, tdop, hdop, vdop = self.positioning(
                start_time, True)
            gdops += [gdop]
            pdops += [pdop]
            tdops += [tdop]
            hdops += [hdop]
            vdops += [vdop]

            start_time += timedelta(seconds=30)

        x = np.arange(epoch)

        _, ax = plt.subplots(5, 1)
        ax[0].plot(x, gdops)
        ax[0].set_xlabel('Epoch')
        ax[0].set_ylabel('GDOP')
        ax[0].set_title('GDOP')

        ax[1].plot(x, pdops)
        ax[1].set_xlabel('Epoch')
        ax[1].set_ylabel('PDOP')
        ax[1].set_title('PDOP')

        ax[2].plot(x, tdops)
        ax[2].set_xlabel('Epoch')
        ax[2].set_ylabel('TDOP')
        ax[2].set_title('TDOP')

        ax[3].plot(x, hdops)
        ax[3].set_xlabel('Epoch')
        ax[3].set_ylabel('HDOP')
        ax[3].set_title('HDOP')

        ax[4].plot(x, vdops)
        ax[4].set_xlabel('Epoch')
        ax[4].set_ylabel('VDOP')
        ax[4].set_title('VDOP')

        plt.subplots_adjust(wspace=0, hspace=0.5)
        plt.show()

    def single_point_positioning_evaluate_chan(self, epoch):
        start_time = self.__observation.get_observation_start_time()
        end_time = self.__observation.get_observation_end_time()
        if start_time+timedelta(seconds=30*epoch) > end_time+timedelta(seconds=30):
            return
    
        ax, ay, az = -0.267442768572702E+07, 0.375714305701559E+07, 0.439152148514515E+07
        ex, ey, ez = [], [], []
        for i in range(epoch):
            x, y, z = self.positioning(start_time)
            ex += [(x-ax)]
            ey += [(y-ay)]
            ez += [(z-az)]
            
            start_time += timedelta(seconds=30)

        x = np.arange(epoch)

        plt.plot(x,ex,label='dX')
        plt.plot(x,ey,label='dY')
        plt.plot(x,ez,label='dZ')
        plt.xlabel('Epoch')
        plt.ylabel('Error(m)')
        plt.legend()
        plt.show()