'''
Description: 
Author: notplus
Date: 2021-03-19 20:56:10
LastEditors: notplus
LastEditTime: 2021-04-20 20:22:03
'''

import numpy as np
import argparse
import sys
import ephemeris_module.ephemeris as eph
from utils.time_convert import Time
import observation.observation as obs

def parse_args():
    """
       Parse input arguments
       """
    parser = argparse.ArgumentParser(
        description='Compute satellite coordinate')
    parser.add_argument('-e', dest='ephemeris',
                        help='input the ephemeris file',
                        default=None, type=str)
    parser.add_argument('-o', dest='out_path',
                        help='output file path',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    print('Called with args:')
    print(args)

    ephemeris = eph.Ephemeris(args.ephemeris)
    print(ephemeris.compute_satellite_coordinates(1, Time(2020, 11, 5)))
    # print(ephemeris.compute_satellite_coordinates(1, Time(2020, 11, 8)))
    # print(ephemeris.compute_satellite_coordinates(1, Time(2020, 11, 7), 'C')) # BD C01

    # prns= [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    
    # Time(xxxx, xx, xx) 起始时间 / Time(xxxx, xx, xx)终止时间 / 5 时间间隔
    # ephemeris.output_precision_ephemeris(
    #     args.out_path, prns, Time(2020, 11, 5), Time(2020, 11, 6), 5)

    # ephemeris.output_precision_ephemeris(
    #     args.out_path, prns, Time(2020, 11, 8), Time(2020, 11, 9), 5)

    observation = obs.Observation("../obs/obs/leij3100.20o")
    