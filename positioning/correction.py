'''
Description: 
Author: notplus
Date: 2021-05-26 08:52:54
LastEditors: notplus
LastEditTime: 2021-05-27 20:04:25
FilePath: /positioning/correction.py

Copyright (c) 2021 notplus
'''

from utils.time_convert import Time
from ephemeris_module.ephemeris import Ephemeris
from ephemeris_module.satellite import Satellite
import math
import utils.constant as constant
from utils.coord_sys_trans import *


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


def compute_ionosphere_correction_k8_model(t: Time, ephemeris: Ephemeris, elevation, azimuth, phi, lambda_):
    # 1
    psi = 0.0137/(elevation/math.pi+0.11)-0.022

    # 2
    phi_I = phi / math.pi + psi*math.cos(azimuth)

    if phi_I > 0.416:
        phi_I = 0.416
    elif phi_I < -0.416:
        phi_I = -0.416

    # 3
    lambda_i = lambda_/math.pi+psi*math.sin(azimuth)/math.cos(phi_I)

    # 4
    phi_m = phi_I + 0.064*math.cos((lambda_i-1.617)*math.pi)

    # 5
    t = 43200*lambda_i+t.GPST()
    t -= math.floor(t/86400)*86400

    # 6
    a_i = A_I = ephemeris.ion_alpha_a0 + ephemeris.ion_alpha_a1*phi_m + \
        ephemeris.ion_alpha_a2*phi_m*phi_m+ephemeris.ion_alpha_a3*phi_m*phi_m*phi_m
    if A_I < 0:
        A_I = 0

    # 7
    P_I = ephemeris.ion_beta_b0 + ephemeris.ion_beta_b1*phi_m + \
        ephemeris.ion_beta_b2*phi_m*phi_m+ephemeris.ion_beta_b3*phi_m*phi_m*phi_m
    if P_I < 72000:
        P_I = 72000

    # 8
    X_I = 2*math.pi*(t-50400)/P_I

    # 9
    F = 1+16*math.pow(0.53-elevation/math.pi, 3)

    # 10
    if abs(X_I) <= 1.57:
        I_L1GPS = (5e-9+a_i*(1-X_I*X_I/2+X_I*X_I*X_I*X_I/24))*F
    else:
        I_L1GPS = 5e-9*F

    return I_L1GPS


def compute_troposphere_correction_hopfield(height, elevation):
    T_s = 273.15+15
    h_d = 40136 + 148.72*(T_s-273.16)
    h_w = 11000
    h_s = height

    K_d = 155.2*1e-7*(1015.75/T_s)*(h_d-h_s)
    K_w = 155.2*1e-7*(4810/T_s/T_s)*11.66*(h_w-h_s)

    delta_s = K_d/math.sin(math.sqrt(elevation*elevation+6.25))+K_w / \
        math.sin(math.sqrt(elevation*elevation+2.25))

    return delta_s
