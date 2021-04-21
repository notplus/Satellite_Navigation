'''
Description: 
Author: notplus
Date: 2021-04-20 21:19:15
LastEditors: notplus
LastEditTime: 2021-04-21 16:48:54
FilePath: /satellite_coordinate/positioning/single_point.py
'''

from ephemeris_module.ephemeris import Ephemeris
from observation.observation import Observation
# from utils.time_convert import Time
import utils.constant as constant
import datetime
from utils.coord_sys_trans import wgs84_to_ecef
import math
import numpy as np
from utils.coord_sys_trans import get_wgs84_elevation


class SinglePointPositioning(object):
    def __init__(self, ephemeris_path, observation_path):
        self.__ephemeris = Ephemeris(ephemeris_path)
        self.__observation = Observation(observation_path)

    def positioning(self, t):
        X, Y, Z, dt_r = 1, 1, 1, 0
        obs = self.__observation.find_last_observation(t)
        num_satellites = 0
        for k in obs.data.keys():
            if k[0] == 'G':
                num_satellites += 1
        P = np.identity(num_satellites)
        i = 0
        for k in obs.data.keys():
            if k[0] == 'G':
                sx, sy, sz, _ = self.__ephemeris.compute_satellite_coordinates(
                    k, t)
                elevation = get_wgs84_elevation(X, Y, Z, sx, sy, sz)
                P[i][i] = math.sin(elevation)*math.sin(elevation)
                i += 1

        while True:
            A = np.zeros([num_satellites, 4])
            l = np.zeros([num_satellites, 1])
            i = 0
            xx = np.zeros([4, 1])
            for prn in obs.data:
                if prn[0] != 'G':
                    continue
                rho = obs.data[prn]['C1']['Obs']
                _, _, _, dt_s = self.__ephemeris.compute_satellite_coordinates(
                    prn, t)

                tau = rho/constant.c-dt_r+dt_s+1
                tau_n = rho/constant.c-dt_r+dt_s
                while abs(tau-tau_n) >= 1e-8:
                    tau = tau_n
                    t_s = obs.epoch-datetime.timedelta(microseconds=tau*1e6)
                    t_s.set_float_second(obs.epoch.get_float_second()-tau)
                    sx, sy, sz, dt_s = self.__ephemeris.compute_satellite_coordinates(
                        prn, t_s)
                    nx, ny, nz = wgs84_to_ecef(
                        sx, sy, sz, tau*constant.omega_e)
                    R = math.sqrt((nx-X)*(nx-X)+(ny-Y) * (ny-Y)+(nz-Z)*(nz-Z))
                    tau_n = R/constant.c

                A[i][0] = (X-nx)/R
                A[i][1] = (Y-ny)/R
                A[i][2] = (Z-nz)/R
                A[i][3] = 1
                l[i][0] = rho - R + constant.c*dt_s-constant.c*dt_r
                i += 1

            nxx = np.dot(np.dot(np.dot(np.linalg.inv(
                np.dot(np.dot(A.transpose(), P), A)), A.transpose()), P), l)

            X += nxx[0][0]
            Y += nxx[1][0]
            Z += nxx[2][0]
            dt_r += nxx[3][0]/constant.c

            if np.sum(np.abs(xx-nxx)) < 1e-8:
                break
            xx = nxx

            i = 0
            P = np.identity(num_satellites)
            for k in obs.data.keys():
                if k[0] == 'G':
                    sx, sy, sz, _ = self.__ephemeris.compute_satellite_coordinates(
                        k, t)
                    elevation = get_wgs84_elevation(X, Y, Z, sx, sy, sz)
                    P[i][i] = math.sin(elevation)*math.sin(elevation)
                    i += 1

        return X, Y, Z

    def compute_satellite_coordinates(self, prn, t):
        return self.__ephemeris.compute_satellite_coordinates(prn, t)
