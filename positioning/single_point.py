'''
Description: 
Author: notplus
Date: 2021-05-26 08:51:32
LastEditors: notplus
LastEditTime: 2021-05-26 10:16:46
FilePath: /positioning/single_point.py

Copyright (c) 2021 notplus
'''

from ephemeris_module.ephemeris import Ephemeris
from observation.observation import Observation
import utils.constant as constant
from utils.coord_sys_trans import wgs84_to_ecef
import math
import numpy as np
from utils.coord_sys_trans import get_wgs84_elevation
from positioning.correction import compute_relativistic_correction


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

    def positioning(self, t):
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

                dt_s += compute_relativistic_correction(
                    self.__ephemeris.find_last_satellite_ephemeris(prn, t.GPST()), ts_2.GPST())
                
                dt_earth = t.clone()
                dt_earth.set_float_second(
                    dt_earth.get_float_second()+dt_r/constant.c-ts_2.get_float_second())
                nx, ny, nz = wgs84_to_ecef(
                    sx, sy, sz, dt_earth.get_float_second()*constant.omega_e)

                elevation = get_wgs84_elevation(X, Y, Z, nx, ny, nz)
                P[i][i] = math.sin(elevation)*math.sin(elevation)

                R = math.sqrt((nx-X)*(nx-X)+(ny-Y)*(ny-Y)+(nz-Z)*(nz-Z))
                A[i][0] = (X-nx)/R
                A[i][1] = (Y-ny)/R
                A[i][2] = (Z-nz)/R
                A[i][3] = 1
                l[i][0] = rho - R + constant.c*dt_s + \
                    1.54573 * (rho - obs.data[prn]['P2']['Obs'])
                i += 1

            nxx = np.dot(np.dot(np.dot(np.linalg.inv(
                np.dot(np.dot(A.transpose(), P), A)), A.transpose()), P), l)

            X += nxx[0][0]
            Y += nxx[1][0]
            Z += nxx[2][0]
            dt_r = nxx[3][0]

            if np.linalg.norm(nxx[0:3]) < 0.01:
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
