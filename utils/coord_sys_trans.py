'''
Description: 
Author: notplus
Date: 2021-05-26 16:05:34
LastEditors: notplus
LastEditTime: 2021-05-27 19:33:02
FilePath: /utils/coord_sys_trans.py

Copyright (c) 2021 notplus
'''

from math import sin
from math import cos
from math import atan
from math import sqrt
from math import pi
import utils.constant as constant


'''
@description: transform wgs84 to ecef
@param {*} x
@param {*} y
@param {*} z
@param {*} alpha
@return {*}
'''


def wgs84_to_ecef(x, y, z, alpha):
    nx = cos(alpha)*x+sin(alpha)*y
    ny = -sin(alpha)*x+cos(alpha)*y
    nz = z
    return nx, ny, nz


'''
@description: transform wgs84 to BLH
@param {*} x
@param {*} y
@param {*} z
@return {*}
'''


def wgs84_to_blh(x, y, z):
    e = sqrt(2*constant.f-constant.f*constant.f)
    L = atan(y/x)
    if x < 0:
        L += pi
    elif x > 0 and y < 0:
        L += 2*pi
    B0 = atan(z/sqrt(x*x+y*y))
    N = constant.a/sqrt(1-e*e*sin(B0)*sin(B0))
    B1 = atan((z+N*e*e*sin(B0))/sqrt(x*x+y*y))

    while abs(B1-B0) >= 1e-5:
        B0 = B1
        N = constant.a/sqrt(1-e*e*sin(B1)*sin(B1))
        B1 = atan((z+N*e*e*sin(B1))/sqrt(x*x+y*y))

    B = B1
    H = sqrt(x*x + y*y)/cos(B)-N

    return B, L, H


'''
@description: 
@param {*} x
@param {*} y
@param {*} z
@param {*} sx
@param {*} sy
@param {*} sz
@return {*}
'''


def wgs84_to_enu(x, y, z, sx, sy, sz):
    B, L, _ = wgs84_to_blh(x, y, z)

    e = -sin(L)*(sx-x)+cos(L)*(sy-y)
    n = -sin(B)*cos(L)*(sx-x)-sin(B)*sin(L)*(sy-y)+cos(B)*(sz-z)
    u = cos(B)*cos(L)*(sx-x)+cos(B)*sin(L)*(sy-y)+sin(B)*(sz-z)

    return e, n, u


'''
@description: 
@param {*} x
@param {*} y
@param {*} z
@param {*} sx
@param {*} sy
@param {*} sz
@return {*}
'''


def get_wgs84_elevation_azimuth(x, y, z, sx, sy, sz):
    e, n, u = wgs84_to_enu(x, y, z, sx, sy, sz)
    return atan(u/sqrt(n*n+e*e)), atan(e/n)
