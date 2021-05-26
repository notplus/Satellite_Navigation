'''
Description: 
Author: notplus
Date: 2021-05-26 08:52:54
LastEditors: notplus
LastEditTime: 2021-05-26 10:17:03
FilePath: /positioning/correction.py

Copyright (c) 2021 notplus
'''

from ephemeris_module.satellite import Satellite
import math
import utils.constant as constant


def compute_relativistic_correction(satellite: Satellite, t):
    t_k = t-satellite.record.toe
    a = satellite.record.sqrt_a*satellite.record.sqrt_a
    n_0 = math.sqrt(constant.mu/a/a/a)
    n = n_0+satellite.record.delta_n
    m_k = satellite.record.m_0+n*t_k

    e_k1 = m_k
    e_k0 = 0.0
    while abs(e_k1-e_k0) > 1e-12:
        e_k0 = e_k1
        e_k1 = m_k+satellite.record.e*math.sin(e_k0)
    e_k = e_k1

    F = -2*math.sqrt(constant.mu)/constant.c/constant.c
    delta_t_r = F*satellite.record.e*satellite.record.sqrt_a*math.sin(e_k)

    return delta_t_r
