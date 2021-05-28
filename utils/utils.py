'''
Description: 
Author: notplus
Date: 2021-03-29 10:25:50
LastEditors: notplus
LastEditTime: 2021-05-28 15:32:07
FilePath: /utils/utils.py

Copyright (c) 2021 notplus
'''

import numpy as np

bds_geo = [1, 2, 3, 4, 5, 18, 59, 60, 61]


def parseDouble(str):
    str = str.replace('D', 'e')

    if not str.isspace():
        return float(str)
    else:
        return 0


def is_bds_geo(prn):
    if prn in bds_geo:
        return True
    else:
        return False


def rotation_matrix(roll, pitch, yaw):
    r_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]], dtype=float)

    r_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]], dtype=float)

    r_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]], dtype=float)

    R = np.matmul(np.matmul(r_x, r_y), r_z)

    return R


def rotation_matrix_z(epsilon):
    r_z = np.array([[np.cos(epsilon), np.sin(epsilon), 0],
                    [-np.sin(epsilon), np.cos(epsilon), 0],
                    [0, 0, 1]], dtype=float)
    return r_z


def rotation_matrix_x(epsilon):
    r_x = np.array([[1, 0, 0],
                    [0, np.cos(epsilon), np.sin(epsilon)],
                    [0, -np.sin(epsilon), np.cos(epsilon)]], dtype=float)
    return r_x


def rotation_matrix_y(epsilon):
    r_y = np.array([[np.cos(epsilon), 0, -np.sin(epsilon)],
                    [0, 1, 0],
                    [np.sin(epsilon), 0, np.cos(epsilon)]], dtype=float)
    return r_y
