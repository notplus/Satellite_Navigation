'''
Description: 
Author: notplus
Date: 2021-03-19 20:56:10
LastEditors: notplus
LastEditTime: 2021-03-28 21:59:39
'''

import numpy as np
import argparse
import sys
import ephemeris_module.ephemeris as eph
from utils.time_convert import Time


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

    gps = eph.Ephemeris(args.ephemeris)
    # print(gps.computeSatelliteCoordinates(1, Time(2020, 11, 5)))
    print(gps.computeSatelliteCoordinates(1, Time(2020, 11, 8)))

